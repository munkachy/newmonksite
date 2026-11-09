/* Oldest Conversation pages: questions that answer one at a time, the explanations that open for you, links into hidden parts.
   Without JavaScript the whole page simply shows. */
(function () {
  "use strict";
  var $ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  $("[data-after]").forEach(function (el) { el.hidden = true; });
  $(".sw-ask .sw-reply").forEach(function (el) { el.hidden = true; el.setAttribute("tabindex", "-1"); });
  function reveal(id) { $('[data-after="' + id + '"]').forEach(function (el) { el.hidden = false; }); }
  $(".sw-ask").forEach(function (ask) {
    $(".sw-choice", ask).forEach(function (btn) {
      btn.addEventListener("click", function () {
        $(".sw-choice", ask).forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
        btn.setAttribute("aria-pressed", "true");
        $(".sw-reply", ask).forEach(function (r) { r.hidden = true; });
        var target = document.getElementById(btn.getAttribute("data-reply"));
        if (target) { target.hidden = false; target.focus({ preventScroll: true }); }
        (btn.getAttribute("data-open") || "").split(/\s+/).forEach(function (pid) {
          var p = pid && document.getElementById(pid);
          if (p) { p.classList.add("sw-suggested"); p.open = true; }
        });
        if (ask.id) reveal(ask.id);
        if (target && target.scrollIntoView) {
          var r = target.getBoundingClientRect();
          if (r.bottom > window.innerHeight) target.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      });
    });
  });
  $(".sw-skip-questions").forEach(function (a) {
    a.addEventListener("click", function (e) {
      e.preventDefault();
      $("[data-after]").forEach(function (el) { el.hidden = false; });
      var to = document.querySelector(a.getAttribute("href"));
      if (to) to.scrollIntoView({ behavior: "smooth" });
    });
  });
  function showHash() {
    if (!location.hash) return;
    var el = document.getElementById(location.hash.slice(1));
    while (el && el !== document.body) {
      if (el.hidden) el.hidden = false;
      if (el.tagName === "DETAILS") el.open = true;
      el = el.parentElement;
    }
  }
  window.addEventListener("hashchange", showHash);
  showHash();
})();
