"""Generate portfolio content from the GitHub profile README; no extra dependencies."""
from pathlib import Path
import argparse, html, re, urllib.request
ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://raw.githubusercontent.com/safdar404/safdar404/main/README.md'
BASE = 'https://raw.githubusercontent.com/safdar404/safdar404/main/'
def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', lambda m: '<a href="'+m[2]+'" target="_blank" rel="noreferrer">'+m[1]+'</a>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def section(md, name):
    match = re.search(r'^## [^\n]*'+re.escape(name)+r'[^\n]*\n(.*?)(?=^## |\Z)', md, re.M|re.S)
    if not match: raise ValueError('Missing source section: '+name)
    return match[1]

def blocks(md):
    matches = list(re.finditer(r'^### (.+)$', md, re.M))
    return [(m[1], md[m.end():matches[i+1].start() if i+1<len(matches) else len(md)]) for i,m in enumerate(matches)]

def render(body):
    out=[]; listing=False
    for line in body.strip().splitlines():
        line=line.strip()
        if not line or line=='---': continue
        if line.startswith('- '):
            if not listing: out.append('<ul>'); listing=True
            out.append('<li>'+inline(line[2:])+'</li>'); continue
        if listing: out.append('</ul>'); listing=False
        if line.startswith('<p '):
            line=line.replace('src="./','src="'+BASE)
            line=re.sub(r'<img ', '<img loading="lazy" decoding="async" style="display:block;width:100%;height:auto;border-radius:10px" ',line)
            out.append(line)
        else: out.append('<p>'+inline(line)+'</p>')
    if listing: out.append('</ul>')
    return '\n'.join(out)

def generate(md):
    md=md.replace('\\n\\n','\n\n')
    groups=blocks(section(md,'Power BI & Decision Intelligence'))
    groups += [('Islamabad Feature Intelligence',section(md,'Islamabad Feature Intelligence'))]
    groups += [('GeoAI Site Intelligence Suite',section(md,'Featured project'))]
    groups += blocks(section(md,'Live AI & GeoAI Applications'))
    groups += blocks(section(md,'Selected projects'))
    unique={}
    for name,body in groups:
        if name not in unique: unique[name]=body
    if len(unique)<15: raise ValueError('Unexpectedly incomplete project catalogue')
    cards='\n'.join('<article class="repo-card reveal"><div class="repo-top"><span>PROJECT SHOWCASE</span><i>Portfolio</i></div><h3>'+html.escape(name)+'</h3>'+render(body)+'</article>' for name,body in unique.items())
    page=(ROOT/'index.html').read_text()
    start=page.index('<div class="repo-grid">')
    end=page.index('<div class="case-label',start)
    page=page[:start]+'<div class="repo-grid">\n'+cards+'\n</div>\n'+page[end:]
    tagline=re.search(r'^### (Data Scientist.+)$',md,re.M)[1]
    bio=re.search(r'^(I transform .+)$',md,re.M)[1]
    page=re.sub(r'(<div class="profile-meta"><strong>Muhammad Safdar</strong><span>).*?(</span>)',lambda m:m[1]+html.escape(tagline)+m[2],page)
    page=re.sub(r'(<p class="lead">).*?(</p>)',lambda m:m[1]+html.escape(bio)+m[2],page,count=1)
    page=page.replace('10+ years','15+ years').replace('<strong>10+</strong>','<strong>15+</strong>')
    page=page.replace('Six flagship systems plus a curated set of professional case studies.',str(len(unique))+' project showcases plus professional case studies.')
    rows=[]
    for line in section(md,'Professional delivery').splitlines():
        if not line.startswith('| **'):continue
        period,role,contribution=[c.strip().replace('**','') for c in line.strip('|').split('|')]
        title,org=role.split(' · ',1)
        rows.append('<article><time>'+html.escape(period)+'</time><div><h3>'+html.escape(title)+'</h3><strong>'+html.escape(org)+'</strong><p>'+html.escape(contribution)+'</p></div></article>')
    if not rows: raise ValueError('No career records found')
    page=re.sub(r'(<div class="timeline reveal">).*?(</div></section>)',lambda m:m[1]+'\n'+'\n'.join(rows)+'\n'+m[2],page,flags=re.S)
    (ROOT/'index.html').write_text(page)
    absolute=re.sub(r'(src="|\]\()\./',lambda m:m[1]+BASE,md)
    (ROOT/'README.md').write_text('# Portfolio source\n\nThis portfolio and its project catalogue are generated from [the GitHub profile README](https://github.com/safdar404/safdar404). Edit that README for shared content. The workflow checks for updates every six hours and can be run manually.\n\n'+absolute)
    (ROOT/'profile-source.md').write_text(md)
    print('Synchronized',len(unique),'projects and',len(rows),'career records')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source');args=parser.parse_args()
    if args.source: md=Path(args.source).read_text()
    else:
        with urllib.request.urlopen(SOURCE,timeout=30) as response:md=response.read().decode('utf-8')
    generate(md)
