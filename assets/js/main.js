/* =============================================================
   Campus & Chaos
   Lightbox, and a couple of small niceties.
   No dependencies, no trackers.
   ============================================================= */

(function () {
  "use strict";

  /* ---------------------------------------------------------
     Lightbox — click any photo marked data-full to enlarge it.
     --------------------------------------------------------- */
  var box = document.getElementById("lightbox");
  if (box) {
    var boxImg = box.querySelector(".lightbox__img");
    var boxCap = box.querySelector(".lightbox__cap");
    var closeBtn = box.querySelector(".lightbox__close");
    var lastFocused = null;

    function open(src, caption, alt) {
      boxImg.src = src;
      boxImg.alt = alt || "";
      boxCap.textContent = caption || "";
      boxCap.hidden = !caption;
      box.dataset.open = "true";
      document.body.style.overflow = "hidden";
      lastFocused = document.activeElement;
      closeBtn.focus();
    }

    function close() {
      box.dataset.open = "false";
      boxImg.src = "";
      boxImg.alt = "";
      boxCap.textContent = "";
      document.body.style.overflow = "";
      if (lastFocused) lastFocused.focus();
    }

    document.addEventListener("click", function (e) {
      var trigger = e.target.closest("[data-full]");
      if (trigger) {
        e.preventDefault();
        // Pull the caption from the polaroid print or the surrounding card
        var print = trigger.closest(".polaroid");
        var capEl = print ? print.querySelector(".polaroid__cap") : null;
        var card = trigger.closest(".card");
        var capText = capEl
          ? capEl.textContent.trim()
          : card && card.querySelector(".card__title")
            ? card.querySelector(".card__title").textContent.trim()
            : "";
        open(trigger.dataset.full, capText, trigger.alt);
        return;
      }
      if (e.target === box || e.target.closest(".lightbox__close")) close();
    });

    document.addEventListener("keydown", function (e) {
      if (box.dataset.open !== "true") return;
      if (e.key === "Escape") close();
      if (e.key === "Tab") {
        // Only the close button is focusable while open
        e.preventDefault();
        closeBtn.focus();
      }
    });
  }

  /* ---------------------------------------------------------
     Fade sections in as they scroll into view.
     Purely decorative — content is visible without it.
     --------------------------------------------------------- */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (!reduceMotion && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".chapter-block, .cover, .contribute");
    var seen = new WeakSet();

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting || seen.has(entry.target)) return;
          seen.add(entry.target);
          entry.target.classList.add("fade-in");
          io.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.04 }
    );

    targets.forEach(function (el) { io.observe(el); });
  }
})();