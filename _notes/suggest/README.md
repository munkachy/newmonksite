# "Suggest a change" button

A floating button on every abbey-site page (`assets/suggest.js`). It takes a picture of what the person was looking at
(html2canvas, in their browser), asks what they would change, and sends the note and picture to a small Supabase Edge
Function (`index.ts` here), which opens an issue on GitHub (munkachy/newmonksite, label `suggestion`) with the page, screen
size and the picture. Anyone can use it (the monks, Fr. Paschal, a visitor): no account needed.

## To switch it on
1. GitHub: Settings → Developer settings → Fine-grained tokens → one for **munkachy/newmonksite only**, permission
   **Issues: Read and write** (nothing else). Put it in Supabase as the secret `GITHUB_TOKEN`; never in the repo.
2. Supabase: a public Storage bucket `suggestion-shots`, and deploy `index.ts` as `abbey-suggest` with Verify JWT off.
3. Put the function's address (`https://<project>.supabase.co/functions/v1/abbey-suggest`) in `ENDPOINT` at the top of
   `assets/suggest.js` and bump its `?v=`. With no address the button does not appear.

## Reading the suggestions
`gh issue list --label suggestion` or the Issues tab; each issue shows the note, the page link and the screenshot.
Close an issue when it is done or declined.
