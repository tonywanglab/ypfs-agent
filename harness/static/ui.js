(function () {
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
})();
