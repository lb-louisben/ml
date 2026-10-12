"""Generate offline reading indexes and unpack selected course starter bundles."""
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse, unquote
from zipfile import ZipFile
from collections import Counter
import json
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT/'library'
NAMES = {
    'mit-1806sc-f11': 'MIT 18.06SC · Fall 2011 · 线性代数',
    'berkeley-data100-sp25': 'UC Berkeley Data 100 · Spring 2025 · 数据科学',
    'stanford-cs229-see': 'Stanford CS229 · SEE 经典公开档案 · 机器学习',
    'berkeley-cs189-sp25': 'UC Berkeley CS189 · Spring 2025 · 机器学习',
    'berkeley-cs182-sp21': 'UC Berkeley CS182 · Spring 2021 · 深度学习',
    'stanford-cs231n-2025': 'Stanford CS231n · 2025 slides / 2026 作业包',
    'stanford-cs224n-w25': 'Stanford CS224N · Winter 2025 · NLP 与 Transformer',
}

def natural(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)',s)]

def name(r):
    raw = unquote(Path(urlparse(r['url']).path).name) if not 'codeload.github.com' in r['url'] else Path(r['file']).name.split('-',1)[-1]
    return re.sub(r'^[a-f0-9]{32}_','',raw)

def category(r):
    n = name(r).lower()
    if any(t in n for t in ('solution','-sol.','_sol.')): return '官方解答'
    if 'project' in n or 'milestone' in n: return '项目与课程说明'
    if any(t in n for t in ('mid','final','exam','quiz')) or re.search(r'_ex[1-3]',n): return '考试与复习卷'
    if re.search(r'(problemset|assignment|hw\d|^a\d|student-head|public-head)', n): return '作业与配套代码'
    if 'prob' in n and 'cs229-prob' not in n: return '练习题'
    if 'sol' in n: return '官方解答'
    if 'data.zip' in n: return '作业数据'
    return '讲义、Slides 与补充材料'

def unpack(r):
    n=name(r).lower()
    chosen = (r['course']=='berkeley-data100-sp25' or
              (r['course']=='stanford-cs231n-2025' and 'assignment' in n) or
              (r['course']=='stanford-cs224n-w25' and re.fullmatch(r'a[1-4]\.zip',n)) or
              (r['course']=='berkeley-cs182-sp21' and n.endswith('.zip')))
    if not chosen or not n.endswith('.zip'): return None
    dest = LIB/r['course']/'unpacked'/Path(r['file']).stem
    marker = dest/'.archive-sha256'
    if marker.exists():
        if marker.read_text().strip()!=r['sha256']: raise ValueError('Archive changed: '+str(dest))
        return dest
    with ZipFile(LIB/r['file']) as z:
        if sum(i.file_size for i in z.infolist())>1024**3: raise ValueError('Archive too large: '+n)
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe archive path')
            if '__MACOSX' in p.parts or p.name.startswith('._'): continue
            if info.is_dir(): continue
            if ((info.external_attr>>16)&0o170000)==0o120000: continue
            target=dest.joinpath(*p.parts)
            target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists(): continue
            target.write_bytes(z.read(info))
    marker.write_text(r['sha256']+'\n')
    return dest

def main():
    m=json.loads((LIB/'manifest.json').read_text())
    records=m['resources']; ok=[r for r in records if r['status']=='downloaded']
    bundles={}
    for r in ok:
        if Path(r['file']).suffix=='.zip':
            folder=unpack(r)
            if folder: bundles[r['file']]=folder
    total=sum(r['bytes'] for r in ok)
    top=['# 本地官方课程资料库','', '[返回工作台](../README.md) · [怎么学](../course/STUDY_GUIDE.md) · [逐主题文件索引](../course/READING_LIST.md)', '',
         f"已归档 **{len(ok)} 个官方文件，{total/1024**2:.1f} MiB**（不含解压副本）。获取记录：{m['retrieved_at']}。",'',
         '每个课程目录提供分类文件列表及可直接打开的作业 Notebook。PDF/ZIP 为官方原件；中文课程指南单独存放在 course/。', '',
         '| 课程 | 文件数 | 内容 |','|---|---:|---|']
    for course,title in NAMES.items():
        rows=sorted([r for r in ok if r['course']==course],key=lambda r:natural(name(r)))
        top.append(f'| [{title}]({course}/README.md) | {len(rows)} | 讲义、练习、代码或考试；详见课程目录 |')
        lines=[f'# {title}', '', '[返回资料库](../README.md) · [学习指南](../../course/STUDY_GUIDE.md)', '']
        snapshots=sorted((LIB/course).glob('source-*.html'))
        lines += ['课程页面存档：'+' · '.join(f'[{p.stem}]({p.name})' for p in snapshots),'']
        if course=='stanford-cs231n-2025':
            lines += ['版本说明：课程 slides 来自 2025；2025 作业网页当前链接的 ZIP 位于官方 `/assignments/2026/` 路径，因此这三个 ZIP 是 2026 发布包。按包内题面完成练习。已核对 `/assignments/2025/assignment1.zip` 返回 404。','']
        if course=='stanford-cs224n-w25':
            lines += ['版本说明：2025 课程页面本身复用了 2019/2023/2024 的若干 notes。文件名保留原始年份，作业采用页面列出的 Winter 2025 包。','']
        lines += ['## 打开已解压的作业与讲课 Notebook','']
        extracted=[]
        for r in rows:
            folder=bundles.get(r['file'])
            if folder:
                for p in sorted(folder.rglob('*')):
                    if p.suffix=='.ipynb' or p.name.lower() in ('readme.md','readme.txt','requirements.txt'):
                        extracted.append(p)
        if extracted:
            for p in extracted:
                rel=p.relative_to(LIB/course).as_posix()
                lines.append(f'- [{p.parent.name}/{p.name}]({rel})')
            lines += ['', 'ZIP 内文件已解压；尚未安装或执行课程代码。数据依赖和运行方式查看对应 README。','']
        else: lines += ['该课程主要使用下方 PDF 和 ZIP 原件。','']
        categories=['讲义、Slides 与补充材料','练习题','作业与配套代码','作业数据','考试与复习卷','官方解答','项目与课程说明']
        for group in categories:
            subset=[r for r in rows if category(r)==group]
            if not subset: continue
            lines += [f'## {group}', '', '| 本地文件 | 官方页面/原始文件 | 大小 |','|---|---|---:|']
            for r in subset:
                filename=Path(r['file']).name
                lines.append(f"| [{name(r)}]({filename}) | [原址]({r['url'].replace(' ','%20')}) | {r['bytes']/1024:.0f} KB |")
        failed=[r for r in records if r['course']==course and r['status']=='failed']
        if failed:
            lines += ['', '## 未成功下载的文件','']
            lines += [f"- [{Path(urlparse(r['url']).path).name}]({r['url'].replace(' ','%20')})：{r['error']}" for r in failed]
            if course=='berkeley-cs182-sp21':
                lines += ['', 'HW2 练习替代入口：[CS231n 本地 CNN 作业包](../stanford-cs231n-2025/README.md)。']
            if course=='stanford-cs231n-2025':
                lines += ['', '求导补充材料替代入口：[CS224N 本地 derivatives / gradient notes](../stanford-cs224n-w25/README.md)。']
        lines += ['', '完整来源、SHA256 与下载状态见 [manifest](../manifest.json)。']
        (LIB/course/'README.md').write_text('\n'.join(lines)+'\n')
    top += ['', '## 完整存储与服务器使用', '',
            '[GitHub 存储与恢复方案](../docs/GITHUB_STORAGE.md) · [服务器只拉作业教程](../docs/SERVER_GUIDE.md)', '',
            '海外原件保存在本仓库的 GitHub Releases；恢复全部用 `python3 scripts/library_archive.py restore --all`。只做某份海外作业时使用 `fetch --file <课程/ZIP文件>`，不会下载讲义归档。', '',
            '## 单独同步的课程', '',
            '[NJU 2026 大语言模型课程](nju-llm-2026/README.md) · [讲义目录](nju-llm-2026/LECTURES.md) · [个人学习副本](../work/nju-llm-2026/README.md)', '',
            'NJU 资料使用独立来源清单，不计入上方归档数量与大小。仅补充新增讲义：`python3 scripts/sync_nju.py lectures`；作业保留固定快照。', '',
            '## 下载与复查', '',
            '[来源与校验清单](manifest.json)记录每份文件的 URL、来源页面、大小与 SHA256。原课程页面也保存了 HTML 快照；页面中的远程链接可能仍需联网。', '',
            '重新下载：`python3 scripts/download_courses.py`；重建目录及解压：`python3 scripts/build_library_catalog.py`。命令在项目根目录执行。','']
    (LIB/'README.md').write_text('\n'.join(top))
    reading=['# 逐主题本地阅读索引','','[学习顺序与作业要求](STUDY_GUIDE.md) · [官方资料库](../library/README.md)','',
             '下列链接直接打开本地文件。每组内按文件编号推进，详细日程与验收见学习指南。','']
    groups=[
        ('math','数学：MIT 配套讲义、题目和答案','mit-1806sc-f11',r'(sum|prob|sol|exam|quiz|_ex|final)',140),
        ('review','数学：CS229 复习','stanford-cs229-see',r'(linalg|cs229-prob|cvxopt)',10),
        ('cs229','CS229：核心讲义与四套作业','stanford-cs229-see',r'(notes[1-9]|problemset|PS[1-4]-data|ps[1-4]_solution)',40),
        ('cs189','CS189：讲义与作业','berkeley-cs189-sp25',r'(^\d+\.pdf|^hw\d|machlearn)',50),
        ('exams','CS189：2024/2025 考试与答案','berkeley-cs189-sp25',r'(mid|final)s(24|25)',12),
        ('dl','CS182：课件、讨论和作业','berkeley-cs182-sp21',r'(^lec-|^dis[1-7]|hw)',60),
        ('vision','CS231n：2025 slides 与 2026 代码包','stanford-cs231n-2025',r'(lecture_|assignment)',30),
        ('nlp','CS224N：2025 slides、四套作业、项目','stanford-cs224n-w25',r'(2025-lecture|^a[1-4]\.|Project|project)',40),
    ]
    for anchor,title,course,pattern,limit in groups:
        subset=sorted([r for r in ok if r['course']==course and re.search(pattern,name(r),re.I)],key=lambda r:natural(name(r)))
        reading += [f'<a id="{anchor}"></a>','',f'## {title}','']
        for r in subset[:limit]: reading.append(f"- [{name(r)}](../library/{r['file']})")
        reading += ['',f'[该课程全部材料](../library/{course}/README.md)','']
    reading += ['## Data 100：直接打开练习','']
    for r in ok:
        if r['course']!='berkeley-data100-sp25' or r['file'] not in bundles: continue
        for p in sorted(bundles[r['file']].rglob('*.ipynb')):
            if any(part in ('hw','lab') for part in p.parts):
                reading.append(f'- [{p.parent.name}/{p.name}](../{p.relative_to(ROOT).as_posix()})')
    (ROOT/'course/READING_LIST.md').write_text('\n'.join(reading)+'\n')
    print(json.dumps({'downloaded':len(ok),'MiB':round(total/1024**2,1),'unpacked_bundles':len(bundles),'courses':dict(Counter(r['course'] for r in ok))},ensure_ascii=False))

if __name__=='__main__': main()
