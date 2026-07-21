(function () {
  var ActiveJob = {
    STORAGE_KEY: "harness-active-job",
    MAX_AGE_MS: 30 * 60 * 1000,
    LABELS: {
      experiment: "Running experiment...",
      prompt_draft: "Generating draft...",
    },
    pollTimer: null,

    labelFor: function (kind) {
      return this.LABELS[kind] || "Working…";
    },

    isTrackOnly: function (state, form) {
      if (state && state.trackOnly) return true;
      return !!(form && form.hasAttribute("data-active-job-track-only"));
    },

    stopPolling: function () {
      window.clearTimeout(this.pollTimer);
      this.pollTimer = null;
    },

    clearStorage: function () {
      try {
        window.sessionStorage.removeItem(this.STORAGE_KEY);
      } catch (_error) {
        // Ignore unavailable storage.
      }
    },

    showHeaderOutcome: function (state, text, href) {
      var status = document.getElementById("active-job-status");
      var textEl = document.getElementById("active-job-text");
      if (status) {
        status.hidden = false;
        status.href = href || (state && state.returnPath) || "/";
      }
      if (textEl) textEl.textContent = text || "Working…";
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
      this.stopPolling();
      this.clearStorage();
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

    applyProgress: function (state, data) {
      var form = this.findForm(state.kind);
      var trackOnly = this.isTrackOnly(state, form);
      var progressMessage = data && data.progress && data.progress.message;
      var headerText = progressMessage || state.label || this.labelFor(state.kind);
      if (form && !trackOnly) {
        var detail =
          progressMessage || "Controls are locked until generation completes.";
        this.setStatusText(form, state.label || this.labelFor(state.kind), detail);
      }
      this.updateStatusText(state, headerText);
    },

    showOnForm: function (form, state, restored) {
      if (!form || this.isTrackOnly(state, form)) return;
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

      this.setStatusText(
        form,
        state.label || this.labelFor(state.kind),
        "Controls are locked until generation completes."
      );
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
      var trackOnly = this.isTrackOnly(state, form);

      if (trackOnly) {
        this.stopPolling();
        this.clearStorage();
        if (result && result.status === "finished") {
          this.showHeaderOutcome(
            state,
            (result.progress && result.progress.message) || "Run complete",
            result.result_url || (state && state.returnPath)
          );
          return;
        }
        if (result && result.status === "failed") {
          this.showHeaderOutcome(
            state,
            "Run failed — " + (result.error || "try again."),
            state && state.returnPath
          );
          return;
        }
      }

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
        this.stopPolling();
        this.clearStorage();
        if (failed) {
          this.showHeaderOutcome(
            state,
            "Stopped before completion — " + (result.error || "open Experiment to retry."),
            state && state.returnPath
          );
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
            // A 404/5xx here means the tracked job id no longer resolves to
            // anything (e.g. left over from a previous session/build).
            // Show the message on this page, but drop it from storage so a
            // future page load doesn't resurrect and re-poll a dead job —
            // otherwise this "interrupted" text gets stuck in the header
            // forever, on every page, until sessionStorage is cleared by hand.
            self.updateStatusText(state, (state.label || self.labelFor(state.kind)) + " — interrupted. Reload and try again.");
            window.clearTimeout(self.pollTimer);
            self.pollTimer = null;
            try {
              window.sessionStorage.removeItem(self.STORAGE_KEY);
            } catch (_error) {
              // Ignore unavailable storage.
            }
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
        if (form.dataset.activeJobRunning === "true" && !self.isTrackOnly(null, form)) {
          event.preventDefault();
          return;
        }
        var kind = form.dataset.activeJob || "job";
        var idField = form.dataset.jobIdField || "job_id";
        var idInput = form.querySelector('[name="' + idField + '"]');
        var state = {
          kind: kind,
          label: self.labelFor(kind),
          jobId: idInput ? idInput.value : "",
          returnPath: form.dataset.activeJobReturn || window.location.pathname,
          statusUrlTemplate: form.dataset.statusUrlTemplate || "",
          startedAt: Date.now(),
          trackOnly: form.hasAttribute("data-active-job-track-only"),
        };
        self.write(state);
        self.updateChrome(state);
        self.showOnForm(form, state, false);
        if (state.jobId && self.resolveStatusUrl(state)) {
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

  document.querySelectorAll("[data-prompt-diff-panel]").forEach(function (panel) {
    var body = panel.querySelector("[data-prompt-diff-body]");
    var diffUrl = panel.dataset.diffUrl;
    var currentId = panel.dataset.currentId || "current";
    var currentPromptNode = document.getElementById("current-prompt-json");
    var currentPrompt = "";
    if (currentPromptNode) {
      try {
        currentPrompt = JSON.parse(currentPromptNode.textContent || '""');
      } catch (_error) {
        currentPrompt = "";
      }
    }
    var input = document.querySelector(panel.dataset.draftInput || "#prompt-text-editor");
    if (!body || !diffUrl || !input) return;

    var timer = null;
    var controller = null;

    function refreshDiff() {
      if (controller) controller.abort();
      controller = new AbortController();
      window.fetch(diffUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          before: currentPrompt,
          after: input.value,
          current_id: currentId,
        }),
        signal: controller.signal,
      })
        .then(function (response) {
          if (!response.ok) throw new Error("Diff request failed");
          return response.text();
        })
        .then(function (html) {
          body.innerHTML = html;
        })
        .catch(function (error) {
          if (error.name === "AbortError") return;
        });
    }

    input.addEventListener("input", function () {
      window.clearTimeout(timer);
      timer = window.setTimeout(refreshDiff, 180);
    });
  });

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
    var needsToggle =
      pre.classList.contains("is-expanded") ||
      pre.scrollHeight > pre.clientHeight + 1;
    btn.hidden = !needsToggle;
  }

  document.querySelectorAll(".collapsible-section").forEach(function (section) {
    var btn = section.querySelector(".collapsible-toggle");
    var pre = section.querySelector(".collapsible-window");
    if (!btn || !pre) return;

    var expandLabel = btn.dataset.expandLabel || "Expand";
    var collapseLabel = btn.dataset.collapseLabel || "Collapse";

    function setToggleLabel(expanded) {
      btn.setAttribute("aria-label", expanded ? collapseLabel : expandLabel);
      btn.setAttribute("aria-expanded", expanded ? "true" : "false");
    }

    function refresh() {
      syncCollapsibleToggle(btn, pre);
      setToggleLabel(pre.classList.contains("is-expanded"));
    }

    refresh();
    window.requestAnimationFrame(refresh);
    if (typeof ResizeObserver === "function") {
      new ResizeObserver(refresh).observe(pre);
    }

    btn.addEventListener("click", function () {
      var expanded = pre.classList.toggle("is-expanded");
      pre.classList.toggle("is-collapsed", !expanded);
      setToggleLabel(expanded);
      syncCollapsibleToggle(btn, pre);
    });
  });

  (function selectionFeedback() {
    var answer = document.getElementById("run-answer");
    var popup = document.getElementById("feedback-popup");
    var input = document.getElementById("feedback-popup-input");
    var errorEl = popup && popup.querySelector(".feedback-popup-error");
    var list = document.getElementById("feedback-list");
    var emptyState = document.getElementById("feedback-empty");
    var itemTemplate = document.getElementById("feedback-item-template");
    var draftSubmit = document.getElementById("feedback-draft-submit");
    var countBadge = document.getElementById("feedback-count");
    if (!answer || !popup || !input || !list || !itemTemplate) return;

    var feedbackUrl = answer.dataset.feedbackUrl;
    var deleteUrlTemplate = list.dataset.deleteUrlTemplate || "";
    var pendingText = "";
    var pendingRange = null;
    var sampleIndex = Number(answer.dataset.sampleIndex);
    var annotations = [];
    var lockedWindowScrollY = 0;
    var scrollLocked = false;

    // Focusing the popup input collapses window.getSelection(), which would
    // otherwise erase the browser's native blue highlight the instant the
    // popup opens. Draw our own highlight rects (independent of Selection
    // state) from the captured Range so it stays anchored to the original
    // text while the popup is open — same answer-relative coords as
    // committed annotations, so expand/collapse/scroll keep them aligned.
    var annotationLayer = document.createElement("div");
    annotationLayer.className = "feedback-annotation-layer";
    answer.appendChild(annotationLayer);

    var highlightRoot = document.createElement("div");
    highlightRoot.className = "feedback-annotation";
    highlightRoot.dataset.role = "pending-highlight";
    annotationLayer.appendChild(highlightRoot);

    function clearHighlight() {
      highlightRoot.innerHTML = "";
    }

    function rangeStillValid(range) {
      try {
        return !!(
          range &&
          !range.collapsed &&
          answer.contains(range.commonAncestorContainer)
        );
      } catch (_error) {
        return false;
      }
    }

    function answerRelativeRows(range) {
      var answerRect = answer.getBoundingClientRect();
      return collectLineRows(range).map(function (row) {
        return {
          top: row.top - answerRect.top + answer.scrollTop,
          left: row.left - answerRect.left + answer.scrollLeft,
          width: row.right - row.left,
          height: row.bottom - row.top,
        };
      });
    }

    // range.getClientRects() called directly on a selection that spans an
    // element boundary (e.g. across a <strong>/<code>/<a>, or across
    // paragraphs) can include a bounding rect for a fully-contained
    // ancestor element on top of the correct per-line text rects — that's
    // the "paragraph box" sitting over the line highlights. Restricting
    // measurement to a sub-range per Text node sidesteps it entirely: a
    // Text-node range only ever reports line rects, never a container box.
    function textNodesInRange(range) {
      var root = range.commonAncestorContainer;
      if (root.nodeType !== Node.ELEMENT_NODE) root = root.parentNode;
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
      var nodes = [];
      var node = walker.nextNode();
      while (node) {
        if (range.intersectsNode(node)) nodes.push(node);
        node = walker.nextNode();
      }
      return nodes;
    }

    function collectLineRows(range) {
      var rows = [];
      function addRect(rect) {
        if (rect.width <= 0 || rect.height <= 0) return;
        // getClientRects() still returns one rect per inline box fragment
        // within a single Text node (e.g. wrapped lines) — merge same-line
        // rects into one box, or the translucent fills stack into a
        // visibly darker patch where fragments overlap.
        for (var j = 0; j < rows.length; j++) {
          var row = rows[j];
          if (Math.abs(row.top - rect.top) < 2 && Math.abs(row.bottom - rect.bottom) < 2) {
            row.left = Math.min(row.left, rect.left);
            row.right = Math.max(row.right, rect.right);
            row.top = Math.min(row.top, rect.top);
            row.bottom = Math.max(row.bottom, rect.bottom);
            return;
          }
        }
        rows.push({ left: rect.left, right: rect.right, top: rect.top, bottom: rect.bottom });
      }

      textNodesInRange(range).forEach(function (node) {
        var nodeRange = document.createRange();
        nodeRange.setStart(node, node === range.startContainer ? range.startOffset : 0);
        nodeRange.setEnd(node, node === range.endContainer ? range.endOffset : node.length);
        var rects = nodeRange.getClientRects();
        for (var i = 0; i < rects.length; i++) addRect(rects[i]);
      });
      return rows;
    }

    function renderHighlight(range) {
      clearHighlight();
      if (!rangeStillValid(range)) return;
      answerRelativeRows(range).forEach(function (row) {
        var mark = document.createElement("div");
        mark.className = "feedback-highlight-rect";
        mark.style.top = row.top + "px";
        mark.style.left = row.left + "px";
        mark.style.width = row.width + "px";
        mark.style.height = row.height + "px";
        highlightRoot.appendChild(mark);
      });
    }

    function offsetsForRange(range) {
      if (!rangeStillValid(range)) return null;
      var map = textMap(answer);
      var start = -1;
      var end = -1;
      for (var i = 0; i < map.nodes.length; i++) {
        var entry = map.nodes[i];
        if (entry.node === range.startContainer) {
          start = entry.start + range.startOffset;
        }
        if (entry.node === range.endContainer) {
          end = entry.start + range.endOffset;
        }
      }
      if (start < 0 || end < 0 || end < start) return null;
      return { start: start, end: end };
    }

    function textMap(root) {
      var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
        acceptNode: function (node) {
          if (annotationLayer.contains(node)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        },
      });
      var nodes = [];
      var full = "";
      var node = walker.nextNode();
      while (node) {
        nodes.push({ node: node, start: full.length });
        full += node.nodeValue;
        node = walker.nextNode();
      }
      return { nodes: nodes, full: full };
    }

    function rangeFromOffsets(map, start, end) {
      var range = document.createRange();
      var startSet = false;
      var endSet = false;
      for (var i = 0; i < map.nodes.length; i++) {
        var entry = map.nodes[i];
        var nodeEnd = entry.start + entry.node.nodeValue.length;
        if (!startSet && start >= entry.start && start <= nodeEnd) {
          range.setStart(entry.node, start - entry.start);
          startSet = true;
        }
        if (!endSet && end >= entry.start && end <= nodeEnd) {
          range.setEnd(entry.node, end - entry.start);
          endSet = true;
        }
        if (startSet && endSet) break;
      }
      return startSet && endSet ? range : null;
    }

    function overlapsConsumed(start, end, consumed) {
      for (var i = 0; i < consumed.length; i++) {
        var span = consumed[i];
        if (start < span.end && end > span.start) return true;
      }
      return false;
    }

    function findNextRange(needle, consumed) {
      if (!needle) return null;
      var map = textMap(answer);
      var from = 0;
      while (from <= map.full.length) {
        var idx = map.full.indexOf(needle, from);
        if (idx === -1) return null;
        var end = idx + needle.length;
        if (!overlapsConsumed(idx, end, consumed)) {
          var range = rangeFromOffsets(map, idx, end);
          if (range) {
            consumed.push({ start: idx, end: end });
            return range;
          }
        }
        from = idx + 1;
      }
      return null;
    }

    function listIndexFor(feedbackId) {
      var items = list.querySelectorAll(".feedback-item");
      for (var i = 0; i < items.length; i++) {
        if (items[i].dataset.feedbackId === feedbackId) return i + 1;
      }
      return items.length;
    }

    function updateFeedbackChrome() {
      var count = list.querySelectorAll(".feedback-item").length;
      if (countBadge) countBadge.textContent = String(count);
      list.hidden = count === 0;
      if (emptyState) emptyState.hidden = count !== 0;
      if (draftSubmit) draftSubmit.disabled = count === 0;
    }

    function paintAnnotation(ann) {
      while (ann.root.firstChild) ann.root.removeChild(ann.root.firstChild);
      if (!rangeStillValid(ann.range)) return;

      var rows = answerRelativeRows(ann.range);
      rows.forEach(function (row) {
        var mark = document.createElement("div");
        mark.className = "feedback-annotation-rect";
        mark.style.top = row.top + "px";
        mark.style.left = row.left + "px";
        mark.style.width = row.width + "px";
        mark.style.height = row.height + "px";
        ann.root.appendChild(mark);
      });

      if (!rows.length) return;

      var first = rows[0];
      var marker = document.createElement("button");
      marker.type = "button";
      marker.className = "feedback-marker";
      marker.dataset.feedbackId = ann.feedbackId;
      marker.setAttribute("aria-label", "Delete feedback " + ann.index);
      var indexFace = document.createElement("span");
      indexFace.className = "feedback-marker-face feedback-marker-index";
      indexFace.setAttribute("aria-hidden", "true");
      indexFace.textContent = String(ann.index);
      var deleteFace = document.createElement("span");
      deleteFace.className = "feedback-marker-face feedback-marker-delete";
      deleteFace.setAttribute("aria-hidden", "true");
      deleteFace.innerHTML =
        '<svg class="feedback-marker-delete-icon" viewBox="0 0 12 12" aria-hidden="true" focusable="false">' +
        '<path d="M3 3l6 6M9 3l-6 6" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round"/>' +
        "</svg>";
      marker.appendChild(indexFace);
      marker.appendChild(deleteFace);
      marker.style.top = first.top + first.height / 2 + "px";
      ann.root.appendChild(marker);
      ann.marker = marker;
    }

    function renumberAnnotations() {
      annotations.forEach(function (ann) {
        ann.index = listIndexFor(ann.feedbackId);
        if (ann.marker) {
          var indexFace = ann.marker.querySelector(".feedback-marker-index");
          if (indexFace) indexFace.textContent = String(ann.index);
          ann.marker.setAttribute("aria-label", "Delete feedback " + ann.index);
        }
      });
    }

    function upsertAnnotation(feedbackId, selectedText, range) {
      var existing = annotations.find(function (ann) {
        return ann.feedbackId === feedbackId;
      });
      if (existing) {
        existing.selectedText = selectedText;
        existing.range = range;
        existing.index = listIndexFor(feedbackId);
        paintAnnotation(existing);
        return existing;
      }

      var root = document.createElement("div");
      root.className = "feedback-annotation";
      root.dataset.feedbackId = feedbackId;
      annotationLayer.appendChild(root);

      var ann = {
        feedbackId: feedbackId,
        selectedText: selectedText,
        range: range,
        index: listIndexFor(feedbackId),
        root: root,
        marker: null,
      };
      annotations.push(ann);
      paintAnnotation(ann);
      return ann;
    }

    function removeAnnotation(feedbackId) {
      annotations = annotations.filter(function (ann) {
        if (ann.feedbackId !== feedbackId) return true;
        if (ann.root && ann.root.parentNode) ann.root.parentNode.removeChild(ann.root);
        return false;
      });
      renumberAnnotations();
    }

    function relayoutAnnotations() {
      var consumed = [];
      // Keep each annotation on its original Range when still valid so
      // expand/collapse and duplicate phrases don't rebind the highlight.
      annotations.forEach(function (ann) {
        if (rangeStillValid(ann.range)) {
          var offsets = offsetsForRange(ann.range);
          if (offsets) consumed.push(offsets);
        }
      });
      annotations.forEach(function (ann) {
        if (!rangeStillValid(ann.range)) {
          ann.range = findNextRange(ann.selectedText, consumed);
        }
        ann.index = listIndexFor(ann.feedbackId);
        paintAnnotation(ann);
      });
      if (!popup.hidden && pendingRange) {
        renderHighlight(pendingRange);
      }
    }

    function hydrateAnnotations() {
      annotations.forEach(function (ann) {
        if (ann.root && ann.root.parentNode) ann.root.parentNode.removeChild(ann.root);
      });
      annotations = [];
      clearHighlight();
      if (!highlightRoot.parentNode) annotationLayer.appendChild(highlightRoot);
      var consumed = [];
      list.querySelectorAll(".feedback-item").forEach(function (li) {
        if (Number(li.dataset.sampleIndex) !== sampleIndex) return;
        var quote = li.querySelector(".feedback-quote");
        var text = quote ? quote.textContent : "";
        var range = findNextRange(text, consumed);
        if (!range) return;
        upsertAnnotation(li.dataset.feedbackId, text, range);
      });
    }

    function deleteFeedback(feedbackId, options) {
      options = options || {};
      if (!feedbackId) return;
      if (!options.skipConfirm && !window.confirm("Delete this feedback item?")) return;

      var li = list.querySelector('.feedback-item[data-feedback-id="' + feedbackId + '"]');
      var ann = annotations.find(function (item) {
        return item.feedbackId === feedbackId;
      });
      var liSnapshot = li ? li.cloneNode(true) : null;
      var annSnapshot =
        ann && ann.range
          ? {
              feedbackId: ann.feedbackId,
              selectedText: ann.selectedText,
              range: ann.range.cloneRange(),
            }
          : null;

      if (li) li.remove();
      removeAnnotation(feedbackId);
      updateFeedbackChrome();

      window
        .fetch(deleteUrlFor(feedbackId), {
          method: "POST",
          headers: {
            Accept: "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
        })
        .then(function (response) {
          if (!response.ok) throw new Error("delete failed");
          var contentType = response.headers.get("Content-Type") || "";
          if (contentType.indexOf("application/json") !== -1) return response.json();
          return { ok: true };
        })
        .catch(function () {
          window.alert("Could not delete feedback.");
          if (liSnapshot) {
            list.appendChild(liSnapshot);
            updateFeedbackChrome();
          }
          if (annSnapshot && rangeStillValid(annSnapshot.range)) {
            upsertAnnotation(
              annSnapshot.feedbackId,
              annSnapshot.selectedText,
              annSnapshot.range
            );
          }
        });
    }

    // Delegated so delete still works after paint/relayout replaces marker nodes.
    annotationLayer.addEventListener("click", function (event) {
      var marker = event.target.closest(".feedback-marker");
      if (!marker || !annotationLayer.contains(marker)) return;
      event.preventDefault();
      event.stopPropagation();
      deleteFeedback(marker.dataset.feedbackId);
    });


    function lockScroll() {
      if (scrollLocked) return;
      scrollLocked = true;
      lockedWindowScrollY = window.scrollY;
      answer.classList.add("is-scroll-locked");
      document.body.classList.add("feedback-scroll-locked");
      document.body.style.top = -lockedWindowScrollY + "px";
    }

    function unlockScroll() {
      if (!scrollLocked) return;
      scrollLocked = false;
      answer.classList.remove("is-scroll-locked");
      document.body.classList.remove("feedback-scroll-locked");
      document.body.style.top = "";
      window.scrollTo(0, lockedWindowScrollY);
    }

    function hidePopup() {
      popup.hidden = true;
      clearHighlight();
      unlockScroll();
      popup.style.position = "";
      clearError();
      input.value = "";
      pendingText = "";
      pendingRange = null;
    }

    function showError(message) {
      if (!errorEl) return;
      errorEl.textContent = message;
      errorEl.hidden = false;
      input.setAttribute("aria-invalid", "true");
    }

    function clearError() {
      if (!errorEl) return;
      errorEl.hidden = true;
      errorEl.textContent = "";
      input.removeAttribute("aria-invalid");
    }

    function showPopup(range) {
      pendingRange = range.cloneRange();
      var rect = range.getBoundingClientRect();
      lockScroll();
      renderHighlight(range);
      popup.hidden = false;
      clearError();
      input.value = "";
      // Body is position:fixed while locked, so place the popup in viewport coords.
      var top = rect.bottom + 8;
      var left = rect.left;
      var maxLeft = document.documentElement.clientWidth - popup.offsetWidth - 8;
      left = Math.max(8, Math.min(left, Math.max(maxLeft, 8)));
      popup.style.position = "fixed";
      popup.style.top = top + "px";
      popup.style.left = left + "px";
      window.requestAnimationFrame(function () {
        input.focus({ preventScroll: true });
      });
    }

    function deleteUrlFor(feedbackId) {
      return deleteUrlTemplate.replace("__FEEDBACK_ID__", encodeURIComponent(feedbackId));
    }

    function appendFeedbackItem(item) {
      var node = itemTemplate.content.cloneNode(true);
      var li = node.querySelector(".feedback-item");
      li.dataset.feedbackId = item.feedback_id;
      li.dataset.sampleIndex = String(item.sample_index);
      var quote = li.querySelector(".feedback-quote");
      if (quote) quote.textContent = item.selected_text;
      var comment = li.querySelector(".feedback-comment");
      if (comment) comment.textContent = item.comment;
      var form = li.querySelector("form");
      if (form) form.setAttribute("action", deleteUrlFor(item.feedback_id));
      list.appendChild(node);
      updateFeedbackChrome();
    }

    document.addEventListener("mouseup", function (event) {
      if (popup.contains(event.target)) return;
      if (event.target.closest && event.target.closest(".feedback-marker")) return;
      window.setTimeout(function () {
        var selection = window.getSelection();
        if (!selection || selection.isCollapsed) {
          hidePopup();
          return;
        }
        var text = selection.toString().trim();
        if (!text) {
          hidePopup();
          return;
        }
        var range = selection.getRangeAt(0);
        if (!answer.contains(range.commonAncestorContainer)) {
          return;
        }
        if (annotationLayer.contains(range.commonAncestorContainer)) {
          return;
        }
        pendingText = text;
        showPopup(range);
      }, 0);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && !popup.hidden) {
        hidePopup();
      }
    });

    document.addEventListener("mousedown", function (event) {
      if (popup.hidden) return;
      if (popup.contains(event.target) || answer.contains(event.target)) return;
      hidePopup();
    });

    input.addEventListener("input", function () {
      if (!errorEl || errorEl.hidden) return;
      clearError();
    });

    popup.addEventListener("submit", function (event) {
      event.preventDefault();
      var comment = input.value.trim();
      if (!pendingText || !comment) {
        showError("Add a comment before sending.");
        return;
      }
      var rangeForAnnotation = pendingRange ? pendingRange.cloneRange() : null;
      var selectedText = pendingText;
      window
        .fetch(feedbackUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            sample_index: Number(answer.dataset.sampleIndex),
            selected_text: selectedText,
            comment: comment,
          }),
        })
        .then(function (response) {
          return response.json().then(function (data) {
            return { ok: response.ok, data: data };
          });
        })
        .then(function (result) {
          if (!result.ok) {
            showError((result.data && result.data.error) || "Could not save feedback.");
            return;
          }
          appendFeedbackItem(result.data.feedback);
          if (rangeForAnnotation) {
            upsertAnnotation(
              result.data.feedback.feedback_id,
              selectedText,
              rangeForAnnotation
            );
          } else {
            // Fall back to text search if the live range was lost.
            var consumed = [];
            annotations.forEach(function (ann) {
              findNextRange(ann.selectedText, consumed);
            });
            var found = findNextRange(selectedText, consumed);
            if (found) {
              upsertAnnotation(result.data.feedback.feedback_id, selectedText, found);
            }
          }
          var selection = window.getSelection();
          if (selection) selection.removeAllRanges();
          hidePopup();
        })
        .catch(function () {
          showError("Could not save feedback.");
        });
    });

    // Delegated (not per-form) so it covers both the server-rendered items
    // present at load and ones appendFeedbackItem() clones in later; the
    // generic form[data-confirm] binding below skips #feedback-list to avoid
    // double-confirming the server-rendered ones.
    list.addEventListener("submit", function (event) {
      var form = event.target;
      if (!(form instanceof HTMLFormElement) || !form.hasAttribute("data-confirm")) return;
      event.preventDefault();
      if (!window.confirm(form.dataset.confirm || "Delete this item?")) return;
      var li = form.closest(".feedback-item");
      if (!li || !li.dataset.feedbackId) return;
      deleteFeedback(li.dataset.feedbackId, { skipConfirm: true });
    });

    window.addEventListener("resize", function () {
      window.requestAnimationFrame(relayoutAnnotations);
    });

    answer.addEventListener("scroll", function () {
      window.requestAnimationFrame(relayoutAnnotations);
    });

    var answerSection = answer.closest(".collapsible-section");
    if (answerSection) {
      var toggle = answerSection.querySelector(".collapsible-toggle");
      if (toggle) {
        toggle.addEventListener("click", function () {
          window.requestAnimationFrame(relayoutAnnotations);
        });
      }
    }

    hydrateAnnotations();
  })();

  document.querySelectorAll("form[data-confirm]").forEach(function (form) {
    if (form.closest("#feedback-list")) return;
    form.addEventListener("submit", function (event) {
      if (!window.confirm(form.dataset.confirm || "Delete this item?")) {
        event.preventDefault();
      }
    });
  });

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
