import re
from mk import make
from crop import bbox
NAVY='rgb(0%, 25.489807%, 41.567993%)'
def dark(name):
    s=open(f'out/{name}.svg').read()
    s=s.replace(f'<g fill="{NAVY}"','<g fill="#fefefe"')
    def fix(m):
        t=m.group(0)
        if NAVY in t:
            b=bbox(t)
            if b and (b[2]-b[0])<45 and (b[3]-b[1])>=16 and 1.2<(b[3]-b[1])/(b[2]-b[0])<1.32:   # the shield: keep navy, add a white outline
                return t.replace('<path ','<path stroke="#fefefe" stroke-width="0.9" stroke-linejoin="round" ',1)
            return t.replace(NAVY,'#fefefe')
        return t
    s=re.sub(r'<path\b[^>]*?/>',fix,s)
    open(f'out/{name}-dark.svg','w').write(s)
make('p6.svg',(460,137,625,296),'primary-prep-light')
make('p6.svg',(446,518,641,565),'horizontal-prep-light')
for n in ['primary-abbey-light','horizontal-abbey-light','primary-prep-light','horizontal-prep-light']: dark(n.replace('-light','')+'') if False else None
for n in ['primary-abbey','horizontal-abbey','primary-prep','horizontal-prep']:
    import shutil; shutil.copy(f'out/{n}-light.svg',f'out/{n}-x.svg'); dark(n+'-x')
