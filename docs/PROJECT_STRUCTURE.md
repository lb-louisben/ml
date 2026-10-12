# 项目目录与文件归属

[项目首页](../README.md) · [GitHub 存储方案](GITHUB_STORAGE.md) · [服务器教程](SERVER_GUIDE.md)

## 放置规则

| 内容 | 位置 |
|---|---|
| 作业总入口、入门练习、题目、原始模板 | `assignments/` |
| Bootcamp Notebook、小数据、NumPy 网络 | `assignments/bootcamp/week1/`～`week3/` |
| 中文补充作业题目 | `assignments/core/A01/`～`A08/` |
| NJU 原始作业与来源清单 | `assignments/nju-llm-2026/a0/`～`a5/`、`SOURCES.json` |
| 学习路线、进度、中文教材、测验、项目要求 | `course/` |
| 学校讲义、参考书与课程来源 | `library/`；海外大资料保存在 GitHub Releases |
| 中文作业的个人实现 | `work/assignments/<编号>/`，开始时创建 |
| NJU 个人作业实现 | `work/nju-llm-2026/a0/`～`a5/` |
| NJU 个人讲义与学习 Notebook | `work/nju-llm-2026/lecture*.md`、`lecture*.ipynb` |
| 独立实验与正式报告 | `work/<任务名>/`；需要保存的结果用 `reports/` 或 `figures/` |
| 临时个人试验 | `work/scratch/` |
| 服务器检出与完整归档清单 | `config/` |
| 任务最小依赖 | `requirements/`；根 requirements 是完整本机环境 |
| 检出、归档、下载、同步和验证工具 | `scripts/` |
| 工具回归测试 | `scripts/tests/`；`course/tests/` 是学习测验 |
| 使用说明、环境和历史迁移 | `docs/`、`docs/setup/`、`docs/archive/` |

`assignments/` 的 NJU 模板保留老师的 TODO；个人 A0 实现已从原件目录转存到 `work/`，不丢原有代码。`SOURCES.json` 保留原始分支路径、SHA256，并通过 `local_roots` 记录现在的放置位置。

## 运行与生成约定

从项目根目录启动 `.venv` 和 JupyterLab。Bootcamp Notebook 向上定位 `assignments/bootcamp/`；Week 1 使用随练习保存的成绩数据，Week 2/3 使用自带数据，Week 3 共用同目录 `numpy_mlp.py`。从周目录或日目录也能运行。

自动验证副本位于 `assignments/bootcamp/week*/outputs/verified/`；缓存、运行产物、环境和模型权重由 Git 忽略。完整存储范围、海外资料恢复和指定 ZIP 下载见存储方案，服务器用 `server_checkout.py` 选择作业。

| 生成文件 | 维护工具 |
|---|---|
| `library/README.md`、海外课程 README、`course/READING_LIST.md` | `download_courses.py`、`build_library_catalog.py` |
| `library/nju-llm-2026/LECTURES.md`、讲义来源清单 | `sync_nju.py`，保持已有内容，仅补充新文件 |
| `config/archive-manifest.json` 与 Release 附件 | `library_archive.py pack/publish` |

索引入口修改需要同步修改生成器，避免重建丢失。NJU 与海外资料分开维护来源清单；NJU 不计入外课的 415 份原件统计。

修改或移动文件后，执行 `python3 scripts/check_structure.py`；完整恢复资料后加 `--strict-library`。该工具验证自有文档链接、图片引用、Notebook JSON 和工具语法，不执行 Notebook或改写老师原件。工具测试与 Notebook 验证命令见 [工具说明](../scripts/README.md)。

## 迁移记录

2026-09-21：将原课程、三周入门内容与环境说明整理到 `course/`、`docs/`；历史脚本为 [reorganize_learning_2026_09_21.py](archive/reorganize_learning_2026_09_21.py)。它记录当时目录，不用于当前迁移。

2026-10-12：先统一 A01～A08 编号目录，整理个人草稿与工具测试，修复个人第二讲图片路径。随后按服务器隔离需求，将 Bootcamp 与中文作业移到 `assignments/bootcamp/`、`assignments/core/`，NJU A0～A5 移到 `assignments/nju-llm-2026/`；更新全部自有文档和 Notebook 路径。海外原件按课程与 ZIP 分别存入 Releases，提供检出配置、归档校验和完整使用教程。
