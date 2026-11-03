import json, re, os, sys, html
import cv2, numpy as np
from PIL import Image, ImageOps
R="/home/user/newmonksite"
sys.path.insert(0,R+"/_notes/tools"); from grade import grade
"""Portraits of the saints, step 2 of 2: python3 _notes/tools/saints_build.py RAW
RAW = the folder saints_fetch.py downloaded into. Makes assets/img/saints/<slug>.jpg (160 px face crop) and full/<slug>.jpg,
adds them beside the names in relics/index.html (only names still without one) and rewrites relics/SAINT-IMAGES.md.
Portraits already on the site are kept even if their raw file is not in RAW. Needs opencv-python-headless==4.10.0.84."""
RAW=sys.argv[1] if len(sys.argv)>1 else sys.exit(__doc__)
m=json.load(open(R+"/_notes/saints/meta.json"))
os.makedirs(R+"/assets/img/saints/full",exist_ok=True)
casc=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
PLACES={"The tomb of Our Lord","The Holy House of Loreto","The tomb of Our Lady","The Uganda Martyrs","Sts. Jacinta and Francisco Marto"}
MAN={"agatha":(0.5,0.33,0.45),"bernard-of-clairvaux":(0.5,0.2,0.5),"bernard":(0.5,0.2,0.5),"hermenegild":(0.46,0.2,0.3),"joseph":(0.57,0.27,0.42),"oswald":(0.43,0.09,0.42),"ursula":(0.56,0.29,0.48),"remigius":(0.665,0.31,0.26)}
slug=lambda n: re.sub(r"[^a-z0-9]+","-",n.lower().replace("st. ","").replace("sts. ","").replace("bl. ","")).strip("-")
made={}
for name,v in m.items():
    f=(RAW+"/"+re.sub(r"[^a-z0-9]+","-",v["file"].lower())[:60]+".jpg") if v.get("file") else None
    if not f or not os.path.exists(f):
        if v.get("file") and os.path.exists(f"{R}/assets/img/saints/{slug(name)}.jpg"): made[name]=(slug(name),0)
        continue
    try: im=ImageOps.exif_transpose(Image.open(f)).convert("RGB")
    except Exception as e: print("bad",name,e); continue
    W,H=im.size; s=slug(name)
    full=im.copy(); full.thumbnail((900,900),Image.LANCZOS)
    grade(full,0.25).save(f"{R}/assets/img/saints/full/{s}.jpg",quality=80,optimize=True,progressive=True)
    faces=() if name in PLACES else casc.detectMultiScale(cv2.cvtColor(np.array(im),cv2.COLOR_RGB2GRAY),1.1,5,minSize=(max(24,W//16),max(24,W//16)))
    if s in MAN:
        cx,cy,sf=MAN[s]; cx*=W; cy*=H; side=sf*min(W,H); faces=[1]
    elif len(faces):
        x,y,w,h=max(faces,key=lambda r:r[2]*r[3]); cx,cy=x+w/2,y+h*0.55; side=min(W,H,w*1.9)
    elif name in PLACES: cx,cy,side=W/2,H/2,min(W,H)
    else: cx,cy,side=W/2,H*0.3,min(W,H)*0.6
    x0=int(max(0,min(W-side,cx-side/2))); y0=int(max(0,min(H-side,cy-side/2)))
    grade(im.crop((x0,y0,x0+int(side),y0+int(side))).resize((160,160),Image.LANCZOS),0.25).save(f"{R}/assets/img/saints/{s}.jpg",quality=82,optimize=True,progressive=True)
    made[name]=(s,len(faces))
# page
p=R+"/relics/index.html"; t=open(p).read()
def li(mm):
    name=html.unescape(mm.group(1))
    if name not in made: return mm.group(0)
    s=made[name][0]
    return f'<li><img class="saint-face" src="../assets/img/saints/{s}.jpg" data-full="../assets/img/saints/full/{s}.jpg" alt="{html.escape(name)}" width="160" height="160" loading="lazy" tabindex="0" role="button">{mm.group(1)}</li>'
t=re.sub(r'<li>([^<]+)</li>',lambda mm: li(mm) if True else mm.group(0),t)
note='<p class="small" style="margin-top:1rem">The saints\' portraits are paintings, icons and photographs from Wikimedia Commons, public domain or freely licensed; tap one to see it whole. <a href="https://github.com/munkachy/newmonksite/blob/main/relics/SAINT-IMAGES.md">Who made each image</a>.</p>'
if "SAINT-IMAGES.md" not in t:
    t=t.replace('<p class="lead rise" style="margin-top:1rem;max-width:44rem">The pictures below are working photographs','<p class="lead rise" style="margin-top:1rem;max-width:44rem">The pictures below are working photographs',1)
    i=t.index('<div class="relics">'); t=t[:i]+note+"\n    "+t[i:]
open(p,"w").write(t)
# credits
lines=["# Images of the saints on the relics page","","From Wikimedia Commons (the lead image of each saint's English Wikipedia article), fetched 2 Nov 2026. Small face crops in `assets/img/saints/`, larger copies in `assets/img/saints/full/`, both lightly graded. Every image is public domain or under a free licence; the licence and author are as Commons gives them.","","| On the page | Image | Author | Licence |","|---|---|---|---|"]
for name,v in m.items():
    if name in made:
        a=(v.get("artist") or "unknown").replace("|","/").replace("\n"," ")[:90]
        lines.append(f"| {name} | [{v['file']}]({v.get('page','')}) | {a} | {v.get('license','')} |")
lines+=["","No image: "+", ".join(k for k in m if k not in made)+". Ambiguous labels (St. Elizabeth, queen; Sts. Agapitus, Secundus, Justina; the unnamed St. Philip) were deliberately left without a picture."]
open(R+"/relics/SAINT-IMAGES.md","w").write("\n".join(lines)+"\n")
print(len(made),"made;", sum(1 for k,(s,n) in made.items() if n), "with a detected face")
