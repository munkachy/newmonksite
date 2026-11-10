import re
from crop import *
def make(src,region,name):
    svg=load(src); head,body=split(svg)
    x0,y0,x1,y1=region
    for e in elems(body):
        b=bbox(e)
        if b and 'glyph' not in e and (b[2]-b[0])>300 and (b[3]-b[1])>40 and 'fill="none"' not in e:
            body=body.replace(e,'',1)
    out=[]
    for m in re.finditer(r'<g fill=[^>]*>.*?</g>|<path\b[^>]*?/>',body,flags=re.S):
        t=m.group(0)
        if t.startswith('<g'):
            uses=re.findall(r'x="([-\d.]+)" y="([-\d.]+)"',t)
            if any(x0-5<=float(x)<=x1+5 and y0-5<=float(y)<=y1+30 for x,y in uses): out.append(t)
        else:
            b=bbox(t)
            if b and b[2]>=x0 and b[0]<=x1 and b[3]>=y0 and b[1]<=y1: out.append(t)
    body='\n'.join(out)
    used=set(re.findall(r'#(glyph-\d+-\d+)',body))
    newdefs='\n'.join(re.search(r'<g id="%s">.*?</g>'%re.escape(g),head,flags=re.S).group(0) for g in sorted(used))
    head2=f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{x1-x0}" height="{y1-y0}" viewBox="{x0} {y0} {x1-x0} {y1-y0}">\n<defs>\n{newdefs}\n</defs>\n'
    open(f'out/{name}.svg','w').write(head2+body+'\n</svg>\n')
J=[('p2.svg',(615,119,936,382),'primary-light'),('p2.svg',(565,543,986,641),'horizontal-light'),
('p2.svg',(687,122,863,297),'cross-light'),
('p3.svg',(488,135,736,340),'primary-dark'),('p3.svg',(466,498,757,542),'horizontal-dark'),
('p3.svg',(546,143,678,276),'cross-dark'),
('p6.svg',(227,137,392,296),'primary-abbey-light'),('p6.svg',(212,518,409,565),'horizontal-abbey-light')]
for s,r,n in J: make(s,r,n)
