# The abbey's Facebook Page: what is in it (read 2 Nov 2026)

The whole Saint Bernard Abbey Page (facebook.com/stbernardabbey, Page id 365859886608) was read through the Graph API
on 2 Nov 2026 with `_notes/tools/fb_page_export.py`: **1,022 posts (Feb 2010 – Nov 2026) and 1,146 photos**.
Texts are kept here, in `_notes/facebook/posts.json` (date, text, link, photo ids) and `_notes/facebook/photos.json`
(date, caption, album, link, file name). The photo files themselves (263 MB) are **not** in the repo (size limit); rerun
the tool to fetch them (`img/<date>_<photo id>.jpg`, the names in photos.json).

## Running it again (any session)

- Needs a token. Br. Augustine stores a long-lived one as the environment variable **FB_PAGE_TOKEN** in the cloud
  environment's settings (never paste tokens into chat or commit them). A user token works too: the tool asks Facebook
  for the Page's own token.
- Making a token: Graph API Explorer (developers.facebook.com/tools/explorer), app "Crawler", permissions
  `pages_show_list`, `pages_read_engagement` **and `business_management`** (the Abbey Page sits in a Meta business
  portfolio: without it the Page is not offered), Generate Access Token, tick the business and the Page.
  `pages_read_user_content` cannot be selected and is not needed. Extend it to ~60 days with the Access Token
  Debugger's "Extend Access Token"; a Page token taken from an extended user token does not expire.
- `FB_PAGE_TOKEN=... python3 _notes/tools/fb_page_export.py OUT_DIR` (resumes; `--since YYYY-MM-DD` for recent only).

## What is there

Posts per year: 2010 53 · 2011 9 · 2012 37 · 2013 82 · 2014 69 · 2015 95 · 2016 100 · 2017 38 · 2018 17 · 2019 41 ·
2020 72 · 2021 67 · 2022 43 · 2023 119 · 2024 74 · 2025 56 · 2026 50. Albums: Photos (799), Mobile uploads (134),
Cover photos (76), **Meet the Monks Mondays (33)**, Simple Profession of Brother Andrew (27), Monks in the Snow (20),
Monks at Bloomin' Fest 2013 (18), Triduum and Easter 2016 (17), Remembering Br. Augustine Campion (12), New Postulants (6).

Kinds of post: **name-day posts** for each monk (2023–2026, a paragraph on the saint and one on the monk: the best
current biographical source); **Meet the Monks Mondays** (Oct 2013 – Jan 2015: hometown, profession and ordination
dates, office); **death notices and funeral arrangements** for monks; vows, clothing, ordinations, abbatial election
(29 Jul 2026), prior named (7 Aug 2026); history ("Happy 135th birthday", 29 Sep 2026: the 1891 election of Abbot
Benedict Menges); liturgy schedules; school, Grotto, Bloomin' Festival and Blues & BBQ notices; photos credited to
Anne Stephens, Joshua Viola and Ed Huddleston (night sky).

Not found: anything about coffee or "Benedictine Brew" (Br. Christopher: unconfirmed).

## Name days (as the abbey keeps them; now on the monk cards)

Brendan 16 May (the Navigator) · Cletus 26 Apr · Marcus 25 Apr · Joel 13 Jul (the prophet) · Charles 3 Jun
(**Charles Lwanga**) · John 31 Jan (**John Bosco**) · Leo 10 Nov (Leo the Great) · Bede 25 May · Patrick 17 Mar ·
Michael 29 Sep · Benedict 21 Mar (the Transitus) · Thomas 28 Jan (**Aquinas**) · Linus 23 Sep · Irenaeus 28 Jun ·
Christopher 25 Jul · Dominic 8 Aug · Paschal 17 May (Baylon) · Pachomius 15 May · Augustine 28 Aug · Raphael 29 Sep ·
Damien 10 May (**of Molokai**) · Nicholas 6 Dec (of Myra) · Boniface 5 Jun.

## New facts about the monks (posts 2024–2026)

- **Fr. Dominic Lee named Prior**, announced after Compline 7 Aug 2026 (Facebook). **Since then Fr. Bede Marcy and Fr. Dominic have switched: Fr. Bede is Prior, Fr. Dominic Subprior** (Br. Augustine, 2 Nov 2026). Fr. Dominic is still assistant headmaster (discipline) and teaching.
- **Br. Christopher McBride** (Montgomery, AL; vows 16 Aug 2014): guestmaster (2026); earlier ran the cookie business,
  kept the chickens and was the community's mailman.
- **Br. Michael Gregersen** (New Orleans; Air Force; vows 21 Mar 2006): sacristan for many years.
- **Br. Irenaeus Ceballos**: in the U.S. 29+ years; citizen 15 Nov 2015; BA Philosophy, St. John Vianney College,
  Miami; seminarian for Palm Beach; 2½ years at St. Leo Abbey; postulant Jan 2013; vows 12 Feb 2014; grounds and maintenance.
- **Br. Leo Borelli** (Decatur, AL; vows 21 Mar 1986): former prior and novice master; hermit; keeps vigil over the
  cemetery; teaches Latin at the Prep; editor of reprints such as Reger's *The Benedictines in Alabama*.
- **Fr. Bede Marcy** (Biloxi, MS; vows 21 Mar 2002; priest 2 May 2009): dining hall manager, theology at the Prep.
- **Br. Raphael Ray** (Lebanon, TN) and **Br. Damien Jackson** (Anniston, AL): simple vows 21 Mar 2026; Raphael
  teaches civics and PE at the Prep. Novices 2025: Damien, Anthony, Raphael (Br. Anthony not on the 2026 roster).
- **Novices** clothed 21 Mar 2026: Austin Smith → Br. Nicholas; Timothy Boland → Br. Boniface; Michael Maddox → Br.
  Gabriel (has left). So "Austin" on the roster is Br. Nicholas's baptismal name, not his birthplace.
- **Fr. Joel Martin**: Emory 1972; St. Meinrad MA and M.Div.; taught at the Prep 1991–95, headmaster 15+ years,
  president 2013; vocation director and choirmaster.
- **Br. Benedict Dyar**: head baker, "a skilled chanter", oblate director.
- **Fr. Paschal Pautler**: St. Rose Academy (Nashville Dominicans); led the recent fundraising; development director.

## Disagreements (settled by Br. Augustine, 2 Nov 2026, unless marked open)

- Br. Augustine: the name-day posts say **born in Pittsburgh**, grew up in Dayton, San Angelo, the Azores and Wichita
  Falls; the Cullman Tribune (2021) says born in Prattville. **Settled: born in Pittsburgh** (Prattville is where his parents live). Card: Pittsburgh.
- Fr. Patrick Egan: Meet the Monks (2014) gives hometown **Sheffield**, AL (the card: Florence), professed 21 Mar 2003,
  **ordained 2 Jun 2008** (so 5 Jun 2006 was his solemn vows, not ordination). **Settled: as the 2014 post says.** Card: Sheffield.
- Br. Thomas Jones: 2014 hometown **Jasper**, AL (the card: Homewood, where he was born). **Open.**
- Fr. Linus: 2014 hometown Buffalo, NY; 2023–26 posts and the card: Allentown, PA. Card kept (recent posts).
- Abbot Brendan: name-day posts say New Albany, IN; the abbey's election notice and the card: Lanesville, IN. **Settled: Lanesville.**

## Meet the Monks Mondays (2013–2014), for the history pages

Abbot Cletus (Cleveland TN; prof. 4 Jul 1965; ord. 24 May 1971; abbot 8 May 1995, re-elected 15 May 2009) ·
Fr. Kevin McGrath (Nashville; 1968/1974; stipendarius) · Fr. John O'Donnell (Philadelphia; prof. 21 Mar 1982; ord.
24 Oct 1998; subprior) · Abbot Victor Clark (Cullman; prof. 18 Jun 1949; ord. 5 Jun 1954; 8th abbot 22 May 1987) ·
Fr. Howard Moussier (El Paso; 1959/1965) · Fr. Edward Markley (Atlanta; 1960/1966; pastor St. Michael's) ·
Br. Augustine Campion (Malvern PA; 1964; Grotto shop, mailman, purchaser) · Fr. Marcus Voss (Cullman; 1964/1971) ·
Br. Joseph Weiss (Chicago; 1964; gardens) · Br. Charles Manning (Knoxville; 1971) · Fr. Joel Martin (Fitzgerald GA;
prof. 21 Mar 1986; ord. 27 May 1991) · Br. Leo Borelli (Decatur AL; 1986; prior, novice master) · Fr. Francis Reque
(Minneapolis; 1995/2000; librarian, historian) · Br. Peter Le (Quinhon, Vietnam; 2001; tailor, barber) · Fr. Bede
Marcy (Biloxi; 2002/2009) · Fr. Patrick Egan (Sheffield AL; 2003/2008) · Br. Brendan Seipel (New Albany IN; 2004;
guest master) · Br. David Bryant (Knoxville; 2004; candle shop) · Br. Michael Gregersen (New Orleans; 2006; sacristan) ·
Fr. Jacob Amos (San Francisco; 2006/2011) · Br. Benedict Dyar (Opelika; 15 Aug 2008) · Br. Anselm Kuehler (Dallas;
2009) · Br. Bernard Denson (Gadsden; 2010) · Br. Martin Weidner (St. Louis; 2010) · Br. Thomas Jones (Jasper AL; 15 Aug
2011) · Br. Linus Klucsarits (Buffalo NY; 8 Jan 2012) · Br. Marion Sanchez (Spring Valley IL; 2013) · Br. Ambrose
Steele (Memphis; 2014) · Br. Irenaeus Ceballos (Buenos Aires, Colombia; 12 Feb 2014) · Br. Raphael Pattarozzi
(Morrisonville IL; 2014) · Br. Christopher McBride (Montgomery AL; 16 Aug 2014) · Novices Dominic Lee and Paschal Pautler
(entered 14 Aug 2014).

## Deaths announced on the Page

Br. Johnpaul (25 Feb 2010) · Br. André Couture (1931–22 Oct 2013) · Br. Joseph Weiss (28 Apr 1930–28 May 2015) ·
Br. Anselm Kuehler (Jan 2016) · Br. Augustine "Gus" Campion (Sep 2017) · Fr. Edward Markley (Jan 2019) · Fr. Howard
Moussier (Jan 2019) · Fr. Kevin McGrath (Nov 2019) · Br. Marion Sanchez (Feb 2021) · Abbot Victor Clark (1930–Jan 2024;
funeral photos by Joshua Viola) · Br. Jude Johnston (Jun 2025). Also a 2016 post explaining the monks' custom of reading
a death notice at supper on each anniversary.

## Photos

Used on the site (2 Nov 2026): Br. Irenaeus walking (2025-06-28 name-day post; `assets/img/monks/irenaeus.jpg`); the
cemetery cross under star trails by **Ed Huddleston** (2025-09-11; `assets/img/cemetery-stars.jpg`, credited). The
2025 and 2026 posts also identified **which junior is which** in Anne Stephens's first-vows photo (Raphael left,
Damien right), so each now has his own card.

Worth using later (files by name in photos.json): the cattle in the pasture (2024-07-24, Anne Stephens, also on
SmugMug); the cemetery and campus in snow (2025-01-10); the northern lights over the abbey (2025-11-19, Ed Huddleston);
the restoration of the great crucifix (2024-07-23); archival black-and-white portraits of Abbot Victor (2024-01-29);
the many 2023–2026 name-day portraits (most are Anne Stephens's headshots, already used). The novices' clothing photos
(2026-03-23) carry no names and include Br. Gabriel (dark hair and beard; Br. Augustine): Br. Nicholas is the one with auburn hair and a full beard, Br. Boniface the clean-shaven red-haired one (Br. Augustine, 2 Nov 2026). Their cards use crops of their family photos (2026-03-23). Group photos from 2024–2026 may
include Br. Joseph Goode or Br. Gabriel: check before using. Ask Ed Huddleston before using more of his photos.
