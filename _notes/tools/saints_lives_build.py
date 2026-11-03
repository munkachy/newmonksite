#!/usr/bin/env python3
"""Build saints/index.html ("The saints of our reliquary") from _notes/saints-lives/part-*.json.

The page is a draft: nothing on the site links to it (all pages are noindex). Header and footer are copied from
relics/index.html so they stay in step with the rest of the site. Portraits: assets/img/saints/<id>.jpg if present.
Run from the repo root: python3 _notes/tools/saints_lives_build.py
"""
import glob, html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT)

entries = []
for path in sorted(glob.glob("_notes/saints-lives/part-*.json")):
    entries += json.load(open(path, encoding="utf-8"))
by_id = {e["id"]: e for e in entries}
assert len(by_id) == len(entries), "duplicate ids"

PATRONS = ["bernard-of-clairvaux", "benedict"]
HOLY = ["the-tomb-of-our-lord", "the-holy-nail", "the-holy-house-of-loreto", "the-tomb-of-our-lady", "our-ladys-garment"]
REST = [e["id"] for e in entries if e["id"] not in PATRONS + HOLY]

def sort_key(i):
    n = re.sub(r"^(Sts?\.|Bl\.|The|A)\s+", "", by_id[i]["name"])
    return n.lower()
REST.sort(key=sort_key)

def esc(s):
    return html.escape(s, quote=False)

def rich(s):
    """Escape, then let <em> through (the only markup the writers may use)."""
    return re.sub(r"&lt;(/?)em&gt;", r"<\1em>", esc(s))

def short(name):
    return re.sub(r"^(Sts?\.|Bl\.)\s+", "", name)

def card(e):
    i = e["id"]
    img = f"assets/img/saints/{i}.jpg"
    face = ""
    if os.path.exists(img):
        face = (f'<img class="saint-face life-face" src="../{img}" data-full="../assets/img/saints/full/{i}.jpg" '
                f'alt="{html.escape(e["name"])}" width="160" height="160" loading="lazy" tabindex="0" role="button">')
    meta = " · ".join(x for x in [e.get("dates", ""), e.get("title", ""),
                                  ("Feast: " + e["feast"]) if e.get("feast") else ""] if x)
    life = "".join(f"<p>{rich(p)}</p>" for p in e["life"])
    pats = "".join(f"<li>{rich(p)}</li>" for p in e.get("patronage", []))
    why = "".join(f"<p>{rich(p)}</p>" for p in e.get("why_here", []))
    check = (f'<p class="life-check"><span class="note-draft">To check</span> {rich(e["check"])}</p>'
             if e.get("check") else "")
    return f"""
<article class="life" id="{i}">
  <header class="life-head">{face}<div><h3 class="h-sm">{esc(e["name"])}</h3><p class="life-meta">{esc(meta)}</p></div></header>
  <div class="life-body">
    <div class="prose life-text">{life}</div>
    <aside class="life-side">
      <div class="life-box"><h4>Patron of</h4><ul role="list">{pats}</ul></div>
      <div class="life-box life-why"><h4>For our abbey and school</h4>{why}</div>
      <p class="life-relic"><b>In our reliquary.</b> {rich(e.get("relic", ""))}</p>
      {check}
    </aside>
  </div>
</article>"""

def chips(ids):
    return "".join(f'<li><a href="#{i}">{esc(short(by_id[i]["name"]))}</a></li>' for i in ids if i in by_id)

def section(ids, eyebrow, title, intro, stone=False):
    cards = "".join(card(by_id[i]) for i in ids if i in by_id)
    cls = "sec-tight on-stone" if stone else "sec-tight"
    return f"""
<section class="{cls}">
  <div class="wrap">
    <p class="eyebrow">{eyebrow}</p>
    <h2 class="h-md">{title}</h2>
    <p class="lives-intro">{intro}</p>
    {cards}
  </div>
</section>"""

STYLE = """<style>
/* saints/: The saints of our reliquary (draft page) */
.draft-bar { background: #fff3c4; color: #5c4700; font-size: .95rem; padding: .7rem 0; }
.lives-index { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: 1.2rem; }
.lives-index a { display: inline-block; font-size: .88rem; padding: .25rem .65rem; border: 1px solid var(--line);
  border-radius: 999px; background: var(--paper); text-decoration: none; }
.lives-index a:hover { border-color: var(--gold-ink); }
.lives-intro { max-width: 46rem; margin-top: 1rem; color: var(--ink-soft); }
.life { border-top: 1px solid var(--line); padding-block: 2.6rem; scroll-margin-top: 5rem; }
.life:first-of-type { margin-top: 2rem; }
.life-head { display: flex; align-items: center; gap: 1.1rem; }
.life-face { width: 5.2rem; height: 5.2rem; border-radius: 50%; object-fit: cover; flex: none; cursor: zoom-in; }
.life-head h3 { font-size: clamp(1.7rem, 2.6vw, 2.2rem); }
.life-meta { font-size: .92rem; color: var(--muted); margin-top: .35rem; }
.life-body { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: clamp(1.5rem, 4vw, 3.5rem);
  margin-top: 1.4rem; align-items: start; }
.life-text { max-width: 44rem; }
.life-side { display: grid; gap: 1rem; }
.life-box { background: var(--paper-2); border-radius: 4px; padding: 1.1rem 1.25rem; }
.on-stone .life-box { background: var(--paper); }
.life-box h4 { font: 600 .74rem/1.2 var(--sans); letter-spacing: .16em; text-transform: uppercase; color: var(--gold-ink);
  margin-bottom: .6rem; }
.life-box ul { display: grid; gap: .25rem; font-size: .98rem; }
.life-box li { padding-left: 1rem; position: relative; }
.life-box li::before { content: ""; position: absolute; left: 0; top: .72em; width: .4rem; height: 1px; background: var(--gold-ink); }
.life-why { border-left: 3px solid var(--gold); }
.life-why p { font-size: 1rem; }
.life-why p + p { margin-top: .8em; }
.life-relic, .life-check { font-size: .92rem; color: var(--ink-soft); }
@media (max-width: 52em) { .life-body { grid-template-columns: 1fr; } .life-face { width: 4.2rem; height: 4.2rem; } }
</style>
"""

src = open("relics/index.html", encoding="utf-8").read()
head, rest = src.split('<main id="main">', 1)
foot = rest.split("</main>", 1)[1]
head = head.replace("<title>The Relics · St. Bernard Abbey</title>", "<title>The Saints of Our Reliquary · St. Bernard Abbey</title>")
head = head.replace('href="https://www.stbernardabbey.com/relics/"', 'href="https://www.stbernardabbey.com/saints/"')
head = head.replace("</head>", STYLE + "</head>")

n = len(entries)
main = f"""<main id="main">
<div class="draft-bar"><div class="wrap"><b>Draft.</b> This page is not linked from anywhere on the site yet. Notes marked <span class="note-draft">To check</span> are for review before it goes public.</div></div>
<section class="page-hero">
  <img src="../assets/img/relics/board.jpg" alt="" width="1200" height="900">
  <div class="wrap">
    <p class="eyebrow">The saints of our reliquary</p>
    <h1 class="h-xl">Their lives, their patronage, their prayers for us</h1>
    <p class="lead">Every saint whose relic the abbey keeps: who they were, what the Church asks them to watch over, and why their prayers matter to the monks of St. Bernard and to the students and families of St. Bernard Prep.</p>
  </div>
</section>

<section class="sec-tight">
  <div class="wrap prose" style="max-width:52rem">
    <p class="eyebrow">How to read this page</p>
    <h2 class="h-md">History, legend and prayer</h2>
    <p style="margin-top:1.2rem">Some of these saints we know from their own letters; others only from stories written down centuries after they died. Each life says plainly which is which. A saint's patronage is the care the Church, or long custom, has given to him or her: some were declared by a pope, most grew from the saint's own life. We ask the saints to pray for us as we ask one another, because "the union of the wayfarers with the brethren who sleep in the peace of Christ is in no way interrupted" (Catechism, no. 955).</p>
    <p>Where a label names a saint but not which one (a St. Agapitus, a St. Innocent), the entry says so. The readings of the labels come from the catalogue of the relics; the relics themselves are described on <a href="../relics/">the relics page</a>.</p>
    <p class="small">{n} entries.</p>
  </div>
  <div class="wrap">
    <nav aria-label="Saints on this page"><ul class="lives-index" role="list">{chips(PATRONS + HOLY + REST)}</ul></nav>
  </div>
</section>
{section(PATRONS, "Our patrons", "St. Bernard and St. Benedict", "The abbey and the school bear St. Bernard's name; every monk here lives by St. Benedict's Rule. The abbey keeps four relics of the one and two of the other.", stone=True)}
{section(HOLY, "Our Lord and Our Lady", "Relics of holy places", "Not relics of bodies, but of the places and things of the Gospel: stone, cloth and iron touched to the story of our salvation.")}
{section(REST, "The saints, A to Z", "Apostles, martyrs, monks, kings and children", "In alphabetical order. Tap a portrait to see it whole.", stone=True)}
</main>"""

os.makedirs("saints", exist_ok=True)
open("saints/index.html", "w", encoding="utf-8").write(head + main + foot)
print("wrote saints/index.html:", n, "entries")
