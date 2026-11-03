// Site check: node _notes/tools/qa.js [page ...]   (pages like relics/ or index.html; default: every page)
// Serves the repo's parent folder locally and opens each page in Playwright at 1440 and 390 px wide. Reports sideways
// scroll, broken images (lazy images are forced to load), console/page errors, failed local requests, and every
// internal link, image and #anchor that does not resolve (checked on disk and against the ids of the target page).
// Exit code 1 if anything failed.
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const R = path.resolve(__dirname, '..', '..'), SITE = path.basename(R), PORT = 8771;
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.jpg': 'image/jpeg', '.png': 'image/png',
  '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webp': 'image/webp', '.ico': 'image/x-icon', '.json': 'application/json', '.vtt': 'text/vtt' };
function allPages(dir = R, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name.startsWith('_') || e.name.startsWith('.') || e.name === 'node_modules') continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) allPages(p, out); else if (e.name === 'index.html') out.push(path.relative(R, p));
  }
  return out.sort();
}
const cache = {};
function parse(file) {
  if (cache[file]) return cache[file];
  const t = fs.readFileSync(file, 'utf8'), ids = new Set(), links = [];
  for (const m of t.matchAll(/\s(?:id|name)="([^"]+)"/g)) ids.add(m[1]);
  for (const m of t.matchAll(/\s(?:href|src|data-full|poster)="([^"]*)"/g)) links.push(m[1]);
  for (const m of t.matchAll(/\ssrcset="([^"]*)"/g)) for (const s of m[1].split(',')) if (s.trim()) links.push(s.trim().split(/\s+/)[0]);
  return (cache[file] = { ids, links });
}
const unesc = s => s.replace(/&amp;/g, '&');
function checkLinks(rel) {
  const src = path.join(R, rel), base = path.dirname(src), bad = [];
  for (let href of parse(src).links) {
    href = unesc(href);
    if (!href || /^(https?:|mailto:|tel:|data:|javascript:|\/\/)/.test(href)) continue;
    const [p0, frag] = href.split('#'), p = decodeURIComponent(p0.split('?')[0]);
    let target = p ? path.normalize(path.join(base, p)) : src;
    if (!target.startsWith(R)) { bad.push('outside site ' + href); continue; }
    if (fs.existsSync(target) && fs.statSync(target).isDirectory()) target = path.join(target, 'index.html');
    if (!fs.existsSync(target)) { bad.push('missing ' + href); continue; }
    if (frag && target.endsWith('.html') && !parse(target).ids.has(decodeURIComponent(frag))) bad.push('no anchor ' + href);
  }
  return bad;
}
const srv = http.createServer((q, s) => {
  let p = decodeURIComponent(q.url.split('?')[0]); let f = path.join(path.dirname(R), p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!f.startsWith(path.dirname(R)) || !fs.existsSync(f)) { s.writeHead(404); return s.end(); }
  s.writeHead(200, { 'Content-Type': TYPES[path.extname(f).toLowerCase()] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(s);
});
(async () => {
  let todo = process.argv.slice(2).map(a => a.replace(/^\.\//, '')).map(a => a.endsWith('.html') ? a : (a.replace(/\/$/, '') + '/index.html').replace(/^\//, ''));
  if (!todo.length) todo = allPages();
  await new Promise(r => srv.listen(PORT, '127.0.0.1', r));
  const b = await chromium.launch(); let fails = 0, n = 0;
  for (const rel of todo) {
    const probs = checkLinks(rel); n += parse(path.join(R, rel)).links.length;
    for (const w of [1440, 390]) {
      const pg = await b.newPage({ viewport: { width: w, height: 900 } }), errs = [];
      pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
      pg.on('pageerror', e => errs.push(String(e)));
      pg.on('response', r => { if (r.status() >= 400 && r.url().includes('127.0.0.1')) errs.push(r.status() + ' ' + r.url()); });
      await pg.goto(`http://127.0.0.1:${PORT}/${SITE}/` + (rel === 'index.html' ? '' : rel.replace(/index\.html$/, '')), { waitUntil: 'load' });
      await pg.evaluate(async () => { for (const i of document.images) i.loading = 'eager';
        for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); });
      await pg.waitForLoadState('networkidle', { timeout: 20000 }).catch(() => {});
      await pg.evaluate(() => Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 8000); }))));
      const over = await pg.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      const broken = await pg.evaluate(() => [...document.images].filter(i => i.getAttribute('src') && i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src')));
      if (over > 0) probs.push(`${w}px: sideways scroll ${over}px`);
      broken.forEach(s => probs.push(`${w}px: broken image ${s}`));
      errs.forEach(e => probs.push(`${w}px: console ${e.slice(0, 160)}`));
      await pg.close();
    }
    const u = [...new Set(probs)]; if (u.length) fails++;
    console.log((u.length ? 'FAIL ' : 'ok   ') + rel); u.forEach(p => console.log('      ' + p));
  }
  await b.close(); srv.close();
  console.log(`${todo.length} pages, ${n} links/images checked, ${fails} with problems`);
  process.exit(fails ? 1 : 0);
})();
