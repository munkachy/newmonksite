"""Builds the two Sing With Us sections of pray/index.html from the munkachy/sing-with-us site:
#begin ("Where are you starting from?", the three doors) and #psalms (the mood picker, with the opening of each
"phone call" with a psalm and its tip). Run again after the meditations change:

    git clone --depth 1 https://github.com/munkachy/sing-with-us /tmp/swu
    python3 _notes/tools/swu_pray.py /tmp/swu

It replaces the sections by id (or inserts them the first time: #begin after the opening section, #psalms after
#lectio). The door texts are written here, in the words of the door pages; the meditations are copied from
meditations/index.html (short Grail excerpts, with the Grail notice, as on that site).
"""
import html, re, sys

SWU = "https://munkachy.github.io/sing-with-us/"
R = __file__.rsplit("/_notes/", 1)[0]
src = open(sys.argv[1] + "/meditations/index.html").read()


def clean(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"[ \t]+", " ", html.unescape(s)).strip()


def e(s):
    return html.escape(s, quote=False)


moods = re.findall(r'<a class="mood-chip" href="#(ps-\d+)"><span class="mood-word">([^<]+)</span>', src)
calls = {}
for pid, b in re.findall(r'<article class="call" id="(ps-\d+)">([\s\S]*?)</article>', src):
    d = {"title": clean(re.search(r"<h3>([\s\S]*?)</h3>", b).group(1)),
         "kicker": clean(re.search(r'<p class="kicker[^"]*">([\s\S]*?)</p>', b).group(1))}
    s = re.search(r'<p class="setting">([\s\S]*?)</p>', b)
    d["setting"] = clean(s.group(1)) if s else ""
    d["ex"] = []
    for x in re.findall(r'<div class="exchange">([\s\S]*?)</div></div>', b)[:2]:
        v = re.search(r'<blockquote class="psalm"><p>([\s\S]*?)</p><footer>([\s\S]*?)<span', x)
        w = re.search(r'<p class="voice (god|monk)">[\s\S]*?<span class="who">([^<]+)</span><i>([\s\S]*?)</i>', x)
        d["ex"].append((clean(v.group(1)), clean(v.group(2)), w.group(1), clean(w.group(2)), clean(w.group(3))))
    t = re.search(r'<h4 class="tip-q"[^>]*>([\s\S]*?)</h4>\s*<p>([\s\S]*?)</p>', b)
    d["tip"] = (clean(t.group(1)), clean(t.group(2))) if t else None
    n = re.search(r'<p class="note">([\s\S]*?)</p>', b)
    d["note"] = clean(n.group(1)) if n and pid == "ps-38" else ""  # only the pastoral one (see a doctor); the others comment on the whole call
    calls[pid] = d


def choices(name, opts):
    """A question with answer buttons; each answer shows its own reply (site.js, [data-choose])."""
    q, items = opts
    btns = "".join(f'<button type="button" class="pick" data-choose="{name}-{i}" aria-pressed="false">{e(a)}</button>'
                   for i, (a, _) in enumerate(items))
    reps = "".join(f'<p class="reply" id="{name}-{i}" data-group="{name}">{r}</p>' for i, (_, r) in enumerate(items))
    return f'<div class="ask"><p class="ask-q">{e(q)}</p><div class="picks" role="group" aria-label="{e(q)}">{btns}</div>{reps}</div>'


DOORS = [
    ("curious", "Just curious", f"""
      <p class="gate-lead">You don't have to believe anything to pray with us.</p>
      <p>No one will ask what you believe. There's nothing to join and nothing to sign. Sit in the pews, sing along, or simply listen. The monks sing very old words that shepherds and kings, prisoners and exiles have prayed: full of joy and anger, fear and thanks. Every human feeling is in there somewhere.</p>
      <blockquote class="gate-quote">“You have made us for yourself, and our heart is restless until it rests in you.”<cite>St. Augustine, who ran from faith for years, <i>Confessions</i> 1.1</cite></blockquote>
      <p>No one can prove to you that these words are sacred. We invite you to try them. When one of Jesus' first followers scoffed, his friend didn't argue. He just said, “Come and see” (John 1:46).</p>
      {choices("q-cur", ("Have you ever heard monks chant?", [
          ("No", "It's simpler than you might think, and very peaceful: mostly psalms, sung back and forth, and a good deal of silence."),
          ("On a recording", "In person is different. You hear the breath, the stone, the silence between verses."),
          ("In person", "Then you know the feeling. Come and feel it again.")]))}
      <div class="btn-row"><a class="btn btn-ink" href="{SWU}seekers/">A page for the curious</a><a class="btn btn-line" href="#hours-h">What happens at each hour</a><a class="btn btn-line" href="../visit/">Plan a visit</a></div>"""),
    ("christian", "A Christian", f"""
      {choices("q-chr", ("One question before anything else: do you believe the Psalms are the inspired, God-breathed word of God?", [
          ("Yes", "So do we. The Psalms are holy ground we share."),
          ("I'm not sure", "Thank you for being honest. We believe they are, and you are just as welcome to pray them with us."),
          ("No", "Thank you for being honest. We believe they are, and you are just as welcome to pray them with us.")]))}
      <p>Jesus prayed the Psalms all his life, even on the cross: “My God, my God, why have you forsaken me?” (Matthew 27:46, quoting Psalm 22). Christians are divided, and the world is more divided still. So for a little while, let's set our divisions aside and simply sing to God together. You don't need to be Catholic, and you don't need to ask anyone. Just come in and sit in the pews.</p>
      <p><b>An honest note:</b> besides the Psalms you will hear hymns, Bible readings and prayers for the world, and also hymns to Mary and prayers honoring the saints. If you disagree with those parts, you don't have to sing them. Stay silent and pray to God in your own words.</p>
      <p><b>Did you know?</b> Protestants can become Benedictine oblates: Christians who join their prayer to a monastery's and follow the Rule of St. Benedict in ordinary life. Some of our own oblates are Protestant.</p>
      <div class="btn-row"><a class="btn btn-ink" href="{SWU}christians/">A page for Christian visitors</a><a class="btn btn-line" href="../monastery/#oblates">About oblates</a><a class="btn btn-line" href="#schedule">Prayer times</a></div>"""),
    ("catholic", "A Catholic", f"""
      {choices("q-cat", ("Do you feel called to go deeper in prayer?", [
          ("Yes", "Thanks be to God. That call is his, and he will help you answer it."),
          ("Maybe", "A small “maybe” is often how it starts. Let's take one step together."),
          ("I'm not sure", "That's an honest answer. Read on, and see if something stirs.")]))}
      <p>When the monks sing the Psalms, they are not praying alone. The Second Vatican Council taught that Christ “joins the entire community of mankind to Himself, associating it with His own singing of this canticle of divine praise” (<i>Sacrosanctum Concilium</i> 83). The Office stretches the praise of the Mass across the day; the Catechism calls it “like an extension of the Eucharistic celebration” (no. 1178).</p>
      <p>And it isn't only for monks. The Liturgy of the Hours “is intended to become the prayer of the whole People of God,” and “the laity, too, are encouraged to recite the divine office” (CCC 1175).</p>
      {choices("q-loh", ("Have you prayed the Liturgy of the Hours before?", [
          ("Never", "Then this is a beautiful place to begin. You don't need a book or any experience. Just come."),
          ("Sometimes", "Praying it with a choir is different from praying it alone. Come hear it sung."),
          ("Every day", "Then you're already praying with us. Come and pray it with us in person. (Our monastic book is arranged differently from the four-volume breviary, and uses the older psalm numbers.)")]))}
      <div class="btn-row"><a class="btn btn-ink" href="{SWU}catholics/">A page for Catholics</a><a class="btn btn-line" href="#office">The Divine Office</a><a class="btn btn-line" href="../relics/">The relics</a><a class="btn btn-line" href="../monastery/#oblates">Become an oblate</a></div>"""),
]

begin = f'''<section class="sec" id="begin" aria-labelledby="begin-h">
  <div class="narrow">
    <p class="eyebrow">Before you come</p>
    <h2 class="h-md" id="begin-h">Where are you starting from?</h2>
    <p class="lead" style="margin-top:1rem">Pick the door that fits you. There are no wrong answers.</p>
    <div class="picks gates" role="group" aria-label="Choose a door">{"".join(f'<button type="button" class="pick" data-choose="door-{k}" aria-pressed="false">{e(lbl)}</button>' for k, lbl, _ in DOORS)}</div>
    {"".join(f'<div class="gate reply" id="door-{k}" data-group="door">{body}</div>' for k, _, body in DOORS)}
    <p class="small" style="margin-top:1.4rem">Whoever you are: <a href="#psalms">try talking with God in the Psalms</a>, the way one of our monks does.</p>
  </div>
</section>
'''


def callpanel(pid, d):
    ex = ""
    for verse, ref, voice, who, said in d["ex"]:
        ex += (f'<blockquote class="psalm-verse"><p>{e(verse).replace(chr(10), "<br>")}</p><cite>{e(ref)}</cite></blockquote>'
               f'<p class="voice voice-{voice}"><span class="who">{e(who)}</span> <i>{e(said)}</i></p>')
    tip = f'<aside class="call-tip"><p class="who">Tip: {e(d["tip"][0])}</p><p>{e(d["tip"][1])}</p></aside>' if d["tip"] else ""
    setting = f'<p class="small">{e(d["setting"])}</p>' if d["setting"] else ""
    return (f'<div class="call reply" id="call-{pid}" data-group="call"><p class="eyebrow">{e(d["kicker"])}</p>'
            f'<h3 class="h-sm">{e(d["title"])}</h3>{setting}{ex}'
            f'<p class="small">… <a href="{SWU}meditations/#{pid}">Read the whole call</a></p>'
            + (f'<p class="call-note">{e(d["note"])}</p>' if d["note"] else "") + f'{tip}</div>')


chips = "".join(f'<button type="button" class="pick" data-choose="call-{pid}" aria-pressed="false">{e(w)}</button>'
                for pid, w in moods)
psalms = f'''<section class="sec on-stone" id="psalms" aria-labelledby="psalms-h">
  <div class="narrow">
    <p class="eyebrow">One monk's conversations with God</p>
    <h2 class="h-md" id="psalms-h">What kind of day are you having?</h2>
    <p style="margin-top:1rem">One of our monks prays the Psalms like a phone call. He hears one verse as his own voice and the next as God answering him. Some days the call is sorrowful, some days full of joy. Tap the word that fits today, and he will show you how one of his calls began.</p>
    <div class="picks moods" role="group" aria-label="Choose a mood">{chips}</div>
    {"".join(callpanel(pid, d) for pid, d in calls.items())}
    <p class="small" style="margin-top:1.4rem">These are one monk's personal meditations, not Church teaching; the psalm text is never changed. Psalm numbers: most Bibles first, our choir book in parentheses. Psalm text: the Grail translation, which our choir sings, © 1963 The Grail (England). <a href="{SWU}meditations/">All the meditations</a> · <a href="{SWU}meditations/tips/">Tips for when prayer is hard</a> · <a href="{SWU}quotes/">The saints on prayer</a></p>
  </div>
</section>
'''

p = R + "/pray/index.html"
t = open(p).read()
for sid, block, after in (("begin", begin, None), ("psalms", psalms, "lectio")):
    m = re.search(rf'<section class="[^"]*" id="{sid}"[\s\S]*?</section>\n', t)
    if m:
        t = t[:m.start()] + block + t[m.end():]
    elif after:
        m = re.search(rf'<section class="[^"]*" id="{after}"[\s\S]*?</section>\n', t)
        t = t[:m.end()] + "\n" + block + t[m.end():]
    else:  # after the opening section (the one right after the page hero)
        i = t.index('<section class="sec">'); j = t.index("</section>\n", i) + len("</section>\n")
        t = t[:j] + "\n" + block + t[j:]
open(p, "w").write(t)
print(len(calls), "calls,", len(moods), "moods")
