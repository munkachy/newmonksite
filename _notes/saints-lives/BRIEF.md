# Brief: "The saints of our reliquary" (hidden page, saints/)

Br. Augustine (webmaster of St. Bernard Abbey, Cullman, Alabama) asked for: detailed information about the life of
every saint in the abbey's reliquary, their patronage, and why their intercession could matter to St. Bernard Abbey
and St. Bernard Preparatory School. You write one slice of the entries as JSON.

## Sources you must read first
- `/home/user/newmonksite/relics/README.md`: the catalogue. Section "The relics, by reliquary" says what the abbey
  holds and where; section "## The saints" has a careful paragraph on each saint. Start from that paragraph: keep its
  facts and its honesty about legend vs. history, and EXPAND it into a fuller life.
- `/home/user/newmonksite/_notes/ABBEY-FACTS.md` and the facts below, for the "why here" part.

## About the abbey and the school (use only these facts; do not invent others)
- Benedictine monks (Rule of St. Benedict; "ora et labora", prayer and work; vows of stability, obedience,
  conversatio morum). About 30 monks. Founded 1891 by monks of St. Vincent Archabbey (Latrobe, PA), whose founder came
  from Metten Abbey in Bavaria: German Catholic roots, and Cullman is a town founded by German immigrants.
  American-Cassinese Congregation; Diocese of Birmingham. More than 800 acres. Vocations are increasing.
- Patron: St. Bernard of Clairvaux. Planned-giving society: the Clairvaux Society.
- Work: Ave Maria Grotto (Br. Joseph Zoettl built 125 miniature shrines, many of the Holy Land and of Rome, from
  stone, shells, glass, marbles and scrap; dedicated 1934), a tradition of craftsman monks (builders, carvers like
  Br. Jude, a potter Br. Leo), bakery (Br. Benedict, head baker), small beef-cattle farm, ~40 chickens, garden,
  tailoring, publishing (Br. Leo edits and reprints the abbey's history books), grounds, guest masters, a Retreat and
  Conference Center (since 1981), an infirmary for old and sick monks, a cemetery of the monks.
- School: monks have taught since 1892 (at times a high school, junior college, four-year college and seminary);
  St. Bernard Prep since 1984: Catholic boarding AND day school, grades 7–12, boys and girls, students from across the
  country and abroad, beside the monastery; aim "cultivating a love of learning and a life of virtue in young men and
  women". Monks teach (Latin, theology, math, civics, PE), coach, keep the library, coach Scholars' Bowl, say Mass.
  Students are teenagers far from home (boarders), athletes, studying, discerning their lives.
- History the abbey honors: Abbot Benedict Menges nursed the sick in the 1878 yellow fever; Fr. Urban Tracy served
  lepers; Frater Hubert Carney died nursing others in the 1918 flu; monks served as military chaplains in both world
  wars and Korea; Abbot Hilary worked with Alcoholics Anonymous; Br. Wolfgang Wolf was a botanist; Fr. Benedict
  Oberdoerfer taught chemistry for 50 years.
- Monks' name saints (a monk named for a saint in your slice is a good link): Brendan (Abbot), Cletus, Mark,
  Joel, Charles Lwanga (Br. Charles, procurator), John Bosco (Fr. John), Leo the Great (Br. Leo), Bede (Fr. Bede,
  prior), Patrick (Fr. Patrick), Michael, Benedict (Br. Benedict, baker, oblate director), Thomas Aquinas (Br. Thomas,
  librarian), Linus, Irenaeus, Christopher, Dominic (Fr. Dominic, subprior, math teacher), Paschal Baylon, Pachomius,
  Augustine of Hippo (Br. Augustine, webmaster), Raphael, Damien of Molokai, Nicholas of Myra and Boniface (novices).
- Oblates (lay people attached to the monastery).

## What to write for each entry (JSON)
{
  "id": "kebab-case-slug, e.g. aloysius-gonzaga (use the slug given in your list)",
  "name": "St. Aloysius Gonzaga",
  "dates": "1568–1591",            // "" if unknown
  "title": "Jesuit, nurse of the plague-stricken",   // a few words
  "feast": "21 June",
  "life": ["paragraph", "paragraph", ...],   // 3–5 paragraphs, about 300–450 words in all; for a saint the
                                              // label can't identify (Agapitus, Secundus, Innocent, Eugene,
                                              // Faustinus, Justina, an unknown Philip) 1–3 paragraphs on the
                                              // candidates is enough
  "patronage": ["young people", "students", ...],  // traditional and official patronages; when a pope declared it,
                                                    // say so in brackets, e.g. "Catholic youth (Pius XI, 1926)"
  "why_here": ["paragraph", ...],   // 1–2 paragraphs, 80–180 words: why his or her prayers matter for the
                                    // monks AND/OR the Prep's students, teachers, families. Concrete, honest, not
                                    // forced; link to the facts above. Don't repeat the same angle for every saint.
  "relic": "One sentence: what the abbey holds (from the catalogue): reliquary, label as read, e.g. 'Four relics: ...'",
  "check": "Optional. Anything uncertain Br. Augustine should verify. Omit if nothing."
}
Group entries (the Uganda Martyrs; Jacinta and Francisco; Beatrice I and II) are one entry each.

## Style (match the site)
- Plain, warm, exact English, American spelling. Short sentences. No gushing, no pious clichés, no exclamation marks.
- Be honest: say plainly what is legend and what is history, as the catalogue does. Never present a legend as fact.
- No colons-heavy or semicolon-heavy prose; no em-dash chains; use en dash only in date ranges.
- HTML allowed inside strings: <em> for book titles and Latin only. Escape nothing else; no markdown.
- Don't invent facts about the abbey, its monks or its relics. Don't claim a relic is authentic.
- Be accurate on dates, feasts and patronages; if you are not sure of a detail, leave it out or put it in "check".
  You may use WebSearch/WebFetch to verify facts if available.

## Output
Write a JSON array (valid JSON, UTF-8, real characters, not \u escapes) to the file named in your task, in the order
given. Then validate it with `python3 -c "import json;json.load(open(PATH))"`. Reply with only: the count written,
and any entries you flagged in "check".

## Summaries (added 3 Nov 2026)
Each entry also gets a "summary" field: the short version shown on the page before "Read more". 2–3 sentences,
40–70 words, plain text (<em> allowed). Say who the saint was and what he or she is best known for, name the one or
two chief patronages, and end with a short clause on why the saint matters to the abbey or the Prep. Same honesty
as the full text (no legend stated as fact); for saints the label can't identify, say so in a sentence.
