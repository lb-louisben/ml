# NJU · 大语言模型基础 · 2026

[返回 ML 项目](../../README.md)

这门课的内容、运行方法、作业和 Git 操作都在本页。按公开材料自学，成果提交到自己的 `git@github.com:lb-louisben/ml.git`。

[讲义与练习](#讲义与练习) · [作业](#作业) · [同步与保存](#同步与保存) · [环境与模型](#环境与模型)

## 开始学习

在项目根目录运行：

```bash
cd "/Users/louis/Documents/workspace/School/cources/machine learning"
bash scripts/start_nju.sh
```

JupyterLab 选择 **ML · Python (.venv)** 内核，再打开下表的学习 Notebook。本机依赖、Graphviz 和完整 Qwen3-0.6B 模型已安装；第 1–4 讲均已有通过的运行记录。

## 讲义与练习

| 讲次 | 老师讲义 | 用来运行和学习的 Notebook |
|---|---|---|
| 1 · 课程简介 | [讲义](2026/lecture1.md) | [本地模型副本](../../work/nju-llm-2026/lecture1.ipynb) |
| 2 · 特征空间的变换 | [讲义](2026/lecture2.md) | [原版 Notebook](2026/notebook/lecture2.ipynb) |
| 3 · 反向传播 | [讲义](2026/lecture3.md) | [兼容副本](../../work/nju-llm-2026/lecture3.ipynb) |
| 4 · 大语言模型解析 I | [讲义](2026/lecture4.md) | [本地模型副本](../../work/nju-llm-2026/lecture4.ipynb) |

[自动生成的全部讲义清单](LECTURES.md) 包含后续同步的新讲次、原版 Notebook 和老师的补充说明。

第 1、4 讲副本自动定位本地模型；第 1 讲默认关闭思考模式，两次生成各限制为 64 个新 token。第 3 讲副本将旧 profiler 调用替换成当前 PyTorch 支持的接口。老师原件保持不变。

目录只分三种用途：

| 位置（相对项目根目录） | 放什么 |
|---|---|
| `library/nju-llm-2026/` | 本页、老师讲义、作业原始模板及来源记录 |
| `work/nju-llm-2026/` | 自己修改的 Notebook、作业实现、笔记和测试 |
| `.cache/` | 模型、下载缓存和运行输出，不提交 Git |

修改老师的 Notebook 前先复制到 `work/nju-llm-2026/`；上表中三个个人副本已经准备好。

## 作业

[官方公开作业仓库](https://github.com/NJUDeepEngine/open-llm-assignments) 的 main 和六个作业分支已一次性归档，后续不再拉取。以下直接进入老师的任务说明与源码：

| 编号 | 内容 | 题目 | 原始模板说明 |
|---|---|---|---|
| A0 | Onboarding / MatMul with Importance | [tasks](assignments/repository/a0-main/tasks/) | [a0-main](assignments/repository/a0-main/README.md) |
| A1 | Norm + Embedding | [tasks](assignments/repository/a1-main/tasks/) | [a1-main](assignments/repository/a1-main/README.md) |
| A2 | MLP | [tasks](assignments/repository/a2-main/tasks/) | [a2-main](assignments/repository/a2-main/README.md) |
| A3 | Attention | [tasks](assignments/repository/a3-main/tasks/) | [a3-main](assignments/repository/a3-main/README.md) |
| A4 | Transformer | [tasks](assignments/repository/a4-main/tasks/) | [a4-main](assignments/repository/a4-main/README.md) |
| A5 | Exploring Llama | [tasks](assignments/repository/a5-main/tasks/) | [a5-main](assignments/repository/a5-main/README.md) |

**编号以代码仓库为准。** [旧博客题面快照](assignments/BLOG.md) 仅作参考：博客 A0 是环境引导、A1 才是矩阵乘法，与代码仓库编号不同。HTML 中的样式、图片和公式脚本仍需联网。

首次开始 A0，在项目根目录复制模板：

```bash
if [ ! -e work/nju-llm-2026/a0 ]; then
  cp -R library/nju-llm-2026/assignments/repository/a0-main work/nju-llm-2026/a0
fi
```

修改 `work/` 中的 TODO，完成后运行公开测试：

```bash
(cd work/nju-llm-2026/a0 && ../../../.venv/bin/python -m pytest test_toy.py -q)
```

其他作业同样复制对应分支，测试命令以该任务说明为准。各份作业在自己的目录单独测试，避免同名 `src` 包冲突。模板尚未完成，不能预期测试立即通过。

无需 Classroom、学号、评分 webhook 或官方评分服务；`test_with_ref.py` 需要未公开的 `ref` 包，自学时跳过。用公开测试及自己补充的 PyTorch / Autograd 对照测试验收，在个人作业记录中写清实现范围、命令、结果和未完成部分。本地通过不代表官方隐藏测试分数。

老师的 requirements 包含 NVIDIA/CUDA 的 Triton 等依赖，不能在本机 Mac 上原样全装。A5 的 Llama 权重与数据只有获取说明，尚未下载；已下载的 Qwen3 用于讲义。

## 同步与保存

### 更新讲义

```bash
python3 scripts/sync_nju.py lectures
```

来源是 [官方讲义仓库](https://github.com/NJUDeepEngine/llm-course-lecture) `main` 分支的 `2026/`，连同引用的配图同步。本机也可用 `git sync-lectures`。默认使用当前代理；代理不可用且能够直连时加 `--direct`。

脚本检测到本地修改时会停止替换，先将自己的版本移到 `work/` 再同步。下载失败可重试，`0 updated` 表示内容一致。上游移除的旧文件保留在本地，当前文件以讲义清单为准。

旧命令 `git sync-assignments` 仅提示已归档，不联网、不改文件；`git sync-nju` 或 `python3 scripts/sync_nju.py all` 只更新讲义并跳过作业。

### 提交到自己的仓库

在项目根目录运行，按实际修改选择文件：

```bash
git status
# 自己的学习成果
git add -- work/nju-llm-2026
# 如果也更新了老师资料
git add -- library/nju-llm-2026
git diff --cached --stat
git commit -m "study: update NJU course work"
git push
```

先检查暂存区，已有的其他文件也会进入这次提交。暂时不提交某文件可用 `git restore --staged -- 文件路径`，不会删除文件内容。首次推送当前 main 分支可用 `git push -u origin main`。

`origin` 与默认推送目标均为 `git@github.com:lb-louisben/ml.git`，可用 `git remote -v` 核对。`git pull --ff-only origin main` 获取自己仓库的新提交；老师讲义使用上面的专用同步命令。若无法快进，先检查分支差异，不要强制推送。

讲义、配图、作业源码与公开测试、来源清单、个人代码和工具均纳入 Git；`.venv/`、`.cache/` 与模型权重不纳入。换电脑克隆自己的仓库即可取得已提交的资料，无需再下载作业。Git 本地简写不随克隆迁移，Python 同步命令始终可用。

## 环境与模型

共用根目录 `.venv`，VS Code 选择 `.venv/bin/python`。依赖见 [requirements.txt](../../requirements.txt)，已验证版本见 [requirements-tested.txt](../../requirements-tested.txt)。安装新包后重启 Notebook 内核。

换电脑时先按 [项目环境安装说明](../../docs/setup/README.md) 创建 `.venv`，再在项目根目录运行：

```bash
.venv/bin/python -m pip install --cache-dir .cache/pip -r requirements.txt
brew install graphviz  # macOS：第 3 讲绘图需要原生 dot 程序
.venv/bin/python scripts/download_nju_model.py
bash scripts/start_nju.sh
```

Python 的 graphviz 包不能替代原生 `dot`；找不到绘图程序时用 `dot -V` 检查。当前为 Apple Silicon Mac，第 2 讲需要 MPS；CUDA 专用代码需使用相应的 Linux/NVIDIA 环境。

已下载 **Qwen/Qwen3-0.6B** 完整权重、分词器、配置和许可证，9 个文件约 1.52 GB，存放在 `.cache/llm-course/qwen3-tokenizer/`。版本固定为 `c1899de289a04d12100db370d81485cdf75e47ca`，下载脚本支持复用文件、断点续传和校验。权重 SHA256 已与官方 LFS 一致，完整记录在该目录的 `download-source.json`。

### 验证与排查

```bash
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_nju_env.py
.venv/bin/python scripts/verify_nju_model.py
```

环境检查离线验证关键库、随机小模型的前向/反向、分词、权重存取、生成和 Graphviz。模型检查离线执行第 1、4 讲个人副本，可加 `--only 1` 或 `--only 4`。输出保存在 `.cache/nju-validation/`。

2026-09-22～23 已验证：Python 3.14.6、PyTorch 2.14.0、Transformers 4.57.6，`pip check` 与环境检查通过；第 1–4 讲分别通过 10、17、19、31 个代码单元，其中第 2 讲为原版，其余使用上表副本。第 1、4 讲使用真实模型权重离线执行。

同步代理错误可尝试 `--direct`；SSH `Permission denied (publickey)` 则检查自己 GitHub 账号的 SSH 密钥，它与讲义下载是独立连接。

## 来源记录

- [讲义清单与校验值](manifest.json)：记录官方提交、文件树及逐文件校验值。
- [作业分支与校验值](assignments/repository-manifest.json)：7 个分支、130 个原始文件的一次性快照。
- [旧博客快照清单](assignments/manifest.json)：保留历史题面来源。

老师目录中的 README、LICENSE 和任务说明是原始资料的一部分，保留原样；本项目的课程使用说明统一维护在本页。
