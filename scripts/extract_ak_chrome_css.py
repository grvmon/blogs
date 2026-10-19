import re,sys
css=open('/tmp/a-K/website.min.css').read()
_h=open('/tmp/a-K/index.html').read()
css+='\n'+'\n'.join(re.findall(r'<style[^>]*>(.*?)</style>',_h,re.S))
css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
KEY=re.compile(r'header-nav|nav-container|nav-brand|brand-logo-text|nav-links|nav-cta-btn|primary-cta-btn|cta-arrow-badge|mobile-toggle|hamburger|mobile-nav|mobile-drawer|drawer-open|site-footer|footer-')
def blocks(s):
    i=0;out=[]
    while i<len(s):
        j=s.find('{',i)
        if j<0:break
        sel=s[i:j].strip(); depth=1;k=j+1
        while depth:
            if s[k]=='{':depth+=1
            elif s[k]=='}':depth-=1
            k+=1
        out.append((sel,s[j+1:k-1])); i=k
    return out
res=[];vars_used=set()
def walk(s,wrap=None):
    for sel,body in blocks(s):
        if sel.startswith('@media') or sel.startswith('@supports'):
            inner=[]
            for s2,b2 in blocks(body):
                if KEY.search(s2): inner.append(f'{s2}{{{b2}}}')
                elif re.fullmatch(r'\.container', s2.strip()): inner.append(f'.header-nav .container,.site-footer .container{{{b2}}}')
            if inner: res.append(sel+'{'+''.join(inner)+'}')
        elif sel.startswith('@keyframes'):
            res.append((sel,body))
        elif KEY.search(sel):
            res.append(f'{sel}{{{body}}}')
        elif re.fullmatch(r'\.container', sel.strip()):
            res.append(f'.header-nav .container,.site-footer .container{{{body}}}')
walk(css)
kf=[r for r in res if isinstance(r,tuple)]; res=[r for r in res if not isinstance(r,tuple)]
text='\n'.join(res)
used=set(re.findall(r'animation(?:-name)?:\s*([\w-]+)',text))
text='\n'.join(f'{s}{{{b}}}' for s,b in kf if s.split()[1] in used)+'\n'+text
vars_needed=set(re.findall(r'var\((--[\w-]+)',text))
root=''.join(b for s,b in blocks(css) if s.strip()==':root')+';'
decl=dict(re.findall(r'(--[\w-]+)\s*:\s*([^;]+);',root))
rootcss=':root{'+''.join(f'{v}:{decl[v]};' for v in sorted(vars_needed) if v in decl)+'}'
print('missing vars',[v for v in vars_needed if v not in decl],file=sys.stderr)
open(sys.argv[1],'w').write('/* Header/footer copied verbatim from acrenkey.com (grvmon/a-K website.min.css + index.html inline <style>). Do not edit here; re-extract. */\n'+rootcss+'\n'+text+'\n')
print(len(res),'rules',len(text))
