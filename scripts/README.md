# 项目维护工具

[返回项目首页](../README.md) · [目录放置规则](../docs/PROJECT_STRUCTURE.md)

[服务器教程](../docs/SERVER_GUIDE.md) · [GitHub 存储方案](../docs/GITHUB_STORAGE.md)

以下命令从项目根目录执行。`python3` 用于只依赖标准库的维护工具；Notebook 与模型验证使用本项目的 `.venv`。

## 日常命令

| 用途 | 命令 |
|---|---|
| 查看服务器检出配置 | `python3 scripts/server_checkout.py list` |
| 在服务器选择 NJU A0 | `python3 scripts/server_checkout.py set nju-a0` |
| 恢复全部海外原件 | `python3 scripts/library_archive.py restore --all` |
| 只下载指定作业 ZIP | `python3 scripts/library_archive.py fetch --file <课程/ZIP文件>` |
| 生成完整资料归档及校验清单 | `python3 scripts/library_archive.py pack --tag <快照名>` |
| 上传并核验归档 | `python3 scripts/library_archive.py publish --tag <快照名> --target <提交号>` |
| 检查维护文档和 Notebook 的本地链接、图片引用与文件语法 | `python3 scripts/check_structure.py` |
| 下载或重试其他学校的资料 | `python3 scripts/download_courses.py` |
| 重建其他学校的阅读索引并解压作业包 | `python3 scripts/build_library_catalog.py` |
| 补充 NJU 2026 新增讲义 | `python3 scripts/sync_nju.py lectures` |
| 下载 NJU 讲义使用的本地模型 | `.venv/bin/python scripts/download_nju_model.py` |
| 启动配置了本地模型路径的 JupyterLab | `bash scripts/start_nju.sh` |
| 验证 Week 1 教学 Notebook | `.venv/bin/python scripts/verify_week1.py` |
| 验证 Week 2/3 带练 Notebook | `.venv/bin/python scripts/verify_bootcamp.py` |
| 离线验证 NJU Python 与 Graphviz 环境 | `.venv/bin/python scripts/verify_nju_env.py` |
| 用已下载的模型离线验证 NJU 个人副本 | `.venv/bin/python scripts/verify_nju_model.py` |

NJU 同步保留已有资料文件，仅补充新增讲义；作业是固定快照。命令 `sync_nju.py assignments` 只确认作业归档存在，`sync_nju.py all` 同步讲义并跳过作业。个人修改与实现放在 [`work/`](../work/README.md)。

## 离线检查与工具测试

```bash
python3 scripts/check_structure.py
python3 -m unittest discover -s scripts/tests -v
```

若使用 pytest：

```bash
.venv/bin/python -m pytest
```

项目根目录的 `pytest.ini` 仅收集 `scripts/tests/` 中的工具回归测试。课程题目中的测试需要在自己的作业目录中按课程说明单独运行。工具测试使用临时目录和模拟下载，不联网、不执行学生作业。

## 生成文件与维护边界

| 工具 | 管理的文件 |
|---|---|
| `download_courses.py` | 其他学校的原件、网页快照、`library/manifest.json`、`library/README.md` 与对应课程 `README.md` |
| `build_library_catalog.py` | 其他学校的 `unpacked/`、`library/README.md`、对应课程 `README.md`、`course/READING_LIST.md` |
| `sync_nju.py` | NJU 新增讲义与配图、`library/nju-llm-2026/manifest.json`、未被手工修改的 `LECTURES.md` |
| Notebook 与环境验证工具 | 各周 `outputs/` 或 `.cache/nju-validation/` 中的验证副本与报告 |

两个资料索引生成器都会保留 NJU 独立入口；NJU 使用自己的来源清单，不计入其他学校的下载数量和大小。`library/nju-llm-2026/README.md` 与 `work/nju-llm-2026/README.md` 由人工维护。

2026-09-21 的一次性目录迁移脚本已归档在 [`docs/archive/reorganize_learning_2026_09_21.py`](../docs/archive/reorganize_learning_2026_09_21.py)。它记录历史迁移操作，日常维护使用上面的命令。
