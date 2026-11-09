# "Suggest a change" button (BugDrop)

Every page ends with BugDrop's widget (https://bugdrop.dev, MIT, hosted free on Cloudflare by its makers):

    <script src="https://bugdrop.neonwatty.workers.dev/widget.v1.59.1.js" data-repo="munkachy/newmonksite" data-show-name="true" data-label="Suggest a change" data-position="bottom-right" data-color="#004069"></script>

Anyone (no login) taps the button, writes a note, optionally gives a name, and BugDrop opens an issue in munkachy/newmonksite
(labels `bugdrop` plus Bug / Feature / Question) with a screenshot taken in their browser. Screenshots are stored in this repo on
the branch `bugdrop-screenshots` (folder `.bugdrop/`), which the site never serves. Suggestions are public, like the repo.

Needs the BugDrop GitHub App installed on this repo only (github.com/marketplace/bugdrop-in-app-feedback-to-github-issues >
Only select repositories > munkachy/newmonksite). The app can write issues and repository contents; uninstall it to switch the
button off for good (and remove the script line). Limits: 10 sends per visitor per 15 minutes, 50 per hour for the site.
Do not add async/defer to the tag. To read them: the Issues tab, label `bugdrop`.
