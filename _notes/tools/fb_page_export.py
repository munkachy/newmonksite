"""Download every post and every photo of a Facebook Page you manage, with captions, at full size.

Uses Facebook's Graph API, the official way for a Page's admins to read their own Page.

1. Get a Page access token (it lasts about an hour, which is enough):
   - Go to https://developers.facebook.com/tools/explorer/ (log in as a Page admin; if it asks, create a free
     "app" of type Business, then choose it in the Explorer).
   - Under "User or Page", choose "Get Page Access Token" and pick Saint Bernard Abbey.
   - Add the permissions pages_read_engagement and pages_show_list, then "Generate Access Token" and copy it.
2. Run (the token is read from the environment and never printed or saved):
       FB_TOKEN='...' python3 _notes/tools/fb_page_export.py OUT_DIR
   Optional: --since 2015-01-01 to limit the date range.

Writes OUT_DIR/posts.json (every post: date, text, link, the photos it carries), OUT_DIR/photos.json (every
uploaded photo: date, caption, album, link) and OUT_DIR/img/<date>_<photo id>.jpg (largest size Facebook keeps).
Run it again to resume: photos already downloaded are skipped. Keep OUT_DIR out of the repo (it is the raw source).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.facebook.com/v21.0/"


def get(path_or_url, token, **params):
    if path_or_url.startswith("http"):
        url = path_or_url  # a "next" link already carries its own parameters and token
    else:
        params["access_token"] = token
        url = API + path_or_url + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503) and attempt < 4:
                time.sleep(5 * (attempt + 1)); continue
            # never echo the URL: it contains the token
            sys.exit(f"Facebook said {e.code}: {body[:400]}")
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(5 * (attempt + 1)); continue
            raise


def every(path, token, **params):
    page = get(path, token, **params)
    while True:
        for item in page.get("data", []):
            yield item
        nxt = page.get("paging", {}).get("next")
        if not nxt:
            return
        page = get(nxt, token)
        time.sleep(0.3)


def largest(images):
    return max(images, key=lambda i: i.get("width", 0) * i.get("height", 0))["source"] if images else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--since", help="YYYY-MM-DD: only posts and photos from this date on")
    a = ap.parse_args()
    token = os.environ.get("FB_TOKEN")
    if not token:
        sys.exit("Set FB_TOKEN to a Page access token (see the top of this file).")
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)
    extra = {"since": a.since} if a.since else {}

    me = get("me", token, fields="id,name")
    print(f"Page: {me.get('name')} ({me.get('id')})")

    # 1. Every uploaded photo, with caption and every size; keep the largest.
    photos = []
    for p in every("me/photos", token, type="uploaded", limit=100, **extra,
                   fields="id,name,created_time,link,album{name},images"):
        photos.append({"id": p["id"], "date": p.get("created_time"), "caption": p.get("name", ""),
                       "album": (p.get("album") or {}).get("name"), "link": p.get("link"),
                       "src": largest(p.get("images", []))})
        if len(photos) % 100 == 0:
            print(f"  {len(photos)} photos listed")
    print(f"{len(photos)} photos")

    # 2. Every post, with its text and the photo ids it carries.
    fields = ("id,created_time,message,permalink_url,"
              "attachments{media_type,target{id},subattachments.limit(100){media_type,target{id}}}")
    posts = []
    for p in every("me/posts", token, limit=50, fields=fields, **extra):
        ids = []
        for att in (p.get("attachments") or {}).get("data", []):
            for s in [att] + (att.get("subattachments") or {}).get("data", []):
                if s.get("media_type") == "photo" and s.get("target", {}).get("id"):
                    ids.append(s["target"]["id"])
        posts.append({"id": p["id"], "date": p.get("created_time"), "text": p.get("message", ""),
                      "link": p.get("permalink_url"), "photos": list(dict.fromkeys(ids))})
    print(f"{len(posts)} posts")

    # Photos in posts that were not in the uploaded list (e.g. shared albums): fetch their sizes too.
    known = {p["id"] for p in photos}
    for pid in {i for p in posts for i in p["photos"]} - known:
        d = get(pid, token, fields="id,name,created_time,link,images")
        if "images" in d:
            photos.append({"id": pid, "date": d.get("created_time"), "caption": d.get("name", ""),
                           "album": None, "link": d.get("link"), "src": largest(d["images"])})

    # 3. Download. File names: date + photo id, so they sort by date and match photos.json.
    done = 0
    for p in photos:
        if not p["src"]:
            continue
        name = f"{(p['date'] or 'undated')[:10]}_{p['id']}.jpg"
        p["file"] = "img/" + name
        dest = os.path.join(a.out, "img", name)
        if os.path.exists(dest):
            continue
        try:
            urllib.request.urlretrieve(p["src"], dest)
            done += 1
        except Exception as e:  # one bad photo should not stop the rest
            print(f"  could not download {p['id']}: {e}")
        if done and done % 50 == 0:
            print(f"  {done} downloaded")
        time.sleep(0.1)
    for p in photos:
        p.pop("src", None)  # signed CDN links expire; the file and the link are what last

    json.dump(sorted(photos, key=lambda p: p["date"] or ""), open(os.path.join(a.out, "photos.json"), "w"),
              indent=1, ensure_ascii=False)
    json.dump(sorted(posts, key=lambda p: p["date"] or ""), open(os.path.join(a.out, "posts.json"), "w"),
              indent=1, ensure_ascii=False)
    print(f"Done: {len(posts)} posts, {len(photos)} photos ({done} new files) in {a.out}")


if __name__ == "__main__":
    main()
