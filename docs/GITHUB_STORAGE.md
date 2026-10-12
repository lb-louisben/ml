# GitHub 存储与隔离方案

[项目首页](../README.md) · [服务器操作教程](SERVER_GUIDE.md) · [目录规则](PROJECT_STRUCTURE.md)

完整学习内容存放在同一个仓库 [lb-louisben/ml](https://github.com/lb-louisben/ml)，按修改方式与使用场景分层。服务器做作业时只检出选定目录，不下载资料归档。

## 内容放在哪里

| 内容 | 本地位置 | GitHub 保存方式 | 服务器做作业时 |
|---|---|---|---|
| Bootcamp Notebook、小数据、NumPy 网络 | `assignments/bootcamp/` | 普通 Git | 选择对应周 |
| 中文 A01～A08 题目 | `assignments/core/` | 普通 Git | 选择某题或全部 |
| NJU A0～A5 模板、题目、测试、许可证 | `assignments/nju-llm-2026/` | 普通 Git | 选择某份作业 |
| 个人作业实现、报告和笔记 | `work/` | 普通 Git | 只选择对应作业；个人讲义 Notebook 不自动带入 |
| 中文讲义、学习计划与项目要求 | `course/` | 普通 Git | 默认不检出 |
| NJU 老师讲义、课件图片与旧博客题面 | `library/nju-llm-2026/` | 普通 Git | 默认不检出 |
| 其他学校 PDF、参考书、原始 ZIP、来源 HTML | `library/<课程>/` | GitHub Releases | 默认不下载；选作业只下载那个 ZIP |
| 来源、文件大小和 SHA256 | `library/manifest.json`、`config/archive-manifest.json` | 普通 Git；来源清单也存 Release | 下载时用于核验 |
| 课程 ZIP 的解压副本 | `library/*/unpacked/` | 从保存的 ZIP 重建 | 按所选作业解压到 `work/` |
| 虚拟环境、模型权重、缓存、日志、检查点、自动输出 | `.venv/`、`.cache/`、各任务运行目录 | Git 忽略，依赖与来源说明保留 | 在服务器按需建立 |

需要保存为成果的图表、指标和报告放在个人任务的 `reports/`、`figures/` 等目录。`outputs/`、`checkpoints/`、`runs/`、`logs/` 是可重建运行产物，不直接提交。

NJU A0 原有实现已完整转存到 `work/nju-llm-2026/a0/`，`assignments/` 的 A0 保留原始 TODO 模板。现有 Bootcamp 学习记录仍随原 Notebook 保存。外课解压副本的 737 个文件已逐一与原 ZIP 比较，一致且无额外个人文件，因此保存 ZIP 即可还原。

## 为何把大资料放 Releases

已保存 415 份海外课程原件，合计 1374.44 MiB，逐份 SHA256 校验通过。其中 4 份超过普通 Git 的 100 MiB 限制。GitHub 提供 Releases 存放这些附件；代码仓库的克隆不会下载它们。依据：[GitHub 大文件说明](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)、[Releases 存储说明](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)。

当前归档：[materials-2026-10-12](https://github.com/lb-louisben/ml/releases/tag/materials-2026-10-12)。每份原始 ZIP 独立存为附件，便于做作业时只取该包；其余文件按课程打包。目录清单记录每个原文件和每个附件的大小、SHA256 与对应位置。

没有成功取得的 3 份历史原址在 `library/manifest.json` 中保持 `failed`，不列入已存的 415 份。现有本地原件一直保留，归档与上传不会删本地文件。

## 在新电脑恢复完整资料

```bash
git clone --depth=1 git@github.com:lb-louisben/ml.git ml
cd ml
# 全部海外资料；需要 gh CLI，并按需要登录 GitHub
python3 scripts/library_archive.py restore --all
# 按需要重建解压副本及阅读索引
python3 scripts/build_library_catalog.py
python3 scripts/check_structure.py --strict-library
```

仅恢复一门课：

```bash
python3 scripts/library_archive.py restore --course stanford-cs224n-w25
```

恢复时核对归档与文件校验值。已有同名但不同内容的本地文件会阻止覆盖；先把自己的修改移入 `work/` 再恢复。材料获取与包内依赖安装是两个步骤，恢复原件不会安装环境或执行课程代码。

## 新增资料后怎样保存

先下载或整理资料，保留来源和许可文件。使用一个新的快照名称，不覆盖已有快照：

```bash
python3 scripts/library_archive.py pack --tag materials-YYYY-MM-DD
python3 scripts/check_structure.py
python3 -m unittest discover -s scripts/tests -v
git add -- config/archive-manifest.json library/manifest.json library/README.md
# 另行添加自己本次修改的代码和文档
git diff --cached --stat
git commit -m "archive: update learning materials snapshot"
git push origin main
python3 scripts/library_archive.py publish --tag materials-YYYY-MM-DD --target "$(git rev-parse HEAD)"
```

`publish` 先创建草稿，上传并核验附件后公开发布。上传失败时草稿保留，重试会复用已经核验一致的附件。生成缓存位于 `.cache/github-archive/`，不提交 Git；归档清单需与代码一起提交。

不要把整个 `.venv/`、模型下载缓存或压缩包强制 `git add -f`。课程模型按题目提供的来源另取；A5 的 `model/`、`data/` 仅提交说明 README。Git 忽略不会自动移除已跟踪文件，维护时仍需检查暂存范围。
