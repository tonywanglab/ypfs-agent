(function () {
  var ActiveJobs = {
    STORAGE_KEY: "harness-active-jobs",
    LEGACY_STORAGE_KEY: "harness-active-job",
    LEGACY_EVAL_KEY: "harness-active-evaluation",
    MAX_AGE_MS: 30 * 60 * 1000,
    POLL_MS: 1500,
    LABELS: {
      experiment: "Running experiment",
      prompt_draft: "Generating new prompt",
      rubric_draft: "Generating new rubric",
    },
    pollTimer: null,
    jobs: [],

    labelFor: function (kind) {
      return this.LABELS[kind] || "Working…";
    },

    read: function () {
      try {
        var stored = window.sessionStorage.getItem(this.STORAGE_KEY);
        if (stored) {
          var parsed = JSON.parse(stored);
          return Array.isArray(parsed) ? parsed : [];
        }
        return this.migrateLegacy();
      } catch (_error) {
        return [];
      }
    },

    migrateLegacy: function () {
      try {
        var legacy = window.sessionStorage.getItem(this.LEGACY_STORAGE_KEY);
        if (!legacy) {
          legacy = window.sessionStorage.getItem(this.LEGACY_EVAL_KEY);
        }
        if (!legacy) return [];
        var old = JSON.parse(legacy);
        var migrated = [{
          kind: old.kind || "experiment",
          jobId: old.jobId || old.experimentId || old.launchId || "",
          returnPath: old.returnPath || "/chat",
          startedAt: old.startedAt || Date.now(),
        }];
        this.write(migrated);
        window.sessionStorage.removeItem(this.LEGACY_STORAGE_KEY);
        window.sessionStorage.removeItem(this.LEGACY_EVAL_KEY);
        return migrated;
      } catch (_error) {
        return [];
      }
    },

    write: function (jobs) {
      this.jobs = jobs;
      try {
        window.sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(jobs));
      } catch (_error) {
        // Form locking still works without storage.
      }
    },

    clear: function () {
      window.clearTimeout(this.pollTimer);
      this.pollTimer = null;
      this.jobs = [];
      try {
        window.sessionStorage.removeItem(this.STORAGE_KEY);
        window.sessionStorage.removeItem(this.LEGACY_STORAGE_KEY);
        window.sessionStorage.removeItem(this.LEGACY_EVAL_KEY);
      } catch (_error) {
        // Ignore unavailable storage.
      }
      this.updateChrome([]);
      document.querySelectorAll("form[data-active-job]").forEach(function (form) {
        ActiveJobs.resetForm(form);
      });
    },

    removeJob: function (jobId) {
      var next = this.jobs.filter(function (entry) {
        return entry.jobId !== jobId;
      });
      this.write(next);
      if (!next.length) {
        this.updateChrome([]);
      }
    },

    consumeUrlParams: function () {
      var currentUrl = new URL(window.location.href);
      var started = currentUrl.searchParams.get("job_started");
      var finished =
        currentUrl.searchParams.get("job_finished") ||
        currentUrl.searchParams.get("experiment_finished") ||
        currentUrl.searchParams.get("evaluation_finished");
      var changed = false;

      if (started && started !== "1") {
        var form = document.querySelector('form[data-active-job]');
        var kind = form ? form.dataset.activeJob || "experiment" : "experiment";
        var returnPath = form ? form.dataset.activeJobReturn || window.location.pathname : "/";
        this.track({ kind: kind, jobId: started, returnPath: returnPath });
        changed = true;
      }

      if (finished) {
        if (finished !== "1") {
          this.removeJob(finished);
        } else {
          this.clear();
        }
        changed = true;
      }

      if (changed) {
        currentUrl.searchParams.delete("job_started");
        currentUrl.searchParams.delete("job_finished");
        currentUrl.searchParams.delete("experiment_finished");
        currentUrl.searchParams.delete("evaluation_finished");
        window.history.replaceState({}, "", currentUrl.pathname + currentUrl.search + currentUrl.hash);
      }
      return changed;
    },

    track: function (entry) {
      var jobs = this.read();
      if (jobs.some(function (j) { return j.jobId === entry.jobId; })) {
        return;
      }
      jobs.push({
        kind: entry.kind,
        jobId: entry.jobId,
        returnPath: entry.returnPath || window.location.pathname,
        startedAt: entry.startedAt || Date.now(),
      });
      this.write(jobs);
    },

    statusUrl: function (jobId) {
      return "/jobs/" + encodeURIComponent(jobId) + "/status";
    },

    updateChrome: function (runningJobs) {
      var chip = document.getElementById("active-job-chip");
      if (!chip) return;
      if (!runningJobs.length) {
        chip.hidden = true;
        var label = document.getElementById("active-job-label");
        var detailEl = document.getElementById("active-job-detail");
        if (label) label.textContent = "Working…";
        if (detailEl) {
          detailEl.textContent = "";
          detailEl.hidden = true;
        }
        return;
      }
      chip.hidden = false;
      var primary = runningJobs[0];
      chip.href = primary.returnPath || "/";
      var label = document.getElementById("active-job-label");
      var detailEl = document.getElementById("active-job-detail");
      var count = runningJobs.length;
      var title = count > 1
        ? count + " jobs running"
        : (this.labelFor(primary.kind));
      var detail = primary.message || "";
      if (label) label.textContent = title;
      if (detailEl) {
        detailEl.textContent = detail;
        detailEl.hidden = !detail;
      }
    },

    findForm: function (kind) {
      return document.querySelector('form[data-active-job="' + kind + '"]');
    },

    setStatusText: function (form, title, detail) {
      var status = form.querySelector("[data-active-job-status]");
      if (!status) return;
      status.hidden = false;
      var titleNode = status.querySelector("[data-active-job-status-title]");
      var detailNode = status.querySelector("[data-active-job-status-detail]");
      if (titleNode || detailNode) {
        if (titleNode) titleNode.textContent = title || "";
        if (detailNode) {
          detailNode.textContent = detail || "";
          detailNode.hidden = !detail;
        }
        return;
      }
      status.textContent = detail ? title + " — " + detail : title;
    },

    applyProgress: function (entry, data, restored) {
      var form = this.findForm(entry.kind);
      var detail = (data && data.message) || (restored
        ? "Still running — restored after returning to this page."
        : "Queued…");
      if (form) {
        this.setStatusText(form, this.labelFor(entry.kind), detail);
      }
      entry.message = detail;
    },

    showOnForm: function (form, entry, restored) {
      if (!form) return;
      var submitBtn = form.querySelector("[data-active-job-submit]");
      var submitLabel = form.querySelector("[data-active-job-submit-label]");
      var lock = form.querySelector("[data-active-job-lock]");
      var resetBtn = form.querySelector("[data-active-job-reset]");
      var idleLabel = form.dataset.activeJobIdleLabel || "";

      form.dataset.activeJobRunning = "true";
      form.setAttribute("aria-busy", "true");
      if (submitBtn) {
        submitBtn.classList.add("is-loading");
        submitBtn.disabled = true;
        submitBtn.setAttribute("aria-busy", "true");
      }
      if (submitLabel) {
        if (!idleLabel) {
          form.dataset.activeJobIdleLabel = submitLabel.textContent;
        }
        submitLabel.textContent = this.labelFor(entry.kind);
      }
      if (lock) lock.inert = true;
      this.setStatusText(
        form,
        this.labelFor(entry.kind),
        restored
          ? "Still running — restored after returning to this page."
          : "Queued…"
      );
      if (resetBtn) resetBtn.hidden = !restored;
    },

    resetForm: function (form) {
      if (!form) return;
      var submitBtn = form.querySelector("[data-active-job-submit]");
      var submitLabel = form.querySelector("[data-active-job-submit-label]");
      var lock = form.querySelector("[data-active-job-lock]");
      var status = form.querySelector("[data-active-job-status]");
      var resetBtn = form.querySelector("[data-active-job-reset]");
      var idleLabel = form.dataset.activeJobIdleLabel;

      delete form.dataset.activeJobRunning;
      form.removeAttribute("aria-busy");
      if (submitBtn) {
        submitBtn.classList.remove("is-loading");
        submitBtn.disabled = false;
        submitBtn.removeAttribute("aria-busy");
      }
      if (submitLabel && idleLabel) submitLabel.textContent = idleLabel;
      if (lock) lock.inert = false;
      if (status) {
        status.hidden = true;
        var titleNode = status.querySelector("[data-active-job-status-title]");
        var detailNode = status.querySelector("[data-active-job-status-detail]");
        if (!titleNode && !detailNode) status.textContent = "";
      }
      if (resetBtn) resetBtn.hidden = true;
    },

    handleFinished: function (entry, data) {
      var form = this.findForm(entry.kind);
      this.removeJob(entry.jobId);
      if (form) this.resetForm(form);

      if (data && data.result_url && data.status === "finished") {
        if (entry.kind === "experiment") {
          window.location.assign(data.result_url);
        } else {
          window.location.assign(data.result_url + "?job_finished=" + encodeURIComponent(entry.jobId));
        }
        return;
      }

      if (data && data.status === "failed") {
        if (form) {
          this.setStatusText(
            form,
            "Stopped before completion",
            data.error || "You can retry."
          );
          var status = form.querySelector("[data-active-job-status]");
          if (status) status.hidden = false;
        }
        if (data.run_id && entry.kind === "experiment") {
          window.location.assign("/runs/" + encodeURIComponent(data.run_id));
        }
      }
    },

    pollAll: function () {
      var self = this;
      var jobs = this.read().filter(function (entry) {
        return Date.now() - Number(entry.startedAt) <= self.MAX_AGE_MS;
      });
      if (jobs.length !== this.read().length) {
        this.write(jobs);
      }
      if (!jobs.length) {
        this.clear();
        return;
      }

      var pending = jobs.length;
      var runningSnapshot = [];

      jobs.forEach(function (entry) {
        window.fetch(self.statusUrl(entry.jobId), { headers: { Accept: "application/json" } })
          .then(function (response) {
            return response.json().then(function (data) {
              return { ok: response.ok, data: data, entry: entry };
            });
          })
          .then(function (result) {
            pending -= 1;
            if (!result.ok) {
              if (Date.now() - Number(result.entry.startedAt) > 10000) {
                self.removeJob(result.entry.jobId);
                self.resetForm(self.findForm(result.entry.kind));
              }
            } else if (result.data.status === "running" || result.data.status === "pending") {
              self.applyProgress(result.entry, result.data, false);
              runningSnapshot.push(result.entry);
            } else {
              self.handleFinished(result.entry, result.data);
            }
            if (pending === 0) {
              if (runningSnapshot.length) {
                self.updateChrome(runningSnapshot);
                self.pollTimer = window.setTimeout(function () {
                  self.pollAll();
                }, self.POLL_MS);
              } else if (self.read().length) {
                self.pollTimer = window.setTimeout(function () {
                  self.pollAll();
                }, self.POLL_MS);
              }
            }
          })
          .catch(function () {
            pending -= 1;
            if (pending === 0 && self.read().length) {
              self.pollTimer = window.setTimeout(function () {
                self.pollAll();
              }, self.POLL_MS * 2);
            }
          });
      });
    },

    restore: function () {
      this.consumeUrlParams();
      var jobs = this.read().filter(function (entry) {
        return Date.now() - Number(entry.startedAt) <= ActiveJobs.MAX_AGE_MS;
      });
      if (jobs.length !== this.read().length) {
        this.write(jobs);
      }
      if (!jobs.length) {
        document.querySelectorAll("form[data-active-job]").forEach(function (form) {
          ActiveJobs.resetForm(form);
        });
        return;
      }
      jobs.forEach(function (entry) {
        var form = ActiveJobs.findForm(entry.kind);
        if (form) ActiveJobs.showOnForm(form, entry, true);
      });
      this.updateChrome(jobs);
      this.pollAll();
    },

    bindForm: function (form) {
      var self = this;
      var resetBtn = form.querySelector("[data-active-job-reset]");
      if (resetBtn) {
        resetBtn.addEventListener("click", function () {
          var kind = form.dataset.activeJob;
          var remaining = self.read().filter(function (entry) {
            return entry.kind !== kind;
          });
          self.write(remaining);
          self.resetForm(form);
          if (!remaining.length) self.updateChrome([]);
        });
      }
      form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) return;
        var kind = form.dataset.activeJob || "job";
        var idField = form.dataset.jobIdField || "job_id";
        var idInput = form.querySelector('[name="' + idField + '"]');
        if (!idInput || !idInput.value) return;
        var entry = {
          kind: kind,
          jobId: idInput.value,
          returnPath: form.dataset.activeJobReturn || window.location.pathname,
          startedAt: Date.now(),
        };
        self.track(entry);
        self.showOnForm(form, entry, false);
        self.updateChrome(self.read());
        self.pollAll();
      });
    },

    init: function () {
      var self = this;
      document.querySelectorAll("form[data-active-job]").forEach(function (form) {
        self.bindForm(form);
      });
      this.restore();
      window.addEventListener("pageshow", function () {
        self.restore();
      });
    },
  };

  ActiveJobs.init();

  function syncSamplesRange(range) {
    var output = document.getElementById("samples-value");
    if (!output) return;
    var min = Number(range.min) || 1;
    var max = Number(range.max) || 20;
    var value = Number(range.value);
    var fill = ((value - min) / (max - min)) * 100;
    range.style.setProperty("--samples-fill", fill + "%");
    output.textContent = String(value);
    output.setAttribute("aria-live", "polite");
  }

  var samplesRange = document.getElementById("samples-range");
  if (samplesRange) {
    syncSamplesRange(samplesRange);
    samplesRange.addEventListener("input", function () {
      syncSamplesRange(samplesRange);
    });
  }

  document.querySelectorAll("[data-markdown-editor]").forEach(function (editor) {
    var input = editor.querySelector("[data-markdown-input]");
    var preview = editor.querySelector("[data-markdown-preview]");
    var status = editor.querySelector("[data-preview-status]");
    var previewUrl = editor.dataset.previewUrl;
    var timer = null;
    var controller = null;

    if (!input || !preview || !previewUrl) return;

    input.addEventListener("input", function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(function () {
        if (controller) controller.abort();
        controller = new AbortController();
        if (status) status.textContent = "Updating…";

        window.fetch(previewUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: input.value }),
          signal: controller.signal,
        }).then(function (response) {
          if (!response.ok) throw new Error("Preview request failed");
          return response.json();
        }).then(function (result) {
          preview.innerHTML = result.html || "";
          if (status) status.textContent = "Synced";
        }).catch(function (error) {
          if (error.name === "AbortError") return;
          if (status) status.textContent = "Preview unavailable";
        });
      }, 180);
    });
  });

  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.dataset.confirm || "Delete this item?")) {
        event.preventDefault();
      }
    });
  });

  document.querySelectorAll("[data-stop-details-toggle]").forEach(function (input) {
    ["click", "mousedown", "mouseup", "pointerdown", "pointerup"].forEach(function (type) {
      input.addEventListener(type, function (event) {
        event.stopPropagation();
      });
    });
  });

  document.querySelectorAll("[data-popover]").forEach(function (root) {
    var trigger = root.querySelector("[data-popover-trigger]");
    var panel = root.querySelector("[data-popover-panel]");
    if (!trigger || !panel) return;

    function isOpen() {
      return panel.getAttribute("data-open") === "true";
    }

    function openPopover() {
      panel.setAttribute("data-open", "true");
      panel.inert = false;
      trigger.setAttribute("aria-expanded", "true");
      var focusable = panel.querySelector("select, button, a, input, textarea");
      if (focusable) focusable.focus({ preventScroll: true });
    }

    function closePopover() {
      if (!isOpen()) return;
      panel.removeAttribute("data-open");
      panel.inert = true;
      trigger.setAttribute("aria-expanded", "false");
    }

    panel.inert = true;

    trigger.addEventListener("click", function (event) {
      event.stopPropagation();
      if (isOpen()) closePopover();
      else openPopover();
    });

    document.addEventListener("click", function (event) {
      if (!isOpen()) return;
      if (root.contains(event.target)) return;
      closePopover();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        closePopover();
        trigger.focus({ preventScroll: true });
      }
    });
  });

  function syncCollapsibleToggle(btn, pre) {
    var needsToggle = pre.scrollHeight > pre.clientHeight + 1 || pre.classList.contains("is-expanded");
    btn.hidden = !needsToggle;
  }

  document.querySelectorAll(".collapsible-section").forEach(function (section) {
    var btn = section.querySelector(".collapsible-toggle");
    var pre = section.querySelector(".collapsible-window");
    if (!btn || !pre) return;

    var expandLabel = btn.dataset.expandLabel || "Show full";
    var collapseLabel = btn.dataset.collapseLabel || "Collapse";

    syncCollapsibleToggle(btn, pre);
    btn.addEventListener("click", function () {
      var expanded = pre.classList.toggle("is-expanded");
      pre.classList.toggle("is-collapsed", !expanded);
      btn.setAttribute("aria-expanded", expanded);
      btn.textContent = expanded ? collapseLabel : expandLabel;
      syncCollapsibleToggle(btn, pre);
    });
  });

  var reviewEntries = document.getElementById("review-entries");
  var reviewTemplate = document.getElementById("review-entry-template");
  var reviewForm = document.getElementById("reviews-form");

  function syncReviewEntries() {
    if (!reviewEntries) return;
    var entries = reviewEntries.querySelectorAll(".review-entry");
    entries.forEach(function (entry, index) {
      var legend = entry.querySelector("legend");
      if (legend) legend.textContent = "Review " + (index + 1);
      var removeBtn = entry.querySelector(".review-remove");
      if (!removeBtn) return;
      removeBtn.hidden = entries.length === 1;
    });
  }

  if (reviewEntries && reviewTemplate) {
    syncReviewEntries();
    var addBtn = reviewForm && reviewForm.querySelector(".review-add");
    if (addBtn) {
      addBtn.addEventListener("click", function () {
        reviewEntries.appendChild(reviewTemplate.content.cloneNode(true));
        syncReviewEntries();
      });
    }
    reviewEntries.addEventListener("click", function (event) {
      var target = event.target;
      if (!(target instanceof HTMLElement) || !target.classList.contains("review-remove")) return;
      var entry = target.closest(".review-entry");
      if (!entry || reviewEntries.querySelectorAll(".review-entry").length === 1) return;
      entry.remove();
      syncReviewEntries();
    });
  }

  document.querySelectorAll(".flash-dismiss").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest("li");
      if (!item) return;
      item.classList.add("is-dismissing");
      item.addEventListener("transitionend", function () {
        item.remove();
        var list = item.closest(".flash");
        if (list && !list.children.length) {
          var region = list.closest(".flash-region");
          if (region) region.remove();
        }
      }, { once: true });
    });
  });

  function pad2(value) {
    return String(value).padStart(2, "0");
  }

  document.querySelectorAll("[data-local-datetime]").forEach(function (node) {
    var raw = node.getAttribute("data-local-datetime");
    if (!raw) return;
    var date = new Date(raw);
    if (Number.isNaN(date.getTime())) return;

    var day =
      date.getFullYear() +
      "-" +
      pad2(date.getMonth() + 1) +
      "-" +
      pad2(date.getDate());
    var time = pad2(date.getHours()) + ":" + pad2(date.getMinutes());
    var zone =
      new Intl.DateTimeFormat(undefined, { timeZoneName: "short" })
        .formatToParts(date)
        .find(function (part) { return part.type === "timeZoneName"; });

    var dayNode = node.querySelector(".run-date-day");
    var timeNode = node.querySelector(".run-date-time");
    if (dayNode) dayNode.textContent = day;
    if (timeNode) {
      timeNode.textContent = time + (zone ? " " + zone.value : "");
    }
    node.setAttribute(
      "title",
      date.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        second: "2-digit",
        timeZoneName: "short",
      })
    );
  });
})();
