# New St. Bernard Abbey website: plan and hand-off

A new version of stbernardabbey.com (now on Wix), built here as plain HTML, CSS and JS: no build step, no libraries,
**relative paths** (so it works at `munkachy.github.io/newmonksite/` now and at the domain root later), the same way
as the `munkachy/sbp` site. Br. Augustine, OSB (webmaster) asked for it on 1 Nov 2026.

**Anyone picking this up (another Claude account or session):** read this file first, then `_notes/`. Work on branch
`claude/saint-photo-identification-ksp79d` (PR #1 in munkachy/newmonksite). `git pull` before you start and before
you push; commit and push after every finished piece, and tick it off below with a line in the log at the bottom.
Take one job at a time, mark it `[~] taken (date, who)` and push that mark first so two accounts don't do the same job.
If a job marked taken has had no commit for two hours, the session that took it has probably hit a limit: take it over.

## What Br. Augustine asked for

1. **Theme: a tradition of craftsman monks.** Br. Joseph Zoettl (Ave Maria Grotto) is only the most famous; feature
   him much more, and show the others (Br. Jude Johnston, Br. Nicholas, and the rest; see `_notes/CRAFTSMEN-public.md`).
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
6. Look at the Ave Maria Grotto site and its gift shop (facts in `_notes/CRAFTSMEN-public.md`).

## Decisions (keep to these unless Br. Augustine says otherwise)

- **Look**: St. Michael's calm: full-width warm photography, a thin elegant serif for headings, cream paper, deep
  ink text, one muted gold accent (dark enough to read on cream; never gold text on cream for body copy), black-and-
  white close-ups of hands at work for the craft sections. Fonts from Google Fonts (the sbp Adobe kit is licensed to
  the school only): **Cormorant Garamond** (headings) and **Source Sans 3** (text). Crest: `_source/abbey-img/logo.jpg`.
- **Navigation**: The Grotto · Monks at Work · The School · Pray with Us · Visit · ♥ Give (pill). Utility line above:
  today's Grotto hours and the next prayer time (computed in JS from the tables below, Central time).
- **Home page order**: (1) hero: silent loop `media/hero-720/1080.mp4` (24 s, cut from the film; pause button;
  still `media/film-still-33.jpg` for reduced motion) with the abbey's name and one line; (2) "Two works, one house":
  equal cards for the Grotto and the Prep; (3) Monks at work: Br. Joseph first, then the strip "A Builder / A Carver /
  A Baker / A Scribe / A Teacher"; (4) the film (sbp tour pattern; `media/film-720.mp4`, 8:30, poster
  `media/film-still-436.jpg`); (5) Pray with us: live "now / next" schedule; (6) the relics: one image and a link;
  (7) three asks in this order: let us pray for you, is God calling you, support the monks; (8) footer.
- **Pages** (one folder each, `index.html` inside): `grotto/`, `work/` (monks at work / craftsmen), `school/`,
  `monastery/` (the monks, daily life, history, vocations, oblates), `pray/` (schedule, Divine Office), `relics/`,
  `visit/` (Grotto visit, retreat center, directions), `give/` (Donorbox, will, Mass intentions, Clairvaux Society).
  Shared: `assets/site.css`, `assets/site.js`, `assets/img/` (web-sized images, ≤ 1800 px, JPEG q≈80).
- **Facts**: only from `_notes/ABBEY-FACTS.md`, `_notes/CRAFTSMEN-public.md`, `relics/README.md` or a cited public
  source. Never quote the Necrology without the abbot's approval. Mark anything uncertain for Br. Augustine.
- **Don't**: animations that hide content when JS is off, pop-ups, carousels, dated widgets that go stale, 24-hour
  times. Test at 1440 and 390 wide, light only, no console errors, no sideways scroll (see sbp CLAUDE.md "Testing").

## Jobs

Jobs 2–8 can run in parallel once job 1 is pushed (they share only `assets/site.css`; add page-specific styles at the
end of it under a comment with your page's name, or in a `<style>` block in your page, to avoid merge conflicts).

- [x] **1. Foundation** (`assets/site.css`, `assets/site.js`, header/footer, home page `index.html`). Done 1 Nov 2026.
  Every section folder has a starter `index.html` with the shared header and footer: replace its `<main>` with the
  real page. Images in `assets/img/` (see the list in `assets/img/README.md`).
- [ ] **2. The Grotto** (`grotto/`): Br. Joseph's life, the miniatures, visiting info, shop link, Library of Congress
  photos (`_notes/research-img/`, credits in its `CREDITS.md`).
- [~] **3. Monks at Work** *(taken by the first session, 1 Nov 2026)* (`work/`): Br. Joseph, Br. Jude, the craftsmen of the past (names only where public; the
  Necrology names marked "to confirm"), and the works of today: bakery, woodworks, Scriptorium, farm, Grotto, school.
- [x] **4. Relics**: done 1 Nov 2026. Cards built by a script from `_notes/relic-groups.json` (cover = first photo of each
  group, `assets/img/relics/`); when the photographer's pictures come, replace `assets/img/relics/<group-id>.jpg`, drop
  the "Placeholder photo" badges, and put the altar long shot in the dashed `.altar-slot`. (`relics/index.html`): from `_notes/relic-groups.json` and `relics/README.md`: groups as cards
  (placeholder photo marked "Photo to come"), each with its saints; a slot for the long shot on the altar.
  Make web copies of the chosen photos in `assets/img/relics/`. Keep `relics/README.md` as the full catalogue.
- [ ] **5. The monastery and prayer** (`monastery/`, `pray/`): the monks (9 profiles in
  `_source/abbey-pages/monk-profiles.md`), a day in the life, formation, FAQ (visible, not hidden), oblates,
  history (Metten → St. Vincent → 1891), the abbots, the live schedule.
- [ ] **6. Visit and Give** (`visit/`, `give/`).
- [ ] **7. The School** (`school/`): a short page on St. Bernard Prep as a work of the monks, linking to
  stbernardprep.com (and to the sbp preview when it goes live).
- [ ] **8. Pictures**: choose the best photos in `_source/abbey-img/` (see its `INDEX.md`) for each page, make web
  copies in `assets/img/`, and list each with its page in `assets/img/README.md`.
- [ ] **9. Check everything**: Playwright at 1440 and 390, every link, then a short report for Br. Augustine.

## For Br. Augustine to decide or supply

- Permission to use photos of Br. Joseph (Grotto archive, ADAH, Troy University) and to quote the Necrology.
- Who drew the campus map ("Br. Nicholas", living), and which living monks are craftsmen today.
- The 78-second trailer on YouTube (`9HsUwl-Prf0`) could not be downloaded here; the full film is used instead.
- Whether the site keeps Donorbox for gifts.

## Log

- 1 Nov 2026: research done (abbey site crawled: `_source/`; monastery sites: `_notes/MONASTERIES.md`; craftsmen:
  `_notes/CRAFTSMEN-public.md`); film re-encoded (`media/film-720.mp4`, 53 MB), hero loop cut (`media/hero-*.mp4`),
  stills (`media/film-still-*.jpg`). Plan written. Starting job 1.
- 1 Nov 2026: job 1 done: home page (hero loop, two works, craftsman monks, the film, prayer times live in Central
  time, relics, three asks), shared CSS/JS, starter pages. Tested at 1440 and 390: no console errors, no sideways
  scroll. Preview: serve the parent folder (`cd .. && python3 -m http.server 8770`), open /newmonksite/.
- 1 Nov 2026: job 4 done (relics page, 14 reliquaries, all 122 photos as thumbnails linking to the labeled copies). Job 3 taken.
