# 本地官方课程资料库

[返回工作台](../README.md) · [怎么学](../course/STUDY_GUIDE.md) · [逐主题文件索引](../course/READING_LIST.md)

已归档 **415 个官方文件，1374.4 MiB**（不含解压副本）。获取记录：2026-09-21T01:58:44.625023+00:00。

每个课程目录提供分类文件列表及可直接打开的作业 Notebook。PDF/ZIP 为官方原件；中文课程指南单独存放在 course/。

| 课程 | 文件数 | 内容 |
|---|---:|---|
| [MIT 18.06SC · Fall 2011 · 线性代数](mit-1806sc-f11/README.md) | 136 | 讲义、练习、代码或考试；详见课程目录 |
| [UC Berkeley Data 100 · Spring 2025 · 数据科学](berkeley-data100-sp25/README.md) | 1 | 讲义、练习、代码或考试；详见课程目录 |
| [Stanford CS229 · SEE 经典公开档案 · 机器学习](stanford-cs229-see/README.md) | 59 | 讲义、练习、代码或考试；详见课程目录 |
| [UC Berkeley CS189 · Spring 2025 · 机器学习](berkeley-cs189-sp25/README.md) | 99 | 讲义、练习、代码或考试；详见课程目录 |
| [UC Berkeley CS182 · Spring 2021 · 深度学习](berkeley-cs182-sp21/README.md) | 48 | 讲义、练习、代码或考试；详见课程目录 |
| [Stanford CS231n · 2025 slides / 2026 作业包](stanford-cs231n-2025/README.md) | 26 | 讲义、练习、代码或考试；详见课程目录 |
| [Stanford CS224N · Winter 2025 · NLP 与 Transformer](stanford-cs224n-w25/README.md) | 46 | 讲义、练习、代码或考试；详见课程目录 |

## 完整存储与服务器使用

[GitHub 存储与恢复方案](../docs/GITHUB_STORAGE.md) · [服务器只拉作业教程](../docs/SERVER_GUIDE.md)

海外原件保存在本仓库的 GitHub Releases；恢复全部用 `python3 scripts/library_archive.py restore --all`。只做某份海外作业时使用 `fetch --file <课程/ZIP文件>`，不会下载讲义归档。

## 单独同步的课程

[NJU 2026 大语言模型课程](nju-llm-2026/README.md) · [讲义目录](nju-llm-2026/LECTURES.md) · [个人学习副本](../work/nju-llm-2026/README.md)

NJU 资料使用独立来源清单，不计入上方归档数量与大小。仅补充新增讲义：`python3 scripts/sync_nju.py lectures`；作业保留固定快照。

## 下载与复查

[来源与校验清单](manifest.json)记录每份文件的 URL、来源页面、大小与 SHA256。原课程页面也保存了 HTML 快照；页面中的远程链接可能仍需联网。

重新下载：`python3 scripts/download_courses.py`；重建目录及解压：`python3 scripts/build_library_catalog.py`。命令在项目根目录执行。
