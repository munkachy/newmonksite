"""Portraits of the saints on the relics page: step 1 of 2 (step 2 is saints_build.py).

    python3 _notes/tools/saints_fetch.py meta          # look up each saint's image on Wikipedia/Commons -> _notes/saints/meta.json
    python3 _notes/tools/saints_fetch.py download RAW  # download every image in meta.json not yet in RAW (keep RAW out of the repo)

meta.json is already in the repo (2 Nov 2026), so normally only `download` is needed. Wikimedia's image server
(upload.wikimedia.org) rate-limits hard: on 2-3 Nov 2026 every request from the cloud session got HTTP 429 with
Retry-After 600 after the first 27 images. The script waits as told and resumes where it stopped; if it still gets
nothing but 429s, try another day or another machine. Names of the saints map to Wikipedia article titles in T.
"""
import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
UA="StBernardAbbeySite/1.0 (https://munkachy.github.io/newmonksite/)"
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","saints")  # _notes/saints
T={"St. Bernard of Clairvaux":"Bernard of Clairvaux","St. Benedict":"Benedict of Nursia","The tomb of Our Lord":"Church of the Holy Sepulchre",
"The Holy House of Loreto":"Basilica della Santa Casa","The tomb of Our Lady":"Tomb of the Virgin Mary","St. John the Baptist":"John the Baptist",
"St. Peter":"Saint Peter","St. Paul":"Paul the Apostle","St. Philip the Apostle":"Philip the Apostle","St. Joseph":"Saint Joseph","St. Anne":"Saint Anne",
"St. Alphonsus Liguori":"Alphonsus Liguori","St. Remigius":"Saint Remigius","St. Ursula":"Saint Ursula","St. Francis of Assisi":"Francis of Assisi",
"St. Anthony of Padua":"Anthony of Padua","St. Roch":"Saint Roch","St. Lucy":"Saint Lucy","St. Agatha":"Agatha of Sicily","St. Radegund":"Radegund",
"St. Hermenegild":"Hermenegild","St. Ferdinand III":"Ferdinand III of Castile","St. Matilda":"Matilda of Ringelheim","St. Henry II":"Henry II, Holy Roman Emperor",
"St. Oswald":"Oswald of Northumbria","St. Contardo d'Este":"Contardo d'Este","Bl. Beatrice I and II d'Este":"Beatrice d'Este (blessed)",
"St. Francis Xavier":"Francis Xavier","St. Raymond Nonnatus":"Raymond Nonnatus","St. Nicholas of Bari":"Saint Nicholas","St. Eucharius":"Eucharius",
"St. Valerius":"Valerius of Trier","St. Norbert":"Norbert of Xanten","St. Gemma Galgani":"Gemma Galgani","St. Joachim":"Saint Joachim","St. Agnes":"Agnes of Rome",
"St. Elizabeth of Hungary":"Elizabeth of Hungary","St. Martin de Porres":"Martin de Porres","St. Claude de la Colombière":"Claude de la Colombière",
"The Uganda Martyrs":"Uganda Martyrs","St. Valentine":"Saint Valentine","St. Anselm":"Anselm of Canterbury","St. Thomas Aquinas":"Thomas Aquinas",
"St. Gerard Majella":"Gerard Majella","St. Charbel":"Charbel Makhlouf","St. Blaise":"Saint Blaise","St. Simon Stock":"Simon Stock",
"St. Elizabeth Ann Seton":"Elizabeth Ann Seton","St. Teresa of Ávila":"Teresa of Ávila","St. Maria Goretti":"Maria Goretti","St. John Vianney":"John Vianney",
"St. Philip Neri":"Philip Neri","St. Catherine Labouré":"Catherine Labouré","St. Helena":"Helena, mother of Constantine I","St. Dominic":"Saint Dominic",
"St. Pius X":"Pope Pius X","St. Frances Xavier Cabrini":"Frances Xavier Cabrini","St. John Neumann":"John Neumann","St. Camillus de Lellis":"Camillus de Lellis",
"St. Augustine":"Augustine of Hippo","St. Matthew":"Matthew the Apostle","St. Luke":"Luke the Evangelist","St. Patrick":"Saint Patrick","St. Clare":"Clare of Assisi",
"St. Francis de Sales":"Francis de Sales","St. Bernadette":"Bernadette Soubirous","Sts. Jacinta and Francisco Marto":"Francisco and Jacinta Marto",
"St. Bonaventure":"Bonaventure","St. Bernard":"Bernard of Clairvaux","St. Aloysius Gonzaga":"Aloysius Gonzaga","St. Maurice":"Saint Maurice",
"St. Catherine of Siena":"Catherine of Siena","St. Angelo of Acri":"Angelo of Acri","St. Leonard of Port Maurice":"Leonard of Port Maurice",
"St. Pacificus of San Severino":"Pacificus of San Severino","St. Thomas of Cori":"Thomas of Cori","St. Paul of the Cross":"Paul of the Cross",
"St. John Berchmans":"John Berchmans","St. Dymphna":"Saint Dymphna","Bl. Columba Marmion":"Columba Marmion","St. Jude Thaddeus":"Jude the Apostle",
"St. Gabriel of Our Lady of Sorrows":"Gabriel of Our Lady of Sorrows","St. John Bosco":"John Bosco","St. Lawrence":"Saint Lawrence","St. Sebastian":"Saint Sebastian",
"St. Gabriel and St. Gemma":"Gabriel of Our Lady of Sorrows","St. Andrew and St. Martin":"Andrew the Apostle","St. Conrad of Parzham":"Conrad of Parzham",
"St. Vincent Ferrer":"Vincent Ferrer","St. Pier Giorgio Frassati":"Pier Giorgio Frassati"}
def get(url,tries=6):
    for i in range(tries):
        try:
            req=urllib.request.Request(url,headers={"User-Agent":UA})
            with urllib.request.urlopen(req,timeout=40) as r: return r.read()
        except urllib.error.HTTPError as e:
            if e.code==429: time.sleep(5*(i+1)); continue
            raise
    raise RuntimeError("gave up "+url)

def meta():
    res={}
    if os.path.exists(OUT+"/meta.json"): res=json.load(open(OUT+"/meta.json"))
    for name,title in T.items():
        if name in res and res[name].get("file"): continue
        try:
            q=json.loads(get("https://en.wikipedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":title,"prop":"pageimages","piprop":"name","redirects":1,"format":"json"})))
            page=list(q["query"]["pages"].values())[0]; fname=page.get("pageimage")
            if not fname: res[name]={"title":title,"file":None,"why":"no page image"}; print(name,"-> none"); time.sleep(1); continue
            time.sleep(1)
            m=json.loads(get("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode({"action":"query","titles":"File:"+fname,"prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":900,"format":"json"})))
            p=list(m["query"]["pages"].values())[0]
            if "imageinfo" not in p: res[name]={"title":title,"file":fname,"why":"not on commons (local/non-free)"}; print(name,"-> local only"); time.sleep(1); continue
            ii=p["imageinfo"][0]; em=ii.get("extmetadata",{})
            g=lambda k: (em.get(k,{}) or {}).get("value","")
            res[name]={"title":title,"file":fname,"thumb":ii.get("thumburl"),"page":ii.get("descriptionurl"),
                       "license":g("LicenseShortName"),"artist":g("Artist"),"credit":g("Credit"),"desc":g("ImageDescription")[:200],"date":g("DateTimeOriginal")}
            print(name,"->",fname,"|",res[name]["license"])
        except Exception as e:
            res[name]={"title":title,"file":None,"why":str(e)[:120]}; print(name,"ERR",e)
        json.dump(res,open(OUT+"/meta.json","w"),indent=1)
        time.sleep(1.2)
    json.dump(res,open(OUT+"/meta.json","w"),indent=1)


def download(raw):
    m = json.load(open(OUT + "/meta.json")); os.makedirs(raw, exist_ok=True); done = 0
    for name, v in m.items():
        u = v.get("thumb")
        if not u: continue
        fn = os.path.join(raw, re.sub(r"[^a-z0-9]+", "-", v["file"].lower())[:60] + ".jpg")
        if os.path.exists(fn) and os.path.getsize(fn) > 2000: continue
        for i in range(6):
            try:
                req = urllib.request.Request(u, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=60) as r: open(fn, "wb").write(r.read())
                done += 1; print("ok", name, flush=True); break
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    ra = int(e.headers.get("retry-after") or 20); print("429, waiting", ra, flush=True); time.sleep(ra + 3); continue
                print("ERR", name, e, flush=True); break
        time.sleep(1.5)
    print("downloaded", done)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "meta": meta()
    elif len(sys.argv) > 2 and sys.argv[1] == "download": download(sys.argv[2])
    else: sys.exit(__doc__)
