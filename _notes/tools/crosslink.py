"""Weave the site together: run after changing any page.

    python3 _notes/tools/crosslink.py

1. Inline links: in each page's <main>, the first plain mention of a term in TERMS becomes a link to its page or
   section (never inside a link, heading, button, caption, eyebrow or credit; never to the page itself; skipped when
   the page already links there). Links it adds carry class "xl", so a rerun first removes them and starts fresh.
2. "Wander further": a row of four related pages at the end of each page's <main> (WANDER), replaced on each run.
The main menu stays short (The Grotto, The School, Pray with Us, Visit, Give); these links let people wander.
"""
import html, os, re

R = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PAGES = ["index.html", "monastery/index.html", "work/index.html", "school/index.html", "grotto/index.html",
         "pray/index.html", "visit/index.html", "give/index.html", "history/index.html", "relics/index.html"]

TERMS = [  # (pattern, target from site root); first match per page wins
    (r"Ave Maria Grotto", "grotto/"),
    (r"Br\. Joseph Zoettl", "grotto/"),
    (r"Abbey Church", "pray/#church"),
    (r"Divine Office", "pray/#office"),
    (r"Liturgy of the Hours", "pray/#office"),
    (r"lectio divina", "pray/#lectio"),
    (r"\brelics\b", "relics/"),
    (r"monks' cemetery|\bcemetery\b", "visit/#cemetery"),
    (r"St\. Boniface Retreat Center|Retreat Center|Boniface Hall", "visit/#retreats"),
    (r"St\. Bernard Prep(?:aratory School)?", "school/"),
    (r"\boblates?\b", "monastery/#oblates"),
    (r"\bnovices\b|\bnovitiate\b", "monastery/#vocations"),
    (r"abbey farm|\bthe farm\b", "work/#farm"),
    (r"\bbakery\b", "work/#bakery"),
    (r"Metten Abbey|\bMetten\b", "history/"),
    (r"Mother Angelica|Pope Francis|Robert F\. Kennedy", "monastery/#wider-church"),
    (r"Herbert Jogerst", "pray/#church"),
    (r"\bCompline\b|\bVespers\b|\bMatins\b|\bLauds\b", "pray/#schedule"),
    (r"Abbot Brendan(?: Seipel)?", "monastery/#monks"),
    (r"Bloomin['’] Festival", "visit/#festivals"),
    (r"Br\. Jude\b", "work/#jude"),
    (r"Br\. Leo\b", "work/#leo"),
    (r"Fr\. Urban Tracy|Frater Hubert|Fr\. Edward Markley", "work/#heroes"),
    (r"Br\. Wolfgang", "work/#scribes"),
    (r"St\. Vincent Abbey|Boniface Wimmer", "history/"),
    (r"Mass for someone|offer Mass", "give/#masses"),
    (r"\bthe Psalms\b", "pray/#psalms"),
    (r"\bBavaria(?:n)?\b|\b1891\b", "history/"),
    (r"Rule of St\. Benedict|\bthe Rule\b", "monastery/#about"),
    (r"\bthe monks\b", "monastery/#monks"),
    (r"\bvocations?\b", "monastery/#vocations"),
    (r"\bheroes\b", "work/#heroes"),
    (r"\bscribes\b|\bscholars\b", "work/#scribes"),
    (r"\bcraftsmen\b|\bwith their own hands\b", "work/"),
    (r"\bpilgrims\b", "visit/"),
    (r"\bteachers\b", "school/#teachers-past"),
]

WANDER = {
    "monastery/index.html": [("history/", "A history in dates", "From Bavaria to Alabama: 135 years on this hill."),
                             ("work/#heroes", "Heroes", "Founders, chaplains under fire, men who gave everything."),
                             ("relics/#witnesses", "A great cloud of witnesses", "The saints, and our brothers in the cemetery."),
                             ("pray/#begin", "Where are you starting from?", "Curious, Christian or Catholic: a door for you.")],
    "work/index.html": [("grotto/", "The Ave Maria Grotto", "Br. Joseph's 125 miniatures of the world's holy places."),
                        ("school/#teachers-past", "Teachers of the past", "Monks who taught generations on this hill."),
                        ("monastery/#monks", "The monks today", "Meet the men who pray and work here now."),
                        ("history/", "A history in dates", "Every builder, baker and scribe in his time.")],
    "school/index.html": [("monastery/#monks", "Meet the monks", "The men behind the classroom doors."),
                          ("work/#scribes", "Scribes and scholars", "Scientists, writers and men of learning."),
                          ("history/", "A history in dates", "A school since 1892: college, seminary, prep."),
                          ("pray/#schedule", "The bells", "The hours of prayer the students hear each day.")],
    "grotto/index.html": [("work/#builders", "The builders", "Br. Joseph was not the only monk who built."),
                          ("visit/#cemetery", "Where Br. Joseph rests", "The monks' cemetery, near the Grotto."),
                          ("relics/", "The relics", "More than a hundred saints in the Abbey Church."),
                          ("pray/#psalms", "What kind of day are you having?", "A monk's conversations with God in the Psalms.")],
    "pray/index.html": [("relics/", "The relics", "The saints who keep us company in the Abbey Church."),
                        ("monastery/#day", "A day in the life", "From the Grand Silence to the holy water."),
                        ("monastery/#vocations", "Called to be a monk?", "The stages of the habit, from postulant to solemn vows."),
                        ("monastery/#oblates", "Oblates", "Living the Rule of St. Benedict in the world.")],
    "visit/index.html": [("grotto/", "The Ave Maria Grotto", "Four acres of miniature shrines."),
                         ("pray/#church", "The Abbey Church", "Plain stone outside, soaring arches within."),
                         ("relics/", "The relics", "Apostles, martyrs and saints of our own century."),
                         ("pray/#begin", "Where are you starting from?", "A door for the curious, Christians and Catholics.")],
    "give/index.html": [("monastery/#monks", "The monks", "The community your gift supports."),
                        ("school/", "The School", "Teaching on this hill since 1892."),
                        ("grotto/", "The Grotto", "Br. Joseph's work, kept for the next century."),
                        ("pray/#intentions", "Your intentions", "The monks pray daily for those who ask.")],
    "history/index.html": [("monastery/#wider-church", "A small abbey, in good company", "Popes, Mother Angelica and a Kennedy."),
                           ("work/#heroes", "Heroes", "The men behind the dates."),
                           ("school/#teachers-past", "Teachers of the past", "Generations of monks in the classroom."),
                           ("relics/#witnesses", "A great cloud of witnesses", "Our brothers who rest in the cemetery.")],
    "relics/index.html": [("pray/#church", "The Abbey Church", "Where the relics are kept."),
                          ("visit/#cemetery", "The cemetery", "Where the monks of St. Bernard rest."),
                          ("work/#heroes", "Heroes", "Monks who stood on the shoulders of giants."),
                          ("pray/#psalms", "Pray the Psalms", "One monk's conversations with God.")],
}

SKIP_TAGS = {"a", "h1", "h2", "h3", "h4", "h5", "h6", "button", "figcaption", "cite", "label", "script", "style",
             "svg", "summary", "title", "blockquote", "table"}
SKIP_CLASS = re.compile(r'id="(?:now|util)-|class="[^"]*\b(eyebrow|credit|monk-meta|monk-role|btn|pick|picks|reply|psalm-verse|voice|saints|wander)\b')
VOID = {"img", "br", "hr", "input", "meta", "link", "source", "use", "path", "wbr"}


def page_of(target):
    return target.split("#")[0] + "index.html" if not target.startswith("index") else "index.html"


def relhref(page, target):
    return ("" if page == "index.html" else "../") + target


def link_main(page, main):
    main = re.sub(r'<a class="xl" href="[^"]*">([\s\S]*?)</a>', r"\1", main)  # remove our old links
    have = set(re.findall(r'href="([^"]+)"', main))
    tokens = re.split(r"(<[^>]+>)", main)
    stack = []  # (tag, skip)
    done = set(); out = []
    for tok in tokens:
        if tok.startswith("<"):
            m = re.match(r"<(/?)([a-zA-Z0-9]+)", tok)
            if m:
                close, tag = m.group(1), m.group(2).lower()
                if close:
                    while stack:
                        t, _ = stack.pop()
                        if t == tag: break
                elif tag not in VOID and not tok.endswith("/>"):
                    stack.append((tag, tag in SKIP_TAGS or bool(SKIP_CLASS.search(tok))))
            out.append(tok); continue
        if not tok.strip() or any(s for _, s in stack):
            out.append(tok); continue
        segs = [tok]; added = 0  # plain text strings, and links we made (tuples)
        for pat, target in TERMS:
            if added == 2: break  # at most two new links in one run of text
            if target in done or page_of(target) == page: continue
            href = relhref(page, target)
            if href in have: continue
            for k, s in enumerate(segs):
                if isinstance(s, tuple): continue
                m = re.search(pat, s)
                if not m: continue
                segs[k:k + 1] = [s[:m.start()], (f'<a class="xl" href="{href}">{m.group(0)}</a>',), s[m.end():]]
                done.add(target); added += 1
                break
        tok = "".join(s[0] if isinstance(s, tuple) else s for s in segs)
        out.append(tok)
    return "".join(out), len(done)


def wander(page):
    items = WANDER.get(page)
    if not items: return ""
    cards = "".join(f'<a class="wander-card" href="{relhref(page, t)}"><b>{html.escape(h)}</b><span>{html.escape(s)}</span></a>'
                    for t, h, s in items)
    return (f'<section class="sec wander" aria-labelledby="wander-h">\n  <div class="wrap">\n    <p class="eyebrow">Wander further</p>\n'
            f'    <h2 class="h-sm" id="wander-h">More to discover</h2>\n    <div class="wander-grid">{cards}</div>\n  </div>\n</section>\n')


for page in PAGES:
    p = os.path.join(R, page); t = open(p).read()
    t = re.sub(r'<section class="sec wander"[\s\S]*?</section>\n', "", t)
    i = t.index('<main id="main">'); j = t.index("</main>")
    main, n = link_main(page, t[i:j])
    t = t[:i] + main + wander(page) + t[j:]
    open(p, "w").write(t)
    print(f"{page}: {n} links")
