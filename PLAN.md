# New St. Bernard Abbey website: plan and hand-off

A new version of stbernardabbey.com (now on Wix), built here as plain HTML, CSS and JS: no build step, no libraries,
**relative paths** (so it works at `munkachy.github.io/newmonksite/` now and at the domain root later), the same way
as the `munkachy/sbp` site. Br. Augustine, OSB (webmaster) asked for it on 1 Nov 2026.

**Live preview: https://munkachy.github.io/newmonksite/** (GitHub Pages serves `main`, root folder; it rebuilds in a
minute or two after each push). To publish, test, then fast-forward `main` to the work branch. Folders starting with
`_` (`_notes/`, `_source/`) are not published.

**Anyone picking this up (another Claude account or session):** read this file first, then `_notes/`. Work on branch
`claude/saint-photo-identification-ksp79d` (PR #1 in munkachy/newmonksite). `git pull` before you start and before
you push; commit and push after every finished piece, and tick it off below with a line in the log at the bottom.
Take one job at a time, mark it `[~] taken (date, who)` and push that mark first so two accounts don't do the same job.
If a job marked taken has had no commit for two hours, the session that took it has probably hit a limit: take it over.

## What Br. Augustine asked for

1. **Theme: a tradition of craftsman monks.** Br. Joseph Zoettl (Ave Maria Grotto) is only the most famous; feature
   him much more, and show the others (Br. Jude Johnston, Br. Nicholas, and the rest; see `_notes/CRAFTSMEN.md`).
   This list will grow later.
2. **Two faces, like the sign on the highway: Ave Maria Grotto and St. Bernard Prep.** Craftsmen and a school.
3. **The monks' film** featured like the virtual tour on the sbp site: a still under a soft veil with a big "Play"
   that plays the film in place (sbp `assets/site.css` `.tour`, `assets/site.js` "Virtual tour").
4. **A relics page** where people can see the relics. A professional photographer will later shoot each relic
   (a wide view and a close-up) and a long shot of all the relics together on the altar; until then use the best of
   Br. Augustine's photos (`relics/`, groups in `_notes/relic-groups.json`) as placeholders, clearly marked.
5. Learn from good monastery sites, especially **St. Michael's Abbey** (Norbertines, Silverado CA). Research done:
   `_notes/MONASTERIES.md` (ideas to borrow, recommended navigation and home-page order, pitfalls, screenshots were
   taken but are not kept).
6. Look at the Ave Maria Grotto site and its gift shop (facts in `_notes/CRAFTSMEN.md`).

## Decisions (keep to these unless Br. Augustine says otherwise)

- **Look**: St. Michael's calm: full-width warm photography, a thin elegant serif for headings, cream paper, deep
  ink text, one muted gold accent (dark enough to read on cream; never gold text on cream for body copy), black-and-
  white close-ups of hands at work for the craft sections. Fonts from Google Fonts (the sbp Adobe kit is licensed to
  the school only): **Cormorant Garamond** (headings) and **Source Sans 3** (text). Crest: `_source/abbey-img/logo.jpg`.
- **Navigation**: The Grotto · Monks at Work · The School · Pray with Us · Visit · ♥ Give (pill). Utility line above:
  today's Grotto hours and the next prayer time (computed in JS from the tables below, Central time).
- **Home page order**: (1) hero: silent loop `media/hero-720/1080.mp4` (21.6 s, cut from the film; title card removed 2 Nov 2026; pause button;
  still `media/film-still-33.jpg` for reduced motion) with the abbey's name and one line; (2) "Two works, one house":
  equal cards for the Grotto and the Prep; (3) Monks at work: Br. Joseph first, then the strip "A Builder / A Carver /
  A Baker / A Scribe / A Teacher"; (4) the film (sbp tour pattern; `media/film-720.mp4`, 8:30, poster
  `media/film-still-436.jpg`); (5) Pray with us: live "now / next" schedule; (6) the relics: one image and a link;
  (7) three asks in this order: let us pray for you, is God calling you, support the monks; (8) footer.
- **Pages** (one folder each, `index.html` inside): `grotto/`, `work/` (monks at work / craftsmen), `school/`,
  `monastery/` (the monks, daily life, history, vocations, oblates), `pray/` (schedule, Divine Office), `relics/`,
  `visit/` (Grotto visit, retreat center, directions), `give/` (Donorbox, will, Mass intentions, Clairvaux Society).
  Shared: `assets/site.css`, `assets/site.js`, `assets/img/` (web-sized images, ≤ 1800 px, JPEG q≈80).
- **Facts**: only from `_notes/ABBEY-FACTS.md`, `_notes/CRAFTSMEN.md`, `relics/README.md` or a cited
  source. The abbey Necrology is public (Br. Augustine, 1 Nov 2026): quote it, citing "the abbey Necrology". Mark
  anything uncertain for Br. Augustine.
- **Don't**: animations that hide content when JS is off, pop-ups, carousels, dated widgets that go stale, 24-hour
  times. Test at 1440 and 390 wide, light only, no console errors, no sideways scroll (see sbp CLAUDE.md "Testing").

## Where things stand (read first)

*Last updated 1 Nov 2026, evening.* Live: https://munkachy.github.io/newmonksite/ . Done: home, Monks at Work, Relics;
phone menu fixed; all links checked. **The four research helpers have finished** (1 Nov 2026) (briefs in
`_notes/briefs/README.md`): Facebook monk posts (→ `_notes/MONKS.md`), Anne Stephens photos (→ `_notes/STEPHENS.md`),
Josh Viola photos (→ `_notes/VIOLA.md`), Br. Leo / Fr. John / Br. Jude (→ `_notes/CRAFTSMEN.md`). If those files are
missing or unfinished, rerun the brief. **Next after research**: (a) DONE 2 Nov 2026: job 5b "Get to know the monks" (`monastery/#monks`);
(b) DONE: Br. Leo, Fr. John, Br. Nicholas and more on Br. Jude are on `work/` ("The craftsmen today"); (c) swap placeholder pictures for Stephens/Viola
photos with credits; then jobs 2, 6, 7, 9.

**Facts given by Br. Augustine (1 Nov 2026)**: the Necrology is public; no carpenter at present (woodshop = tradition
only, no custom-work offer); Br. Joseph Goode (gone to another monastery) and Br. Gabriel Maddox (left) stay off the
site; novices may be shown; Br. Damien and Br. Raphael are juniors; photos by Anne Stephens and Josh Viola may be used
with credit. Publishing: commit on the work branch, then push the same commit to `main` (Pages).

**Repo size (1 Nov 2026): about 940 MB, at GitHub's ~1 GB guideline for a Pages repo.** Do NOT add more raw photos or
video to the repo. Keep raw sources in Google Drive (the "Relics" folder's parent, or a new "Abbey website sources"
folder) and commit only web-sized copies used on the site (`assets/img/`, ≤ 1800 px, q≈80). Slimming the history
(removing `_source/stephens` etc. from past commits) needs a force-push to `main`: only with Br. Augustine's yes.

## Jobs

Jobs 2–8 can run in parallel once job 1 is pushed (they share only `assets/site.css`; add page-specific styles at the
end of it under a comment with your page's name, or in a `<style>` block in your page, to avoid merge conflicts).

- [x] **1. Foundation** (`assets/site.css`, `assets/site.js`, header/footer, home page `index.html`). Done 1 Nov 2026.
  Every section folder has a starter `index.html` with the shared header and footer: replace its `<main>` with the
  real page. Images in `assets/img/` (see the list in `assets/img/README.md`).
- [x] **2. The Grotto** (`grotto/`, done 2 Nov 2026): Br. Joseph's life, the miniatures, visiting info, shop link, Library of Congress
  photos (`_notes/research-img/`, credits in its `CREDITS.md`).
- [x] **3. Monks at Work** (`work/`): done 1 Nov 2026: Rule ch. 57, Br. Joseph with a timeline and his own words, Br. Jude,
  the builders of the past, the work today. Wanted: a photo of Br. Jude or his work (the picture there is a placeholder)
  and the names of living craftsman monks.
- [x] **4. Relics**: done 1 Nov 2026. Cards built by a script from `_notes/relic-groups.json` (cover = first photo of each
  group, `assets/img/relics/`); when the photographer's pictures come, replace `assets/img/relics/<group-id>.jpg`, drop
  the "Placeholder photo" badges, and put the altar long shot in the dashed `.altar-slot`. (`relics/index.html`): from `_notes/relic-groups.json` and `relics/README.md`: groups as cards
  (placeholder photo marked "Photo to come"), each with its saints; a slot for the long shot on the altar.
  Make web copies of the chosen photos in `assets/img/relics/`. Keep `relics/README.md` as the full catalogue.
- [x] **5. The monastery and prayer** (`monastery/`, `pray/`, done 2 Nov 2026): the monks (9 profiles in
  `_source/abbey-pages/monk-profiles.md`), a day in the life, formation, FAQ (visible, not hidden), oblates,
  history (Metten → St. Vincent → 1891), the abbots, the live schedule.
- [x] **5b. Get to know the monks** (done 2 Nov 2026: `monastery/#monks`, 22 cards in three groups, portraits in
  `assets/img/monks/` cut from Anne Stephens's *Monk Headshots*; to do: photos of Br. Irenaeus and the two novices, the
  feast day of each monk's name saint (only Br. Augustine's is known), more on Br. Michael and Br. Christopher, a strip
  on the home page if wanted) (in `monastery/`, perhaps also a strip on the home page): every monk on the
  roster (`_notes/ROSTER.md`) with a photo and a few lines, drawn from the abbey's own Facebook posts (written by
  Br. Augustine; gathered in `_notes/MONKS.md`) and Anne Stephens's photographs (`_notes/STEPHENS.md`,
  `_source/stephens/`; credit "Photo: Anne Stephens") and Josh Viola's (`_notes/VIOLA.md`, `_source/viola/`; credit "Photo: Josh Viola"). Like Saint Louis Abbey's "Meet our family": face, name,
  hometown, work, feast day. Show them in groups: solemnly professed monks, juniors (simple vows: Br. Damien,
  Br. Raphael), novices (Br. Nicholas, Br. Boniface: may be shown).
- [x] **6. Visit and Give** (`visit/`, `give/`, done 2 Nov 2026).
- [x] **7. The School** (`school/`, done 2 Nov 2026): a short page on St. Bernard Prep as a work of the monks, linking to
  stbernardprep.com (and to the sbp preview when it goes live).
- [ ] **8. Pictures**: choose the best photos in `_source/abbey-img/` (see its `INDEX.md`) for each page, make web
  copies in `assets/img/`, and list each with its page in `assets/img/README.md`.
- [ ] **10. Picture pass over the whole site** (after `_notes/STEPHENS.md` and `_notes/VIOLA.md` are finished): go page
  by page and choose the best picture for every slot from all sources (Stephens, Viola, Facebook monk photos, the old
  site in `_source/abbey-img/`, Library of Congress, the film stills). Prefer real monks at work and prayer over
  empty rooms; faces for "Get to know the monks"; the Grotto photos for `grotto/`. Make web copies in `assets/img/`
  (≤ 1800 px, q≈80), credit every photo under it ("Photo: Anne Stephens", "Photo: Josh Viola"), and update
  `assets/img/README.md`. Br. Augustine asked for this, 1 Nov 2026.
- [ ] **11. Media page** (`media/` is taken by the video files, so use `photos/`): a gallery of good photos not used
  elsewhere, grouped (the community, liturgy, the church and grounds, the Grotto, the school, at work), each with
  photographer credit; plus the film and the Facebook/Instagram/YouTube links. Thumbnails ~600 px, lazy-loaded,
  opening the 1800 px copy. Link it from the footer. Br. Augustine asked for this, 1 Nov 2026.
- [ ] **9. Check everything**: Playwright at 1440 and 390, every link, then a short report for Br. Augustine.

## For Br. Augustine to decide or supply

- Permission to use photos of Br. Joseph (Grotto archive, ADAH, Troy University).
- Who drew the campus map ("Br. Nicholas", living), and which living monks are craftsmen today.
- The 78-second trailer on YouTube (`9HsUwl-Prf0`) could not be downloaded here; the full film is used instead.
- Whether the site keeps Donorbox for gifts.

## Log

- 1 Nov 2026: research done (abbey site crawled: `_source/`; monastery sites: `_notes/MONASTERIES.md`; craftsmen:
  `_notes/CRAFTSMEN.md`); film re-encoded (`media/film-720.mp4`, 53 MB), hero loop cut (`media/hero-*.mp4`),
  stills (`media/film-still-*.jpg`). Plan written. Starting job 1.
- 1 Nov 2026: job 1 done: home page (hero loop, two works, craftsman monks, the film, prayer times live in Central
  time, relics, three asks), shared CSS/JS, starter pages. Tested at 1440 and 390: no console errors, no sideways
  scroll. Preview: serve the parent folder (`cd .. && python3 -m http.server 8770`), open /newmonksite/.
- 1 Nov 2026: job 4 done (relics page, 14 reliquaries, all 122 photos as thumbnails linking to the labeled copies). Job 3 taken.
- 1 Nov 2026: job 3 done (work/). Jobs 2, 5, 6, 7, 8, 9 are open.
- 1 Nov 2026: the Necrology is public (Br. Augustine): full craftsmen notes now in `_notes/CRAFTSMEN.md`; Br. Joseph's own words added to work/.
- 1 Nov 2026: published to main at Br. Augustine's request; live at https://munkachy.github.io/newmonksite/ (home, work, relics; other pages are starters).
- 1 Nov 2026: fixes from Br. Augustine's phone: heading words glued when the line break is hidden on phones (space before every <br>), and the phone menu trapped inside the header by `backdrop-filter` (removed; the menu now covers the screen and shows an X). QA script: every page at 1440 and 390, images, overflow, all 166 links and #anchors: clean. Added real Mass-intention, giving, vocation and oblate sections so the home page's links land. CSS/JS now ?v=2.
- 1 Nov 2026: roster (Mar 2026) in `_notes/ROSTER.md`; Anne Stephens's SmugMug photos may be used with credit; the abbey's Facebook monk posts may be used. Research running on: the Facebook posts, the SmugMug galleries, Br. Leo Borelli, Fr. John O'Donnell, Br. Jude. No current carpenter: woodshop shown as tradition only.
- 1 Nov 2026: Josh Viola's photographs (pic-time portfolio) may be used with credit "Photo: Josh Viola".
- 1 Nov 2026: Br. Gabriel Maddox (novice) has left: leave him off the site. Br. Joseph Goode has gone to another monastery: leave him off too.
- 1 Nov 2026: novices may be named and shown; Br. Damien and Br. Raphael are juniors (simple vows).
- 1 Nov 2026: work/ gets "The craftsmen today" (Br. Leo Borelli, Fr. John O'Donnell, Br. Nicholas Smith) and more on Br. Jude (Meštrović, Pratt, Yale, his own words; abbey's portrait). Wanted: photos of Br. Leo's ceramics, Fr. John's painted churches, Br. Nicholas's art.
- 1 Nov 2026: Br. Augustine asked for a media/photos page and a picture pass over the whole site with the new photos (jobs 10 and 11).
- 1 Nov 2026: Facebook research done: `_notes/MONKS.md` (16 monks with plenty, 2 thin, 4 nothing: Br. Damien, Br. Raphael, Br. Nicholas, Br. Boniface). Facebook can't be read without login: Br. Augustine may export or paste his monk posts. Photos in `_notes/monk-img/` (abbey's own).
- 1 Nov 2026: Viola research done: only the Abbot Marcus Thanksgiving Mass gallery (137 photos, 1600 px) is public; Abbot Brendan, Fr. Pachomius, Br. Augustine's solemn profession and MonkMindset are behind Pic-Time's login (covers only). Ask Josh for those galleries or files. 30 best flagged ★ in `_notes/VIOLA.md`.
- 1 Nov 2026: Stephens research done: 417 photos (~410 MB) in `_source/stephens/`, catalogue `_notes/STEPHENS.md` (61 galleries, ~16,700 photos on SmugMug; "Monk Headshots" gallery names 20 monks for sure; 30 best flagged; no Grotto photos, few school). All four research jobs done; next: job 5b (Get to know the monks), job 10 (picture pass), job 11 (photos page). Br. Augustine to check: who the bakers are; faces marked "unsure".
- 2 Nov 2026: job 5b done: "Get to know the monks" on `monastery/` (replaces the "Page being built" placeholder; vocations and oblates kept). 18 Stephens headshots + the Damien/Raphael first-vows photo (one joint card, since which is which is unsure), cropped 4:5 at 600x750 in `assets/img/monks/` (~1 MB); Br. Irenaeus, Br. Nicholas, Br. Boniface show "Photo to come". Text only from `_notes/MONKS.md`; left out what it marks unconfirmed (Br. Nicholas and the campus map, Br. Christopher's coffee). Styles in a `<style>` block in the page. Tested at 1440 and 390: no console errors, no sideways scroll, all images load. Br. Augustine to check: the cards' wording, Br. Leo's line (from the roster note), Fr. Bede's current work.
- 2 Nov 2026: jobs 2, 5, 6, 7 done: grotto/, pray/, school/, visit/ written; monastery/ gets an overview, a day in the life, history (with the 1891 founding story from Br. Augustine's Facebook export), formation and FAQ; give/ loses its placeholder. Name days added to the monk cards (Br. Augustine: put them in from the names; my choices for ambiguous names: Joel 19 Oct, John the Apostle, Thomas the Apostle, Damien of Molokai, Nicholas of Myra). Br. Nicholas drew the Bloomin' Festival campus map (the original campus map probably by Br. Nicholas Weiss). New photo grade `_notes/tools/grade.py` (warm, softened colour, ink blacks, cream whites, light vignette): the old choir photo is replaced by Anne Stephens's Palm Sunday 2022 choir, and the Br. Joseph statue regraded to match; new graded web copies for pray, school, visit (choir-nave, school-teaching, church-spring, church-night, cemetery). Left out the 2018 and 2024 group photos: Br. Joseph Goode may be in them. Buttons inside `.prose` were unreadable (link colour won): fixed in site.css (v=3). Tested at 1440 and 390: no errors, no sideways scroll, 151 internal links and anchors resolve. Waiting on: Br. Irenaeus's photo as a file (pasted in chat, not received as a file); Br. Christopher and "Benedictine Brew" coffee; photos of the novices. The Facebook export (FB.zip, Drive) covers only the "Bernard Abbey" profile Nov 2025–Nov 2026, five posts; the monks' posts on the abbey Page need an export of the Page itself.
- 2 Nov 2026: the whole Facebook Page read through the Graph API (1,022 posts, 1,146 photos): notes in `_notes/FACEBOOK.md`, texts in `_notes/facebook/`, tool `_notes/tools/fb_page_export.py` (token in the env var FB_PAGE_TOKEN; photos not in the repo). Monk cards corrected from it: name days as the abbey keeps them (Charles Lwanga, John Bosco, Thomas Aquinas, Joel 13 Jul, Pachomius 15 May, Benedict 21 Mar), Fr. Dominic prior (Aug 2026), Br. Christopher guestmaster, more on Brs. Leo, Michael, Irenaeus and Fr. Bede; Br. Irenaeus's photo; Br. Raphael and Br. Damien now separate cards; Br. Nicholas's 'Austin' was his baptismal name. Visit: Ed Huddleston's star-trail photo of the cemetery cross. Br. Augustine to settle the disagreements listed in FACEBOOK.md (his own birthplace, Fr. Patrick's and Br. Thomas's hometowns).
- 2 Nov 2026 (Br. Augustine): Fr. Bede is now Prior and Fr. Dominic Subprior (they switched); Br. Augustine was born in Pittsburgh; Fr. Patrick from Sheffield (ordained 2008); Abbot Brendan from Lanesville. Novices identified (Nicholas: auburn hair and beard; Boniface: red hair) and given photos: every monk on the site now has a picture.
- 2 Nov 2026: Br. Augustine sent Anne Stephens's March 2026 photos: new choir photos (home, pray) and a Vocations section with a picture for each stage (the belts and habits, the tonsure, the capuche at first vows; solemn vows: photo of the cuculla to come from Br. Augustine). Br. Gabriel cropped out of the novices' photo. To check: the number of pleats in the cuculla (Br. Augustine said 72, one per chapter of the Rule; the Rule has 73 chapters), not yet on the page.
- 2 Nov 2026: the two novices now share one card, with Anne Stephens's photo of them and Abbot Brendan behind (Br. Gabriel cropped out), as Br. Augustine asked.
- 2 Nov 2026 (Br. Augustine): there is no official scriptorium (Br. Leo edits and reprints the abbey's history books): wording fixed everywhere. Home trade tiles now plural (Builders, Heroes, Bakers, Scribes, Teachers); the Carver tile (no carpenter now) replaced by Heroes. New: work/#heroes (founders and Br. Maurus Lindner, Abbot Benedict Menges in the 1878 yellow fever, Fr. Urban Tracy and the lepers, Frater Hubert Carney in the 1918 flu, Fr. Patrick O'Neill's Carnegie Medal, Fr. Edward Markley, Br. Osmund's finger) and school/#teachers-past (the Capesius brothers, Fr. Benedict Oberdoerfer, Br. Wolfgang Wolf, Fr. Stephen Radtke, Fr. Patrick O'Neill, Fr. Malachy Shanaghan, Fr. Timothy Harrison, Fr. Aloysius Plaisance), all from the Necrology (psalter repo PDF, text via pdftotext). More stories there for later: Fr. Severin Laufenberg, Fr. Theodosius Osterrieder, chaplains in both world wars and Korea.
- 2 Nov 2026 (Br. Augustine): work/ gains Abbot Hilary among the Heroes (overcame alcohol addiction; AA), 'Men fully alive' (#alive: St. Irenaeus, Adv. Haer. IV.20.7; Br. Gus Campion, Br. John Bichler, Br. Vincent Kiefl, Br. Sebastian Alberti, Br. Placidus Schiesser, Fr. Damian Gusmus: room for every kind of man) and 'Scribes' (#scribes: Br. Wolfgang Wolf the botanist, Fr. Edward Stoeberl's choir books, Fr. Charles Fries's press, Abbot Ambrose Reger, Fr. Andrew Capesius, Fr. Aloysius Plaisance, Fr. Malachy Shanaghan, Br. Leo today). Home 'Scribes' tile links there. School: Fr. Michael Morgan replaces Br. Wolfgang among the teachers.
- 2 Nov 2026 (Br. Augustine): Fr. Patrick O'Neill's card keeps only his honours (no mention of his leaving and return); Abbot Hilary: only his AA work (not that he overcame addiction: unconfirmed); Br. Wolfgang's species named exactly as in his obituary (Talinum mengesii, T. appalachianum, Erythronium Harperi, E. Rostratum, Quercus Bernardianis, Quercus Capesii). Heroes gain 'Those who served': the chaplains and veterans of the Necrology, and Fr. Patrick Egan, Br. Michael and Br. Augustine today.
- 2 Nov 2026: the abbey Archives (three zips from Br. Augustine, see `_notes/ARCHIVES.md`): Br. Joseph at his worktable now on work/ and grotto/; archive portraits put faces on the Heroes, Men fully alive, Scribes, Those who served (work/) and Teachers we remember (school/), in `assets/img/past/`.
- 2 Nov 2026 (Br. Augustine): home tiles now Builders, Bakers, Scribes, Teachers, Heroes, Men fully alive (six across; on phones Heroes and Men fully alive are the last pair). The Men fully alive tile is Br. John Bichler in his cook's whites (archives).
- 2 Nov 2026: Arc.zip (12 archive photos; 'Monks at Prayer-web' carries a HistoricImages watermark: not used). New section pray/#church 'The Abbey Church': square sandstone outside, pointed arches and carved saints inside; native sandstone quarried on the grounds (ADAH); finished 1964 under Abbot Bede (Cullman Tribune 2023; Necrology); statues by Herbert Jogerst (former POW, St. Meinrad), Br. Jude his apprentice; the Great Cross by Gloria Thomas, restored 2024 by Gary Chapman (CNHI). Architect not found anywhere: ask the archives. monastery/#history gains four 'then' photos (monks c. 1900, the college c. 1900, solemn vows 1937, the old chapel 1950s).
- 2 Nov 2026 (Br. Augustine): home 'Pray with us' picture is now a then-and-now pair: the monks in the old chapel in the 1950s and the monks in choir in 2013, seen from behind (Archives, Arc.zip). choir.jpg (Stephens, 2026) stays on pray/.
- 2 Nov 2026: monastery/#wider-church 'A small abbey, in good company': Abbot Cletus with Pope Francis (Congress of Abbots, Rome 2016), Abbot Hilary with St. John Paul II, Abbot Hilary with Mother Angelica (1982), Abbot Bede and Fr. Brian Egan with Robert F. Kennedy in the old gym (five photos from Br. Augustine's Drive; the second Mother Angelica photo is ready as church-world/angelica-2.jpg). The papal photos are probably by the Vatican's photographers: ask the archives whether a credit is owed.
- 2 Nov 2026: the archive faces (work/, school/) open a larger portrait when clicked or tapped (lightbox in site.js v3; full images in assets/img/past/full/). Famous visitors: searched Facebook, the Necrology and the web: no record found of Ozzy Osbourne or of a soccer team training here; found Cardinal Samuel Stritch of Chicago (preached at Abbot Boniface Seng's golden jubilee, 1947; visited Cullman with Chicago dignitaries) and an Ernie Pyle column on the Grotto, 1939 (NRHP note; column not found). Ask the archives/old monks for the soccer team and Ozzy stories with a date.
- 2 Nov 2026: new page history/ 'A history in dates' (1846–2026, seven eras; from the Necrology, the archives' school history, Facebook 2010–26, EOA, NRHP), linked from monastery/#history and every footer. Abbot Brendan and the farm: reopened 2014, first calf Dec 2014 (Facebook), on his card and work/ farm card. Frater Hubert died 13 Oct 1918, the day of his deathbed vows (Necrology table): Heroes card corrected.
- 2 Nov 2026: school/ 'The monks at the school' cards get faces too (assets/img/monks/face/, cut from the Stephens portraits; tap opens the full portrait).
- 2 Nov 2026 (All Souls): relics/#witnesses 'A great cloud of witnesses': Heb 12:1–2; CCC 955 and 958; the cemetery as a living family (Necrology read at supper on the eve of each anniversary, funerals with Vespers of the Dead, All Souls procession), 'we do not call them saints; that judgement belongs to the Church', links to Heroes and Men fully alive. Photos: Stephens cemetery and chapel (cemetery-rows, -autumn, -snow, -funeral).
- 2 Nov 2026 (Br. Augustine): main menu kept simple: The Grotto, The School, Pray with Us, Visit, Give (Monks at Work taken out). Deeper pages are reached from the home page and the footer: the monks section now ends 'not only craftsmen and teachers…' with 'Meet the monks at work' and 'The heroes of our house'; a new home section '135 years on this hill' has 'Learn more about our history' (history/) and 'Popes, Mother Angelica and a Kennedy' (monastery/#wider-church).
- 3 Nov 2026 (Br. Augustine): choir photos with Br. Augustine in them taken out; Pray with Us now uses the 2016 and 2017 choir photos from the archives (before he entered).
- 3 Nov 2026: saints' portraits on the relic cards (small round image in each saint's name; tap opens it): lead images of each saint's Wikipedia article from Wikimedia Commons, public domain or free licence, credits in relics/SAINT-IMAGES.md. Wikimedia rate-limits this session hard (Retry-After up to 600 s): downloads continue in batches; rerun _notes/tools/saints_build.py when more arrive (it adds only missing ones). No image for: Radegund, Contardo d'Este, the Beatrices d'Este, Valerius, John Berchmans; ambiguous labels deliberately left without.
