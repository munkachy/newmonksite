// St. Bernard Abbey: menu, hero video, the film player, today's Grotto hours and next prayer (Central time),
// and a gentle rise-in. Everything on the page is readable without this script.
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  document.documentElement.classList.add('js');
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- Menu (phones and tablets) ----
  var menuBtn = $('menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Menu');
    });
    document.querySelectorAll('#nav a').forEach(function (a) {
      a.addEventListener('click', function () { if (document.body.classList.contains('menu-open')) menuBtn.click(); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('menu-open')) { menuBtn.click(); menuBtn.focus(); }
    });
  }

  // ---- Hero video: a still for those who ask for less motion; a pause button for everyone ----
  var hv = $('hero-video'), hp = $('hero-pause');
  if (hv) {
    if (reduce) { hv.removeAttribute('autoplay'); hv.pause(); if (hp) hp.setAttribute('aria-pressed', 'true'); }
    if (hp) hp.addEventListener('click', function () {
      var paused = hp.getAttribute('aria-pressed') !== 'true';
      if (paused) hv.pause(); else hv.play().catch(function () {});
      hp.setAttribute('aria-pressed', paused ? 'true' : 'false');
      hp.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video');
    });
  }

  // ---- The film: plays in place, over its picture (as the virtual tour on stbernardprep) ----
  var fp = $('film-player'), fv = $('film-video'), fplay = $('film-play'), fclose = $('film-close');
  if (fp && fv && fplay) {
    fplay.addEventListener('click', function () {
      fp.hidden = false; if (hv) hv.pause();
      fv.play().catch(function () {}); if (fclose) fclose.focus();
    });
    if (fclose) fclose.addEventListener('click', function () { fv.pause(); fp.hidden = true; fplay.focus(); });
  }

  // ---- Today: Grotto hours and the next public prayer, in Cullman's time ----
  // Source: stbernardabbey.com/liturgy-schedule and avemariagrotto.com (1 Nov 2026). "Subject to change on feasts."
  var OFFICE = {
    weekday: [['Matins & Lauds', 360], ['Sext', 715], ['Mass', 1020], ['Vespers', 1050], ['Compline', 1155]],
    sat: [['Matins & Lauds', 360], ['Sext', 645], ['Mass', 660], ['Vespers', 1050], ['Compline', 1155]],
    sun: [['Matins & Lauds', 420], ['Sext', 600], ['Mass', 630], ['Solemn Vespers', 1050]]  // Compline not public
  };
  function central() {
    var p = {};
    new Intl.DateTimeFormat('en-US', { timeZone: 'America/Chicago', year: 'numeric', month: 'numeric', day: 'numeric',
      hour: 'numeric', minute: 'numeric', hourCycle: 'h23', weekday: 'short' })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    return { y: +p.year, m: +p.month, d: +p.day, wd: p.weekday, min: (+p.hour % 24) * 60 + (+p.minute) };
  }
  function easter(y) { // Gregorian computus
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4, f = Math.floor((b + 8) / 25),
      g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30, i = Math.floor(c / 4), k = c % 4,
      l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451);
    return [Math.floor((h + l - 7 * m + 114) / 31), ((h + l - 7 * m + 114) % 31) + 1];
  }
  function grottoClosed(t) {
    if ((t.m === 1 && t.d === 1) || (t.m === 7 && t.d === 4) || (t.m === 12 && t.d === 25)) return true;
    var e = easter(t.y); if (t.m === e[0] && t.d === e[1]) return true;
    return t.m === 11 && t.wd === 'Thu' && t.d >= 22 && t.d <= 28; // Thanksgiving
  }
  function clock(min) {
    var h = Math.floor(min / 60), mm = min % 60, ap = h >= 12 ? 'p.m.' : 'a.m.';
    h = h % 12 || 12; return h + (mm ? ':' + (mm < 10 ? '0' : '') + mm : '') + ' ' + ap;
  }
  function today() {
    var t = central(), list = t.wd === 'Sun' ? OFFICE.sun : t.wd === 'Sat' ? OFFICE.sat : OFFICE.weekday;
    if (t.wd === 'Wed') list = list.slice(0, 4); // Compline not public on Wednesdays
    var next = null, when = 'today';
    for (var i = 0; i < list.length; i++) if (list[i][1] > t.min) { next = list[i]; break; }
    if (!next) { next = (t.wd === 'Sat' ? OFFICE.sun : t.wd === 'Fri' ? OFFICE.sat : OFFICE.weekday)[0]; when = 'tomorrow'; }
    var open = t.wd === 'Sun' ? 690 : 540, close = 1020, g;
    if (grottoClosed(t)) g = 'The Grotto is closed today';
    else if (t.min < open) g = 'The Grotto opens today at ' + clock(open);
    else if (t.min < close) g = 'The Grotto is open until 5 p.m.';
    else g = 'The Grotto opens tomorrow at ' + (t.wd === 'Sat' ? '11:30 a.m.' : '9 a.m.');
    return { grotto: g, next: next[0], at: clock(next[1]), when: when };
  }
  function fill() {
    var n = today();
    [['util-grotto', n.grotto], ['now-grotto', n.grotto]].forEach(function (x) { var el = $(x[0]); if (el) el.textContent = x[1]; });
    var un = $('util-next'); if (un) un.innerHTML = 'Next prayer: <b></b>'; if (un) un.querySelector('b').textContent = n.next + ', ' + n.at + (n.when === 'tomorrow' ? ' tomorrow' : '');
    var nn = $('now-next'), nw = $('now-when');
    if (nn) nn.textContent = n.next; if (nw) nw.textContent = n.at + (n.when === 'tomorrow' ? ', tomorrow' : ', today');
  }
  try { fill(); setInterval(fill, 60000); } catch (e) { /* the static text stays */ }

  // ---- Rise-in: only when the reader allows motion; content is visible without it ----
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    document.querySelectorAll('.rise').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.rise').forEach(function (el) { el.classList.add('in'); });
  }
})();

// ---- Faces: click a small portrait to see the whole photograph ----
(function () {
  var faces = document.querySelectorAll('img[data-full]');
  if (!faces.length) return;
  var box = document.createElement('div');
  box.className = 'lightbox'; box.hidden = true;
  box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Photograph');
  box.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lightbox-close" aria-label="Close"><svg class="ic"><use href="#i-close"/></svg></button>';
  document.body.appendChild(box);
  var big = box.querySelector('img'), cap = box.querySelector('figcaption'), closeBtn = box.querySelector('button'), opener = null;
  function open(img) {
    opener = img; big.src = img.getAttribute('data-full'); big.alt = img.alt || '';
    cap.textContent = img.alt || ''; box.hidden = false; document.body.classList.add('menu-open'); closeBtn.focus();
  }
  function close() { box.hidden = true; big.src = ''; document.body.classList.remove('menu-open'); if (opener) opener.focus(); }
  faces.forEach(function (img) {
    img.addEventListener('click', function () { open(img); });
    img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(img); } });
  });
  box.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (!box.hidden && e.key === 'Escape') close(); });
})();
