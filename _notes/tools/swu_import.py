"""Brings The Oldest Conversation (munkachy/sing-with-us) into the abbey site as its own pages under pray/, so the
abbey site no longer links out to it:  pray/curious/  pray/curious/open-questions/  pray/christians/  pray/catholics/
pray/psalms/  pray/choir-book/  pray/quotes/.   Run again after the source pages change:

    GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/munkachy/sing-with-us /tmp/swu
    python3 _notes/tools/swu_import.py /tmp/swu

It reads each source page's <main>, drops the review marks and comments, renames the classes it brings over to sw-NAME
(so they never meet the abbey's own .call, .quote, .ask ...), turns the hero into the abbey's page-hero, copies the
pictures to assets/img/swu/ and wraps the rest in the abbey's header and footer (taken from work/index.html).
The styles are the 'Oldest Conversation pages' block at the end of assets/site.css, the script is assets/swu.js.
"""
import html, os, re, shutil, sys

SRC = sys.argv[1]
R = __file__.rsplit("/_notes/", 1)[0]
PAGES = [  # source dir, destination under pray/, <title>, description
    ("seekers", "curious", "Just curious? Come in", "You don't have to believe anything to pray with us. Come and see what it's like."),
    ("seekers/bracketing", "curious/open-questions", "Leaving the question open", "Why we say: leave the big questions open for now, and come and see."),
    ("christians", "christians", "Christian visitor? Welcome", "For Protestant and non-denominational Christians who love God's word: praying the Psalms with the monks."),
    ("catholics", "catholics", "Catholic? Welcome home", "For Catholics who feel called to go deeper in prayer: the Liturgy of the Hours with the monks."),
    ("meditations/tips", "psalms/tips", "Tips for praying the Psalms", "Short, practical ways to pray the Psalms as a conversation."),
    ("meditations", "psalms", "The Psalms as a conversation with God", "One monk's meditations: the Psalms prayed as a conversation, with the Grail text."),
    ("our-psalter", "choir-book", "Following along in our book", "How the monks' prayer works, hour by hour, and how to follow along in the abbey church."),
    ("quotes", "quotes", "Quotes about prayer", "Saints and the Church on prayer."),
]
PRAY = {s: d for s, d, _, _ in PAGES}
PRAY.update({"": "", "about": "", "index.html": ""})


def rel(frm, to):
    """relative path between two directories (site-root relative, no leading slash)"""
    a = [x for x in frm.split("/") if x]; b = [x for x in to.split("/") if x]
    while a and b and a[0] == b[0]: a.pop(0); b.pop(0)
    return "../" * len(a) + "/".join(b) + ("/" if b else "")


def fix_link(href, here):
    m = re.match(r"^((?:\.\./)+)([^#?]*)(#.*)?$", href)
    if not m: return href
    path = m.group(2).strip("/"); frag = m.group(3) or ""
    if path in PRAY and path not in ("", "about", "index.html"): tgt = "pray/" + PRAY[path]
    elif path in ("", "index.html", "about"): tgt = "pray"
    elif path == "visit": tgt = "pray"; frag = "#schedule"
    elif path == "oblates": tgt = "monastery"; frag = "#oblates"
    elif path.startswith("assets/"): return href
    else: tgt = "pray"
    r = rel(here, tgt)
    return (r or "./") + frag


def convert(sdir, slug, title, desc):
    here = "pray/" + slug
    root = rel(here, "")
    s = open(f"{SRC}/{sdir}/index.html").read()
    main = re.search(r"<main[^>]*>(.*)</main>", s, re.S).group(1)
    main = re.sub(r"<span class=\"rv[^\"]*\">.*?</span>", "", main, flags=re.S)
    main = re.sub(r"<!--.*?-->", "", main, flags=re.S)
    main = re.sub(r"<script.*?</script>", "", main, flags=re.S)
    main = re.sub(r"<div class=\"placeholder-img\">.*?</div>", "", main, flags=re.S)
    # hero -> page-hero
    hm = re.search(r"<section class=\"hero[^\"]*\">(.*?)</section>", main, re.S)
    hero = ""; credit = ""
    if hm:
        h = hm.group(1)
        img = re.search(r"<img src=\"([^\"]*)\" alt=\"([^\"]*)\"", h)
        kicker = re.search(r"class=\"kicker\">(.*?)</span>", h, re.S)
        h1 = re.search(r"<h1>(.*?)</h1>", h, re.S)
        lede = re.search(r"<p class=\"lede\">(.*?)</p>", h, re.S)
        cr = re.search(r"<p class=\"credit\">(.*?)</p>", h, re.S)
        hero = ("<section class=\"page-hero\">\n  " + (f"<img src=\"{img.group(1)}\" alt=\"{img.group(2)}\" width=\"1600\" height=\"1066\">" if img else "") +
                "\n  <div class=\"wrap\">\n    " + (f"<p class=\"eyebrow\">{kicker.group(1)}</p>" if kicker else "") +
                f"\n    <h1 class=\"h-xl\">{h1.group(1) if h1 else title}</h1>" +
                (f"\n    <p class=\"lead\">{lede.group(1)}</p>" if lede else "") + "\n  </div>\n</section>\n")
        if cr: credit = f"<div class=\"wrap\"><p class=\"credit small\">{cr.group(1)}</p></div>\n"
        main = main.replace(hm.group(0), "")
    else:  # pages without a hero (bracketing): make a plain head
        m1 = re.search(r"<h1>(.*?)</h1>", main, re.S)
        hero = ("<section class=\"page-hero page-hero-plain\">\n  <div class=\"wrap\">\n    <p class=\"eyebrow\">The Oldest Conversation</p>\n"
                f"    <h1 class=\"h-xl\">{m1.group(1) if m1 else title}</h1>\n  </div>\n</section>\n")
        if m1: main = main.replace(m1.group(0), "", 1)
    # pictures
    os.makedirs(f"{R}/assets/img/swu", exist_ok=True)
    def pic(m):
        name = os.path.basename(m.group(2))
        shutil.copy(f"{SRC}/assets/img/{name}", f"{R}/assets/img/swu/{name}")
        return m.group(1) + root + "assets/img/swu/" + name
    main = re.sub(r"(src=\")((?:\.\./)+assets/img/[^\"]+)", pic, main)
    hero = re.sub(r"(src=\")((?:\.\./)+assets/img/[^\"]+)", pic, hero)
    # links
    main = re.sub(r"href=\"((?:\.\./)+[^\"]*)\"", lambda m: "href=\"" + fix_link(m.group(1), here) + "\"", main)
    # buttons, classes
    main = main.replace("class=\"btn ghost\"", "class=\"btn btn-line\"")
    main = re.sub(r"class=\"btn\"", "class=\"btn btn-ink\"", main)
    RENAME = ("ask q choices choice reply if big primer inner qa tip tip-badge tip-q tip-more quote quote-badge quote-who quote-more call num mood "
              "mood-picker mood-grid mood-chip mood-word mood-ps back-to-moods setting label-meditation exchange psalm heard voice voice-img said who "
              "monk god tagline ornament note callout art book-scan side-links what intro dropcap freely freely-q freely-ref join-row sorrow joy trust mercy "
              "skip-questions suggested portrait door").split()
    def cls(m):
        return "class=\"" + " ".join(("sw-" + c if c in RENAME else c) for c in m.group(1).split()) + "\""
    main = re.sub(r"class=\"([^\"]*)\"", cls, main)
    # template (abbey header and footer) from work/index.html
    t = open(f"{R}/work/index.html").read()
    head, tail = t.split("<main id=\"main\">", 1)
    tail = tail.split("</main>", 1)[1]
    def deeper(x):
        x = re.sub(r"(href|src)=\"\.\./", lambda m: f"{m.group(1)}=\"{root}", x)
        return x
    head = deeper(head); tail = deeper(tail)
    head = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} · St. Bernard Abbey</title>", head)
    head = re.sub(r"(<meta name=\"description\" content=\").*?(\">)", lambda m: m.group(1) + html.escape(desc, quote=True) + m.group(2), head, count=1)
    head = re.sub(r"(<link rel=\"canonical\" href=\").*?(\">)", lambda m: m.group(1) + "https://www.stbernardabbey.com/pray/" + slug + "/" + m.group(2), head)
    head = head.replace("<body>", "<body>")
    tail = tail.replace("</body>", f"<script src=\"{root}assets/swu.js?v=1\" defer></script>\n</body>", 1) if "swu.js" not in tail else tail
    out = head + "<main id=\"main\">\n" + hero + credit + "<div class=\"swu\">\n" + main.strip() + "\n</div>\n" + (
        f"<div class=\"wrap swu-back\"><a class=\"more\" href=\"{rel(here, 'pray')}\">Back to Pray with Us <svg class=\"ic\"><use href=\"#i-arrow\"/></svg></a></div>\n") + (f"<div class=\"wrap pair-rule\" aria-hidden=\"true\"><img src=\"{root}assets/img/brand/cross-light.svg\" alt=\"\" width=\"132\" height=\"175\"><span></span><img class=\"crest\" src=\"{root}assets/img/crest.png\" alt=\"\" width=\"391\" height=\"718\"></div>\n") + "</main>" + tail
    os.makedirs(f"{R}/{here}", exist_ok=True)
    open(f"{R}/{here}/index.html", "w").write(out)
    print(here, len(out))


for p in PAGES: convert(*p)
