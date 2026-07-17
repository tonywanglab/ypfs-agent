(function () {
  var ActiveJob = {
    STORAGE_KEY: "harness-active-job",
    MAX_AGE_MS: 30 * 60 * 1000,
    LABELS: {
      experiment: "Running experiment",
      prompt_draft: "Generating new prompt",
      rubric_draft: "Generating new rubric",
    },
    pollTimer: null,

    labelFor: function (kind) {
      return this.LABELS[kind] || "Working…";
    },

    read: function () {
      try {
        var stored = window.sessionStorage.getItem(this.STORAGE_KEY);
        return stored ? JSON.parse(stored) : null;
      } catch (_error) {
        return null;
      }
    },

    write: function (state) {
      try {
        window.sessionStorage.setItem(this.STORAGE_KEY, JSON.stringify(state));
      } catch (_error) {
        // UI locking still works without storage.
      }
    },

    clear: function () {
      window.clearTimeout(this.pollTimer);
      this.pollTimer = null;
      try {
        window.sessionStorage.removeItem(this.STORAGE_KEY);
      } catch (_error) {
        // Ignore unavailable storage.
      }
      this.updateChrome(null);
    },

    updateChrome: function (state) {
      var status = document.getElementById("active-job-status");
      if (!status) return;
      if (!state) {
        status.hidden = true;
        this.updateStatusText(null, "");
        return;
      }
      status.hidden = false;
      status.href = state.returnPath || "/";
      this.updateStatusText(state, state.progressMessage || state.label || this.labelFor(state.kind));
    },

    resolveStatusUrl: function (state) {
      if (!state || !state.jobId) return "";
      if (state.statusUrlTemplate) {
        return state.statusUrlTemplate.replace(
          "__JOB_ID__",
          encodeURIComponent(state.jobId)
        );
      }
      return "/tasks/" + encodeURIComponent(state.jobId) + "/status";
    },

    updateStatusText: function (state, text) {
      var textEl = document.getElementById("active-job-text");
      if (!textEl) return;
      textEl.textContent = text || "Working…";
      if (state && text) {
        state.progressMessage = text;
        this.write(state);
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

    experimentDetail: function (data) {
      var progress = (data && data.progress) || {};
      if (progress.message) return progress.message;
      var samples = Number(data && data.payload && data.payload.samples) || 1;
      if (samples > 1) {
        return "Starting " + samples + " samples…";
      }
      return "Preparing run…";
    },

    applyExperimentProgress: function (form, state, data) {
      if (state.kind !== "experiment") return;
      var detail = this.experimentDetail(data);
      if (form) {
        this.setStatusText(
          form,
          state.label || this.LABELS.experiment,
          detail
        );
      }
      this.updateStatusText(state, detail || state.label || this.LABELS.experiment);
    },

    applyProgress: function (state, data) {
      if (state.kind === "experiment") {
        this.applyExperimentProgress(this.findForm(state.kind), state, data);
        return;
      }
      var form = this.findForm(state.kind);
      var detail = (data && data.progress && data.progress.message)
        || "Controls are locked until generation completes.";
      if (form) {
        this.setStatusText(form, state.label || this.labelFor(state.kind), detail);
      }
      this.updateStatusText(state, detail || state.label || this.labelFor(state.kind));
    },

    showOnForm: function (form, state, restored) {
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
        submitLabel.textContent = state.label || this.labelFor(state.kind);
      }
      if (lock) lock.inert = true;

      if (state.kind === "experiment") {
        this.applyExperimentProgress(form, state, { samples: state.samples });
      } else {
        this.setStatusText(
          form,
          state.label || this.labelFor(state.kind),
          "Controls are locked until generation completes."
        );
      }
      // The reset button only matters when re-attaching to a run that may be
      // stuck — the fresh poll() call right after this fills in real progress
      // within a second or two either way.
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

    finish: function (state, result) {
      var form = this.findForm(state.kind);
      if (result && result.result_url && result.status === "finished") {
        this.clear();
        if (form) this.resetForm(form);
        window.location.assign(result.result_url);
        return;
      }
      var failed = result && result.status === "failed";
      if (!form) {
        // No form on this page (e.g. a dashboard-launched draft finished
        // while the user is on a run detail page) — stop polling but keep
        // the header status visible long enough to show the outcome,
        // rather than clearing it (which would hide the text right away).
        window.clearTimeout(this.pollTimer);
        this.pollTimer = null;
        try {
          window.sessionStorage.removeItem(this.STORAGE_KEY);
        } catch (_error) {
          // Ignore unavailable storage.
        }
        if (failed) {
          var status = document.getElementById("active-job-status");
          this.updateStatusText(state, "Stopped before completion — " + (result.error || "open Experiment to retry."));
          if (status) status.hidden = false;
        } else {
          this.updateChrome(null);
        }
        return;
      }
      this.clear();
      this.resetForm(form);
      if (failed) {
        this.setStatusText(
          form,
          "Stopped before completion",
          result.error || "You can retry."
        );
        var formStatus = form.querySelector("[data-active-job-status]");
        if (formStatus) formStatus.hidden = false;
        return;
      }
      if (state.kind === "experiment") {
        this.setStatusText(form, "Evaluation finished", "Open Runs to view the result.");
        var experimentStatus = form.querySelector("[data-active-job-status]");
        if (experimentStatus) experimentStatus.hidden = false;
      }
    },

    poll: function (state) {
      var self = this;
      var form = this.findForm(state.kind);
      var url = this.resolveStatusUrl(state);
      if (!state.jobId || !url) {
        this.clear();
        if (form) this.resetForm(form);
        return;
      }
      window.fetch(url, { headers: { Accept: "application/json" } })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          var age = Date.now() - Number(state.startedAt);
          if (!result.ok && age < 10000) {
            self.pollTimer = window.setTimeout(function () {
              self.poll(state);
            }, 1500);
            return;
          }
          if (!result.ok) {
            self.updateStatusText(state, (state.label || self.labelFor(state.kind)) + " — interrupted. Reload and try again.");
            if (form) self.resetForm(form);
            return;
          }
          if (result.data.status === "running" || result.data.status === "queued") {
            self.applyProgress(state, result.data);
            self.pollTimer = window.setTimeout(function () {
              self.poll(state);
            }, 1500);
            return;
          }
          self.finish(state, result.data);
        })
        .catch(function () {
          if (Date.now() - Number(state.startedAt) > self.MAX_AGE_MS) {
            self.clear();
            if (form) self.resetForm(form);
            return;
          }
          self.pollTimer = window.setTimeout(function () {
            self.poll(state);
          }, 3000);
        });
    },

    restore: function () {
      var state = this.read();
      if (!state || Date.now() - Number(state.startedAt) > this.MAX_AGE_MS) {
        this.clear();
        document.querySelectorAll("form[data-active-job]").forEach(function (form) {
          ActiveJob.resetForm(form);
        });
        return;
      }
      this.updateChrome(state);
      var form = this.findForm(state.kind);
      if (form) {
        this.showOnForm(form, state, true);
      }
      if (state.jobId && this.resolveStatusUrl(state)) {
        this.poll(state);
      }
    },

    bindForm: function (form) {
      var self = this;
      var resetBtn = form.querySelector("[data-active-job-reset]");
      if (resetBtn) {
        resetBtn.addEventListener("click", function () {
          self.clear();
          self.resetForm(form);
        });
      }
      form.addEventListener("submit", function (event) {
        if (!form.checkValidity()) return;
        if (form.dataset.activeJobRunning === "true") {
          event.preventDefault();
          return;
        }
        var kind = form.dataset.activeJob || "job";
        var idField = form.dataset.jobIdField || "job_id";
        var idInput = form.querySelector('[name="' + idField + '"]');
        var samplesInput = form.querySelector('[name="samples"]');
        var state = {
          kind: kind,
          label: self.labelFor(kind),
          jobId: idInput ? idInput.value : "",
          returnPath: form.dataset.activeJobReturn || window.location.pathname,
          statusUrlTemplate: form.dataset.statusUrlTemplate || "",
          startedAt: Date.now(),
          samples: samplesInput ? Number(samplesInput.value) : undefined,
        };
        self.write(state);
        self.updateChrome(state);
        self.showOnForm(form, state, false);
        if (state.statusUrlTemplate && state.jobId) {
          self.poll(state);
        }
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

  ActiveJob.init();

  (function pollActiveTasksPanel() {
    var list = document.getElementById("active-tasks-list");
    var countEl = document.querySelector("[data-active-tasks-count]");
    var emptyEl = document.querySelector("[data-active-tasks-empty]");
    var rows = document.querySelectorAll("[data-task-row]");
    if (!rows.length) return;

    // Updates rows in place and drops finished/failed ones — no full-page
    // reload. A task finishing shouldn't yank the supervisor away from
    // whatever else they're reading on the dashboard.
    function poll() {
      var stillActive = false;
      var fetches = Array.prototype.map.call(rows, function (row) {
        var taskId = row.getAttribute("data-task-id");
        if (!taskId) return Promise.resolve();
        return window.fetch("/tasks/" + encodeURIComponent(taskId) + "/status", {
          headers: { Accept: "application/json" },
        })
          .then(function (response) { return response.json(); })
          .then(function (data) {
            if (data.status === "queued" || data.status === "running") {
              var statusEl = row.querySelector("[data-task-status]");
              var messageEl = row.querySelector("[data-task-message]");
              if (statusEl) statusEl.textContent = data.status;
              if (messageEl) messageEl.textContent = (data.progress && data.progress.message) || "";
              stillActive = true;
            } else {
              row.remove();
            }
          })
          .catch(function () {});
      });
      Promise.all(fetches).then(function () {
        rows = document.querySelectorAll("[data-task-row]");
        if (countEl) countEl.textContent = String(rows.length);
        if (!rows.length) {
          if (list) list.hidden = true;
          if (emptyEl) emptyEl.hidden = false;
        }
        if (stillActive) {
          window.setTimeout(poll, 2000);
        }
      });
    }

    window.setTimeout(poll, 2000);
  })();

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
