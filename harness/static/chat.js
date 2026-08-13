/* Chat UI behavior: quote-reply from a text selection, and transcript polling.
 *
 * The selection flow is deliberately shallow. Selecting text in a response and
 * hitting "Quote & reply" copies that span into the composer as a quote chip —
 * it does not create an annotation. Nothing is stored until the message is
 * sent, and what gets stored is part of the next question. That is why there is
 * no highlight layer, no gutter markers, and no re-anchoring logic here: there
 * is nothing to find again on reload.
 */
(function () {
  "use strict";

  var thread = document.querySelector(".chat-thread");
  if (!thread) return;

  // ---- Quote-reply --------------------------------------------------------

  var popup = document.getElementById("quote-popup");
  var popupButton = document.getElementById("quote-popup-button");
  var quoteBox = document.getElementById("composer-quote");
  var quoteText = document.getElementById("composer-quote-text");
  var quoteClear = document.getElementById("composer-quote-clear");
  var quotedField = document.getElementById("composer-quoted-text");
  var quotedRunField = document.getElementById("composer-quoted-run-id");
  var input = document.getElementById("composer-input");
  var composer = document.getElementById("composer");

  // The selection we'd quote if the button were pressed. Captured on
  // selectionchange because clicking the button collapses the selection.
  var candidate = null;

  function answerFor(node) {
    var el = node && node.nodeType === Node.TEXT_NODE ? node.parentElement : node;
    return el && el.closest ? el.closest(".chat-answer") : null;
  }

  function hidePopup() {
    if (popup) popup.hidden = true;
  }

  function showPopupAt(rect) {
    if (!popup) return;
    popup.hidden = false;
    // Above the selection, clamped into the viewport. Measured after unhiding
    // so offsetWidth/Height are real.
    var top = rect.top + window.scrollY - popup.offsetHeight - 8;
    var left = rect.left + window.scrollX + rect.width / 2 - popup.offsetWidth / 2;
    var maxLeft = window.scrollX + document.documentElement.clientWidth - popup.offsetWidth - 8;
    if (top < window.scrollY + 8) top = rect.bottom + window.scrollY + 8;
    popup.style.top = top + "px";
    popup.style.left = Math.max(window.scrollX + 8, Math.min(left, maxLeft)) + "px";
  }

  document.addEventListener("selectionchange", function () {
    var selection = window.getSelection();
    if (!selection || selection.isCollapsed || selection.rangeCount === 0) {
      candidate = null;
      hidePopup();
      return;
    }
    var range = selection.getRangeAt(0);
    var start = answerFor(range.startContainer);
    // Only offer to quote a selection that stays inside one response.
    if (!start || start !== answerFor(range.endContainer)) {
      candidate = null;
      hidePopup();
      return;
    }
    var text = selection.toString().replace(/\s+/g, " ").trim();
    if (!text) {
      candidate = null;
      hidePopup();
      return;
    }
    candidate = { text: text, runId: start.dataset.runId || "" };
    showPopupAt(range.getBoundingClientRect());
  });

  function setQuote(text, runId) {
    if (!quotedField || !quoteBox) return;
    quotedField.value = text;
    if (quotedRunField) quotedRunField.value = runId || "";
    quoteText.textContent = text;
    quoteBox.hidden = false;
    if (input) input.focus();
  }

  function clearQuote() {
    if (!quotedField || !quoteBox) return;
    quotedField.value = "";
    if (quotedRunField) quotedRunField.value = "";
    quoteText.textContent = "";
    quoteBox.hidden = true;
  }

  if (popupButton) {
    popupButton.addEventListener("click", function () {
      if (!candidate) return;
      setQuote(candidate.text, candidate.runId);
      hidePopup();
      var selection = window.getSelection();
      if (selection) selection.removeAllRanges();
      candidate = null;
    });
  }

  if (quoteClear) quoteClear.addEventListener("click", clearQuote);

  // Don't leave the popup floating over content it no longer refers to.
  window.addEventListener("scroll", hidePopup, { passive: true });
  window.addEventListener("resize", hidePopup);

  // ---- Composer -----------------------------------------------------------

  if (input && composer) {
    input.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" || event.shiftKey) return;
      // Enter sends; Shift+Enter is a newline. requestSubmit so `required`
      // validation still runs.
      event.preventDefault();
      if (input.value.trim()) composer.requestSubmit();
    });
  }

  if (composer) {
    composer.addEventListener("submit", function () {
      var button = composer.querySelector(".composer-send");
      if (button) button.disabled = true;
      if (input) input.readOnly = true;
    });
  }

  // ---- Polling ------------------------------------------------------------
  //
  // Runs go through the harness task queue, so a turn appears as "Thinking…"
  // until its worker finishes. Poll a chat-scoped endpoint (NOT the harness's
  // /tasks/<id>/status, which would hand a user session the prompt version) and
  // reload when the answered count changes or the queue drains.

  var statusUrl = thread.dataset.statusUrl;
  var pendingAtLoad = parseInt(thread.dataset.pending || "0", 10);
  var hasPendingTurn = document.querySelector("[data-turn-pending]") !== null;
  if (!statusUrl || (!pendingAtLoad && !hasPendingTurn)) return;

  var POLL_MS = 2000;
  var MAX_POLLS = 450; // ~15 minutes, then stop rather than poll forever
  var polls = 0;
  var answeredAtLoad = null;

  function showTurnFailed(hadFailure) {
    var pending = document.querySelector("[data-turn-pending]");
    if (!pending) return;
    pending.classList.remove("is-pending");
    pending.classList.add("is-failed");
    pending.textContent = hadFailure
      ? "This turn didn't complete — the run failed. Check the worker log, then reload."
      : "This turn didn't complete, and nothing is queued for it. Reload to check again.";
  }

  function poll() {
    if (polls++ > MAX_POLLS) return;
    window
      .fetch(statusUrl, { headers: { "X-Requested-With": "XMLHttpRequest" } })
      .then(function (response) {
        if (!response.ok) throw new Error("status " + response.status);
        return response.json();
      })
      .then(function (data) {
        if (answeredAtLoad === null) answeredAtLoad = data.answered;

        // A new answer landed: reload to render it.
        if (data.answered > answeredAtLoad) {
          window.location.reload();
          return;
        }

        // Nothing queued, but a turn is still unanswered — the run failed (or a
        // worker died holding it). Say so and STOP. Reloading here would spin
        // forever: the reloaded page sees the same unanswered turn and the same
        // empty queue, and asks again.
        if (data.pending === 0 && hasPendingTurn) {
          showTurnFailed(data.failed > 0);
          return;
        }

        var thinking = document.querySelector(".turn-thinking");
        if (thinking && data.messages && data.messages.length) {
          thinking.textContent = data.messages[0];
        }
        window.setTimeout(poll, POLL_MS);
      })
      .catch(function () {
        // Transient failure (worker restart, dropped connection): back off
        // rather than giving up on the turn.
        window.setTimeout(poll, POLL_MS * 2);
      });
  }

  window.setTimeout(poll, POLL_MS);
})();
