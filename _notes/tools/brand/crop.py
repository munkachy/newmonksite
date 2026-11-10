import re,sys
def load(f): return open(f).read()
def split(svg):
    i=svg.index('</defs>')+7
    return svg[:i], svg[i:]
def elems(body):
    # top-level elements: <path .../> and <use .../> ; groups may exist
    return re.findall(r'<(?:path|use)\b[^>]*?/>',body,flags=re.S)
def bbox(el):
    m=re.search(r'\bd="([^"]*)"',el)
    if not m: 
        u=re.search(r'x="([-\d.]+)" y="([-\d.]+)"',el)
        return (float(u.group(1)),float(u.group(2)),)*2 if u else None
    nums=[float(x) for x in re.findall(r'-?\d+\.?\d*',m.group(1))]
    xs=nums[0::2]; ys=nums[1::2]
    return min(xs),min(ys),max(xs),max(ys)
if __name__=='__main__':
    svg=load(sys.argv[1]); head,body=split(svg)
    for i,e in enumerate(elems(body)):
        b=bbox(e)
        if b and (b[2]-b[0])>150:
            print(i,[round(x) for x in b],re.search(r'fill="([^"]*)"',e).group(1) if 'fill="' in e else '')
