"""Writes the 'Oldest Conversation pages' block at the end of assets/site.css from the source site's CSS (see swu_import.py):
    python3 _notes/tools/swu_css.py /tmp/swu
Rules for the classes swu_import.py renames to sw-NAME are copied, scoped under .swu, with the source's theme variables
mapped to the abbey's navy, gold and white. Re-run after the source CSS changes; it replaces its own block."""
import re, sys
SRC = open(sys.argv[1] + "/assets/css/site.css").read()
R = __file__.rsplit("/_notes/", 1)[0]
NAMES = ("ask q choices choice reply if big primer inner qa tip tip-badge tip-q tip-more quote quote-badge quote-who quote-more call num mood mood-picker "
         "mood-grid mood-chip mood-word mood-ps back-to-moods setting label-meditation exchange psalm heard voice voice-img said who monk god tagline ornament "
         "note callout art book-scan side-links what intro dropcap freely freely-q freely-ref join-row sorrow joy trust mercy skip-questions suggested portrait").split()
KEEP = re.compile(r"(?<![\w-])\.(" + "|".join(sorted(map(re.escape, NAMES), key=len, reverse=True)) + r")(?![\w-])")
src = re.sub(r"/\*.*?\*/", "", SRC, flags=re.S)

def rules(css):
    i = 0; out = []
    while i < len(css):
        j = css.index("{", i) if "{" in css[i:] else None
        if j is None: break
        sel = css[i:j].strip(); depth = 1; k = j + 1
        while depth and k < len(css):
            depth += (css[k] == "{") - (css[k] == "}"); k += 1
        out.append((sel, css[j + 1:k - 1])); i = k
    return out

def conv(sel):
    parts = []
    for p in sel.split(","):
        p = p.strip()
        if "[data-theme" in p or ".review" in p or ":root" in p or p.startswith(("body", "html")) or "rv" in p.split(): continue
        if not KEEP.search(p): continue
        parts.append(".swu " + KEEP.sub(lambda m: ".sw-" + m.group(1), p))
    return ", ".join(parts)

def fix(body):
    body = body.replace('"Cinzel", serif', "var(--serif)")
    return body

blocks = []
for sel, body in rules(src):
    if sel.startswith("@media"):
        inner = []
        for s2, b2 in rules(body):
            c = conv(s2)
            if c: inner.append(f"  {c} {{{fix(b2)}}}")
        if inner: blocks.append(f"{sel} {{\n" + "\n".join(inner) + "\n}")
    elif not sel.startswith("@"):
        c = conv(sel)
        if c: blocks.append(f"{c} {{{fix(body)}}}")

HEAD = """
/* ===== Oldest Conversation pages (pray/curious, christians, catholics, psalms, choir-book, quotes): made by _notes/tools/swu_css.py ===== */
.swu { --surface: #fff; --rule: rgba(0,64,105,.2); --accent: var(--blue); --accent-2: var(--gold); --muted: var(--slate); --text: var(--ink); --heard: #1d4a6a;
  --bg-2: var(--mist); --card-shadow: 0 14px 30px -22px rgba(1,37,61,.45); --jewel-1: var(--blue); --jewel-2: #8a4b4b; --jewel-3: var(--steel); --jewel-4: #7a6a1f; --link: var(--blue); --accent-ink: #fefefe; }
.swu .wrap { width: min(46rem, 100% - 2 * var(--gut)); }
.swu .wrap-wide { width: min(64rem, 100% - 2 * var(--gut)); }
.swu { padding-block: clamp(2.5rem, 6vw, 4.5rem); font-size: 1.1rem; }
.swu h2 { font: 400 clamp(1.5rem, 2.6vw, 2rem)/1.25 var(--serif); color: var(--blue); margin: 2.6rem 0 1rem; }
.swu h3 { font: 400 1.3rem/1.3 var(--serif); color: var(--blue); }
.swu p { margin: 0 0 1.1rem; }
.swu a { color: var(--blue); text-decoration-color: var(--gold); }
.swu .btn { text-decoration: none; }
.swu .btn-ink { color: #fefefe; }
.swu .btn-line { color: var(--blue); }
.swu .btn-row { margin-top: 1.4rem; }
.swu img { max-width: 100%; height: auto; }
.swu .sw-art img, .swu .sw-book-scan img { width: 100%; }
.swu figure { margin: 2rem 0; }
.swu figcaption { font-size: .92rem; color: var(--slate); margin-top: .6rem; }
.swu blockquote { margin: 1.4rem 0; padding: .2rem 0 .2rem 1.2rem; border-left: 3px solid var(--gold); }
.swu blockquote footer, .swu .cite { font-size: .92rem; color: var(--slate); }
.swu .sw-psalm { font-family: var(--italic); font-style: italic; }
.swu .sw-psalm p { font-size: 1.2rem; }
.swu .sw-ask, .swu .sw-call, .swu .sw-tip, .swu .sw-quote { border-top: 3px solid var(--blue); border-radius: 0; }
.swu .sw-choice { border-radius: 2px; font: 600 .78rem/1.3 var(--sans); letter-spacing: .14em; text-transform: uppercase; color: var(--blue); border-color: rgba(0,64,105,.3); }
.swu .sw-choice[aria-pressed="true"] { background: var(--blue); color: #fefefe; border-color: var(--blue); }
.swu .sw-q { font-family: var(--serif); font-weight: 400; color: var(--blue); }
.swu details.sw-primer, .swu details.sw-qa { border-radius: 0; }
.swu details.sw-primer.sw-suggested { border-left: 3px solid var(--gold); }
.swu .sw-ornament::before { content: ""; display: block; width: 1.8rem; height: 1.9rem; margin: 0 auto; background: url("img/brand/cross-light.svg") center / contain no-repeat; }
.swu .sw-ornament { letter-spacing: 0; }
.swu .sw-callout { border-left: 3px solid var(--gold); }
.credit { font-size: .82rem; color: var(--slate); margin: .7rem 0 0; }
.swu-back { padding-bottom: clamp(2rem, 5vw, 4rem); }
.page-hero-plain { min-height: 16rem; background: var(--grad); }
.page-hero-plain::before { display: none; }
"""
css = open(R + "/assets/site.css").read()
css = re.sub(r"\n/\* ===== Oldest Conversation pages.*\Z", "\n", css, flags=re.S)
marker, rest = HEAD.split("\n.swu .wrap {", 1)
open(R + "/assets/site.css", "w").write(css.rstrip("\n") + "\n" + marker + "\n" + "\n".join(blocks) + "\n.swu .wrap {" + rest)
print(len(blocks), "rules")
