/**
 * "Suggest a change" receiver, a Google Apps Script web app (no server, no Supabase). The floating button on the abbey site
 * (assets/suggest.js) posts a note and a screenshot here; this script saves the screenshot in a Google Drive folder and opens
 * an issue on GitHub (munkachy/newmonksite, label "suggestion") with the note, the page link and the picture.
 * If GitHub can't be reached, it emails the note to whoever owns this script, so nothing is lost.
 *
 * Set-up (about five minutes, see README.md in this folder):
 *   1. script.google.com > New project > paste this file.
 *   2. Project Settings > Script properties > add  GITHUB_TOKEN  = a fine-grained GitHub token for munkachy/newmonksite only,
 *      permission "Issues: Read and write" (nothing else). The token lives only here, never on the website or in the repo.
 *   3. Deploy > New deployment > type Web app > Execute as: Me > Who has access: Anyone > Deploy. Allow the permissions it asks for
 *      (Drive, external requests, mail). Copy the /exec address and give it to Claude (it goes in ENDPOINT in assets/suggest.js).
 * After changing this file: Deploy > Manage deployments > edit > New version (the address stays the same).
 */
var REPO = "munkachy/newmonksite";
var FOLDER = "Abbey site suggestions (screenshots)";

function doPost(e) {
  try {
    var b = JSON.parse(e.postData.contents);
    if (b.website) return out_({ ok: true, issue: 0 });                      // honeypot: pretend it worked
    var message = clip_(b.message, 4000).trim();
    if (message.length < 3) return out_({ ok: false, error: "empty" });
    if (tooMany_()) return out_({ ok: false, error: "slow down" });

    var name = clip_(b.name, 100).trim(), page = clip_(b.page, 500), title = clip_(b.title, 200);
    var viewport = clip_(b.viewport, 20), agent = clip_(b.agent, 300), scroll = Number(b.scroll) || 0;

    var shotUrl = "", shotId = "";
    var shot = String(b.screenshot || "");
    if (shot.indexOf("data:image/jpeg;base64,") === 0 && shot.length < 2000000) {
      try {
        var bytes = Utilities.base64Decode(shot.split(",")[1]);
        var stamp = Utilities.formatDate(new Date(), "America/Chicago", "yyyy-MM-dd HHmmss");
        var file = folder_().createFile(Utilities.newBlob(bytes, "image/jpeg", stamp + " " + Utilities.getUuid().slice(0, 6) + ".jpg"));
        file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
        shotId = file.getId();
        shotUrl = "https://drive.google.com/thumbnail?id=" + shotId + "&sz=w1600";
      } catch (err) { /* the note still goes through without the picture */ }
    }

    var lines = [message, "", "---",
      "**Page:** " + page, title ? "**Title:** " + esc_(title) : "", "**From:** " + (name ? esc_(name) : "anonymous"),
      "**Screen:** " + (viewport || "?") + ", scrolled " + scroll + "px", "**Browser:** " + esc_(agent), "",
      shotUrl ? "![Screenshot of where they were](" + shotUrl + ")\n\n[Open the screenshot](https://drive.google.com/file/d/" + shotId + "/view)" : "_No screenshot._"];
    var body = lines.filter(function (x) { return x !== ""; }).join("\n");
    var first = message.split("\n")[0].slice(0, 70);

    var token = PropertiesService.getScriptProperties().getProperty("GITHUB_TOKEN");
    var r = UrlFetchApp.fetch("https://api.github.com/repos/" + REPO + "/issues", {
      method: "post", muteHttpExceptions: true, contentType: "application/json",
      headers: { Authorization: "Bearer " + token, Accept: "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "abbey-suggest" },
      payload: JSON.stringify({ title: "Suggestion: " + first, body: body, labels: ["suggestion"] })
    });
    if (r.getResponseCode() >= 300) {
      MailApp.sendEmail(Session.getEffectiveUser().getEmail(), "Abbey site suggestion (GitHub did not take it)", body + "\n\nGitHub said: " + r.getResponseCode() + " " + r.getContentText().slice(0, 300));
      return out_({ ok: true, issue: 0 });
    }
    return out_({ ok: true, issue: JSON.parse(r.getContentText()).number });
  } catch (err) {
    return out_({ ok: false, error: "error" });
  }
}

function doGet() { return out_({ ok: true, hello: "abbey suggestion box" }); }

function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function clip_(s, n) { return String(s == null ? "" : s).replace(/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/g, "").slice(0, n); }
function esc_(s) { return String(s).replace(/([\\`*_{}\[\]<>#|])/g, "\\$1"); }
function folder_() {
  var it = DriveApp.getFoldersByName(FOLDER);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER);
}
// a best-effort limit: 40 suggestions an hour for the whole site
function tooMany_() {
  var c = CacheService.getScriptCache(), n = Number(c.get("hits") || 0);
  if (n >= 40) return true;
  c.put("hits", String(n + 1), 3600);
  return false;
}
