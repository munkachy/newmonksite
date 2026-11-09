/* "Suggest a change": a floating button for the monks, Fr. Paschal and anyone who wants to give feedback.
   It takes a picture of what the person is looking at, then sends their note and the picture to a small function that
   opens an issue on GitHub (munkachy/newmonksite, label "suggestion"). Set the function's address in ENDPOINT
   (or window.SUGGEST_URL); with no address the button does not appear. The function is a Google Apps Script (_notes/suggest/suggest.gs). Setup: _notes/suggest/README.md. */
(function () {
  "use strict";
  var ENDPOINT = "";
  var URL_ = window.SUGGEST_URL || ENDPOINT;
  if (!URL_) return;
  var H2C = "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
  var shot = null, shotP = null;

  function el(tag, attrs, html) { var e = document.createElement(tag); for (var k in attrs || {}) e.setAttribute(k, attrs[k]); if (html != null) e.innerHTML = html; return e; }
  function loadScript(src) {
    return new Promise(function (ok, no) {
      if (window.html2canvas) return ok();
      var s = el("script", { src: src }); s.onload = ok; s.onerror = no; document.head.appendChild(s);
    });
  }
  function capture() {
    // the picture is taken before the box opens, so it shows the page as the person saw it
    return loadScript(H2C).then(function () {
      var w = window.innerWidth, h = window.innerHeight;
      return window.html2canvas(document.documentElement, {
        x: window.scrollX, y: window.scrollY, scrollX: 0, scrollY: 0, width: w, height: h, windowWidth: document.documentElement.clientWidth,
        scale: Math.min(1, 1100 / w) , useCORS: true, logging: false, backgroundColor: "#ffffff",
        ignoreElements: function (n) { return n.hasAttribute && n.hasAttribute("data-suggest-ui"); }
      });
    }).then(function (c) { return c.toDataURL("image/jpeg", 0.72); });
  }

  var btn = el("button", { type: "button", class: "suggest-btn", "data-suggest-ui": "", "aria-haspopup": "dialog" },
    '<svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg><span>Suggest a change</span>');
  var dlg = el("dialog", { class: "suggest-dlg", "data-suggest-ui": "", "aria-labelledby": "sg-h" });
  dlg.innerHTML =
    '<form method="dialog" class="sg-form" novalidate>' +
    '<h2 id="sg-h">Suggest a change</h2>' +
    '<p class="sg-lead">Tell us what to fix, add or reword on this page. We attach a picture of what you were looking at.</p>' +
    '<label class="sg-l" for="sg-msg">What would you change?</label>' +
    '<textarea id="sg-msg" name="message" rows="5" maxlength="4000" required placeholder="For example: the opening line should say…"></textarea>' +
    '<label class="sg-l" for="sg-name">Your name (optional)</label>' +
    '<input id="sg-name" name="name" maxlength="100" autocomplete="name">' +
    '<input class="sg-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
    '<label class="sg-check"><input type="checkbox" id="sg-shot" checked> <span>Include a picture of this page</span></label>' +
    '<div class="sg-prev" id="sg-prev" aria-live="polite"></div>' +
    '<p class="sg-msg" id="sg-status" role="status"></p>' +
    '<div class="sg-row"><button type="button" class="sg-cancel" id="sg-cancel">Cancel</button><button type="submit" class="sg-send" id="sg-send">Send</button></div>' +
    '</form>';
  document.body.appendChild(btn); document.body.appendChild(dlg);
  var $ = function (id) { return dlg.querySelector("#" + id); };

  btn.addEventListener("click", function () {
    shot = null; $("sg-prev").innerHTML = ""; $("sg-status").textContent = ""; $("sg-msg").value = "";
    shotP = capture().then(function (d) { shot = d; return d; }, function () { return null; });
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    $("sg-prev").textContent = "Taking a picture…";
    shotP.then(function (d) {
      $("sg-prev").innerHTML = d ? '<img alt="The picture that will be sent" src="' + d + '">' : "No picture could be taken. Your note will still be sent.";
    });
    setTimeout(function () { $("sg-msg").focus(); }, 50);
  });
  $("sg-cancel").addEventListener("click", function () { dlg.close ? dlg.close() : dlg.removeAttribute("open"); });
  $("sg-shot").addEventListener("change", function () { $("sg-prev").style.display = this.checked ? "" : "none"; });

  dlg.querySelector("form").addEventListener("submit", function (e) {
    e.preventDefault();
    var msg = $("sg-msg").value.trim(), st = $("sg-status"), send = $("sg-send");
    if (msg.length < 3) { st.textContent = "Please write a few words first."; return; }
    send.disabled = true; st.textContent = "Sending…";
    Promise.resolve(shotP).then(function (d) {
      var body = {
        message: msg, name: $("sg-name").value.trim(), website: dlg.querySelector(".sg-hp").value,
        page: location.href, title: document.title, viewport: window.innerWidth + "x" + window.innerHeight,
        scroll: Math.round(window.scrollY), agent: navigator.userAgent, screenshot: $("sg-shot").checked ? d : null
      };
      return fetch(URL_, { method: "POST", headers: { "Content-Type": "text/plain" }, body: JSON.stringify(body) });
    }).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok || !j.ok) throw new Error(j.error || r.status); return j; }); })
      .then(function () {
        st.textContent = "Thank you. Your suggestion was sent.";
        $("sg-msg").value = ""; setTimeout(function () { dlg.close ? dlg.close() : dlg.removeAttribute("open"); send.disabled = false; }, 1600);
      })
      .catch(function () { st.textContent = "Sorry, that did not send. Please try again in a minute."; send.disabled = false; });
  });
})();
