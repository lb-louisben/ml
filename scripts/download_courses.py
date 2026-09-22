"""Download public course documents; preserve originals and generate a local catalog."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse, unquote, quote
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import re
import datetime
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1] / 'library'
COURSES = {
    'stanford-cs229-see': ['https://see.stanford.edu/Course/CS229'],
    'berkeley-cs189-sp25': ['https://people.eecs.berkeley.edu/~jrs/189/'],
    'stanford-cs231n-2025': ['https://cs231n.stanford.edu/2025/schedule.html',
        'https://cs231n.github.io/assignments2025/assignment1/',
        'https://cs231n.github.io/assignments2025/assignment2/',
        'https://cs231n.github.io/assignments2025/assignment3/'],
    'stanford-cs224n-w25': ['https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1254/'],
    'berkeley-cs182-sp21': ['https://cs182sp21.github.io/'],
    'mit-1806sc-f11': ['https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/resource-index/',
        'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/ax-b-and-the-four-subspaces/exam-1/',
        'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/least-squares-determinants-and-eigenvalues/exam-2/',
        'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/positive-definite-matrices-and-applications/exam-3/',
        'https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/final-exam/'],
    'berkeley-data100-sp25': ['https://ds100.org/sp25/'],
}

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []; self.href = None; self.label = ''
    def handle_starttag(self, tag, attrs):
        if tag == 'a': self.href = dict(attrs).get('href'); self.label = ''
    def handle_data(self, data):
        if self.href: self.label += data
    def handle_endtag(self, tag):
        if tag == 'a' and self.href:
            self.links.append((self.href, self.label.strip())); self.href = None

def fetch(url):
    url = quote(url, safe=':/?=&%#+~')
    with urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (personal course archive)'}), timeout=45) as r:
        limit = 512 if (re.search(r'hw\d+\.zip',url) or 'codeload.github.com' in url or 'machlearn.pdf' in url) else 80
        data = r.read(limit * 1024 * 1024 + 1)
        if len(data) > limit * 1024 * 1024: raise ValueError(f'File exceeds {limit} MiB limit')
        return data, r.geturl(), r.headers.get('Content-Type', '')

def collect(course, pages):
    folder = ROOT / course
    folder.mkdir(parents=True, exist_ok=True)
    found = {}
    resource_pages = set()
    for i, page in enumerate(pages):
        try:
            cache = folder / f'source-{i+1}.html'
            if cache.exists(): data, final = cache.read_bytes(), page
            else:
                data, final, _ = fetch(page)
                cache.write_bytes(data)
            parser = Links(); parser.feed(data.decode('utf-8', errors='replace'))
            for href, label in parser.links:
                url = urljoin(final, href)
                path = urlparse(url).path.lower()
                if course == 'mit-1806sc-f11' and '/resources/' in path and any(t in path for t in ('sum', 'prob', 'sol', 'exam', '_ex', '_final')):
                    resource_pages.add(url)
                # Download course-hosted files, not the linked paper literature or videos.
                host = urlparse(url).hostname or ''
                if not any(h in host for h in ('stanford.edu', 'berkeley.edu', 'cs182sp21.github.io', 'cs231n.github.io', 'ocw.mit.edu')): continue
                if path.endswith(('.pdf', '.zip', '.ipynb')):
                    found[url] = {'course': course, 'url': url, 'title': label or Path(path).name, 'source_page': page}
        except Exception as exc:
            print('PAGE FAILED', page, str(exc), flush=True)
    def resolve_resource(page):
        try:
            cache = folder / 'source-pages' / (hashlib.sha256(page.encode()).hexdigest()[:16]+'.html')
            cache.parent.mkdir(exist_ok=True)
            if cache.exists(): data, final = cache.read_bytes(), page
            else:
                data, final, _ = fetch(page)
                cache.write_bytes(data)
            parser = Links(); parser.feed(data.decode('utf-8', errors='replace'))
            return [dict(course=course, url=urljoin(final,h), title=t or Path(h).name, source_page=page)
                    for h,t in parser.links if urlparse(h).path.lower().endswith('.pdf')]
        except Exception as exc:
            print('RESOURCE FAILED',page,str(exc),flush=True); return []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for entries in pool.map(resolve_resource, sorted(resource_pages)):
            for entry in entries: found[entry['url']] = entry
    return list(found.values())

def download(item):
    url = item['url']; name = unquote(Path(urlparse(url).path).name)
    name = re.sub(r'[^\w.\-]+', '_', name)
    if 'codeload.github.com' in url: name = urlparse(url).path.split('/')[2] + '-HEAD.zip'
    name = hashlib.sha256(url.encode()).hexdigest()[:8] + '-' + name
    path = ROOT / item['course'] / name
    try:
        if path.exists() and path.suffix.lower()=='.zip' and not zipfile.is_zipfile(path):
            rejected = ROOT.parent / '.cache' / 'downloads' / (path.name+'.incomplete')
            rejected.parent.mkdir(parents=True,exist_ok=True)
            if not rejected.exists(): path.rename(rejected)
            else: raise ValueError('Incomplete archive already quarantined')
        if path.exists(): data = path.read_bytes(); final = url
        else:
            data, final, _ = fetch(url)
            suffix = path.suffix.lower()
            if suffix == '.pdf' and not data.startswith(b'%PDF'): raise ValueError('Not a PDF')
            if suffix == '.zip' and not zipfile.is_zipfile(io.BytesIO(data)): raise ValueError('ZIP is incomplete or invalid')
            path.write_bytes(data)
        return dict(item, status='downloaded', file=str(path.relative_to(ROOT)),
                    bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), final_url=final)
    except Exception as exc:
        return dict(item, status='failed', error=str(exc))

def main():
    ROOT.mkdir(exist_ok=True)
    items = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        for future in as_completed([pool.submit(collect, c, p) for c,p in COURSES.items()]):
            items.extend(future.result())
    for course, repo in [('berkeley-data100-sp25','DS-100/sp25-student'),
                         ('berkeley-cs182-sp21','cs182sp21/cs182_hw2_student'),
                         ('berkeley-cs182-sp21','cs182sp21/hw3_public'),
                         ('berkeley-cs182-sp21','cs182sp21/hw4_student')]:
        items.append(dict(course=course, url=f'https://codeload.github.com/{repo}/zip/HEAD',
                          title=repo+' official starter-code snapshot (HEAD)',
                          source_page=f'https://github.com/{repo}'))
    print('Discovered', len(items), 'official documents', flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for f in as_completed([pool.submit(download, x) for x in items]):
            result = f.result(); results.append(result)
            print(result['status'], result['course'], result['url'].rsplit('/',1)[-1], flush=True)
    results.sort(key=lambda x:(x['course'], x['url']))
    previous = ROOT/'manifest.json'
    if previous.exists():
        merged = {r['url']:r for r in json.loads(previous.read_text())['resources']}
        merged.update({r['url']:r for r in results})
        results = sorted(merged.values(), key=lambda x:(x['course'],x['url']))
    (ROOT/'manifest.json').write_text(json.dumps({'retrieved_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'resources':results}, ensure_ascii=False, indent=2))
    top = ['# 官方课程资料库', '', '原件保留作者与学校署名。按学期归档；下面的文件链接均指向本地。下载日期、原始 URL、文件大小和 SHA256 见 [manifest](manifest.json)。', '', '[返回学习入口](../README.md)', '']
    for course, pages in COURSES.items():
        rows = [r for r in results if r['course']==course]
        ok = [r for r in rows if r['status']=='downloaded']
        top.append(f'- [{course}]({course}/README.md)：{len(ok)} 个已下载文件')
        lines = [f'# {course}', '', '[返回资料库](../README.md)', '', '## 官方来源', '']
        lines += [f'- [课程页面 {i+1}]({p}) · [页面存档](source-{i+1}.html)' for i,p in enumerate(pages)]
        lines += ['', '## 本地文件', '', '| 材料 | 文件 | 大小 |', '|---|---|---:|']
        for r in ok:
            title = r['title'].replace('|','/').replace('\n',' ')
            lines.append(f"| {title} | [{Path(r['file']).name}]({Path(r['file']).name}) | {r['bytes']/1024:.0f} KB |")
        failures = [r for r in rows if r['status']=='failed']
        if failures:
            lines += ['', '## 尚未下载成功', ''] + [f"- [{r['title']}]({r['url']})：{r['error']}" for r in failures]
        (ROOT/course/'README.md').write_text('\n'.join(lines)+'\n')
    (ROOT/'README.md').write_text('\n'.join(top)+'\n')
    print('DONE', sum(r['status']=='downloaded' for r in results), '/', len(results), flush=True)

if __name__ == '__main__': main()
