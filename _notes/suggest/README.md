# "Suggest a change" button

A floating button on every abbey-site page (`assets/suggest.js`). It takes a picture of what the person was looking at
(html2canvas, in their browser), asks what they would change, and sends the note and picture to a small **Google Apps Script**
(`suggest.gs` here; no server, no Supabase). The script saves the picture in a Google Drive folder and opens an issue on
GitHub (munkachy/newmonksite, label `suggestion`) with the note, the page link, the screen size and the picture. Anyone can use
it (the monks, Fr. Paschal, a visitor): no account needed. If GitHub is down, the note is emailed to the script's owner.

## To switch it on (about five minutes)
1. **GitHub token.** github.com > Settings > Developer settings > Fine-grained tokens > Generate. Repository access: only
   `munkachy/newmonksite`. Permissions: **Issues: Read and write** (nothing else). Copy it once.
2. **The script.** script.google.com > New project, name it "Abbey suggestions", paste all of `suggest.gs`. Project Settings (gear) >
   Script properties > Add `GITHUB_TOKEN` with the token. Never put the token anywhere else.
3. **Publish it.** Deploy > New deployment > gear > Web app. Execute as **Me**, who has access **Anyone**. Deploy, then allow the
   permissions (Drive, external requests, mail). Copy the web app address (ends in `/exec`).
4. Give the address to Claude, who puts it in `ENDPOINT` at the top of `assets/suggest.js` and publishes. With no address the button does not appear.

## Reading the suggestions
`gh issue list --label suggestion`, or the Issues tab on GitHub; each issue has the note, a link to the page and the screenshot
(the pictures are in the Drive folder "Abbey site suggestions (screenshots)"). Tell Claude "look at the suggestions" and it reads them,
makes the changes and closes each issue when done.

## Notes
- The screenshot is of the visible part of the page, taken in the visitor's browser before the box opens. The sticky top bar and
  the background video are not always drawn exactly; the page address, screen size and scroll position are in the issue.
- Anyone who knows the address could send a note, so there is a hidden spam trap and a limit of 40 an hour for the whole site.
