"""Read-only HTTP/sitemap/HTML audit. Output stays in the project audit folder."""
import concurrent.futures, json, sys, time, urllib.request, urllib.error
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

BASE = 'https://nmaus.ru'
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else 'audit/2026-10-31/live-before.json')

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.title=''; self.h1=[]; self.links=[]; self.assets=[]; self.meta={}; self.canonical=[]; self.schema=[]; self.mode=None; self.buf=''
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='meta': self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical': self.canonical.append(a.get('href'))
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag in ('img','script') and a.get('src'): self.assets.append(a['src'])
        if tag in ('title','h1') or (tag=='script' and a.get('type')=='application/ld+json'): self.mode=tag; self.buf=''
    def handle_data(self,data):
        if self.mode: self.buf+=data
    def handle_endtag(self,tag):
        if tag!=self.mode:return
        if tag=='title':self.title=self.buf.strip()
        elif tag=='h1':self.h1.append(self.buf.strip())
        else:
            try:self.schema.append(json.loads(self.buf))
            except ValueError:self.schema.append({'error':'invalid JSON'})
        self.mode=None

def fetch(url):
    started=time.monotonic()
    try:
        r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'NMA-SEO-Audit/1.0'}),timeout=25)
    except urllib.error.HTTPError as e:r=e
    except Exception as e:return {'url':url,'error':str(e)}
    body=r.read(); result={'url':url,'final_url':r.url,'status':r.code,'headers':dict(r.headers),'bytes':len(body),'seconds':round(time.monotonic()-started,3)}
    if 'text/html' in r.headers.get('Content-Type',''):
        p=Page();p.feed(body.decode('utf-8','replace'))
        result.update({k:getattr(p,k) for k in ('title','h1','links','assets','meta','canonical','schema')})
    else:result['body']=body.decode('utf-8','replace')
    return result

def main():
    sitemap=fetch(BASE+'/sitemap-index.xml'); maps=[sitemap]; urls=[]
    for entry in ET.fromstring(sitemap['body']):
        loc=entry.find('{*}loc').text; m=fetch(loc);maps.append(m)
        urls += [e.find('{*}loc').text for e in ET.fromstring(m['body'])]
    probes=['http://nmaus.ru/','https://www.nmaus.ru/','http://www.nmaus.ru/',BASE+'/robots.txt',BASE+'/seo-audit-missing-20261031/',BASE+'/about',BASE+'/about/index.html',BASE+'/?utm_source=seo-audit',BASE+'/nao/vl/']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: pages=list(pool.map(fetch,dict.fromkeys(urls+probes)))
    canonical_pages=[p for p in pages if p['url'] in urls]
    summary={'sitemap_urls':len(urls),'statuses':dict(Counter(p.get('status','error') for p in canonical_pages)), 'missing_title':[p['url'] for p in canonical_pages if not p.get('title')], 'bad_h1':[p['url'] for p in canonical_pages if len(p.get('h1',[]))!=1], 'non_self_canonical':[p['url'] for p in canonical_pages if p.get('canonical')!=[p['url']]],'duplicate_titles':{k:v for k,v in Counter(p.get('title') for p in canonical_pages).items() if v>1},'duplicate_descriptions':{k:v for k,v in Counter(p.get('meta',{}).get('description') for p in canonical_pages).items() if v>1}}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps({'summary':summary,'sitemaps':maps,'pages':pages},ensure_ascii=False,indent=2))
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Saved:',OUT)

if __name__=='__main__':main()
