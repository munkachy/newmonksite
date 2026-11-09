# newmonksite
## Publishing (GitHub Pages)
Every push to `main` publishes the site in one to two minutes ("pages build and deployment" in the Actions tab).
A new push cancels a deploy still running, so batch small edits into one push. GitHub's own "Deploy to GitHub Pages" step
sometimes hangs for ten minutes and fails (it did three times on 9 Nov 2026); a re-run can sit queued, and the next push to
`main` publishes everything anyway.
