import json, time, urllib.request, urllib.parse, re
exec(open("saints_fetch.py").read().split("def get(")[0])  # UA, OUT, T
def get(url,tries=12):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept-Encoding":"identity"})
            with urllib.request.urlopen(req,timeout=60) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code==429:
                ra=int(e.headers.get("retry-after") or 30); print("429, waiting",ra+5,flush=True); time.sleep(ra+5); continue
            raise
    raise RuntimeError("gave up")
titles=sorted(set(T.values()))
page_img={}; norm={}
for i in range(0,len(titles),40):
    chunk=titles[i:i+40]
    q=json.loads(get("https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":"|".join(chunk),"prop":"pageimages","piprop":"name","redirects":1,"format":"json","pilimit":"max"})))
    for n in q["query"].get("normalized",[]): norm[n["from"]]=n["to"]
    for n in q["query"].get("redirects",[]): norm[n["from"]]=n["to"]
    for p in q["query"]["pages"].values(): page_img[p["title"]]=p.get("pageimage")
    time.sleep(40)
def resolve(t):
    for _ in range(3): t=norm.get(t,t)
    return t
files=sorted(set(f for f in page_img.values() if f))
info={}
for i in range(0,len(files),40):
    chunk=files[i:i+40]
    m=json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":"|".join("File:"+f for f in chunk),"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":900,"format":"json"})))
    nn={n["to"]:n["from"] for n in m["query"].get("normalized",[])}
    for p in m["query"]["pages"].values():
        if "imageinfo" not in p: continue
        ii=p["imageinfo"][0]; em=ii.get("extmetadata",{}); g=lambda k: (em.get(k,{}) or {}).get("value","")
        key=p["title"].replace("File:","").replace(" ","_")
        info[key]={"thumb":ii.get("thumburl"),"page":ii.get("descriptionurl"),"license":g("LicenseShortName"),"artist":re.sub("<[^>]+>","",g("Artist")).strip()[:150],"desc":re.sub("<[^>]+>","",g("ImageDescription")).strip()[:200]}
    time.sleep(40)
res={}
for name,title in T.items():
    t=resolve(title); f=page_img.get(t)
    if not f: res[name]={"title":t,"file":None}; continue
    i2=info.get(f.replace(" ","_"))
    res[name]={"title":t,"file":f,**(i2 or {"why":"not on commons"})}
json.dump(res,open(OUT+"/meta.json","w"),indent=1)
from collections import Counter
print(Counter((v.get("license") or v.get("why") or ("no image" if not v.get("file") else "?"))[:25] for v in res.values()).most_common())
for k,v in res.items():
    if not v.get("license"): print("  none:",k,"|",v.get("title"),"|",v.get("file"),v.get("why",""))
