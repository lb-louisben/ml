# 服务器：按学习分支取作业、写代码和测试

[项目首页](../README.md) · [本机创建学习分支](setup/README.md#用学习分支保持-main-为空白模板)

分支决定读取哪份学习记录，目录配置决定检出哪些练习；二者独立。`main` 是课程模板，ML/DL/LLM 的学习成果保存在各自分支。分支本身包含仓库快照，减少下载使用 partial clone，减少目录使用 sparse checkout。依据：[Git clone](https://git-scm.com/docs/git-clone)、[sparse checkout](https://git-scm.com/docs/git-sparse-checkout)。

## 1. 第一次克隆已发布的学习分支

先按本机教程创建并推送 `codex/study-ml`。服务器上使用尚不存在的新目录 `ml-server`：

```bash
git clone --branch codex/study-ml --single-branch \
  --filter=blob:none --depth=1 --no-tags --no-checkout \
  git@github.com:lb-louisben/ml.git ml-server
cd ml-server
git show HEAD:scripts/server_checkout.py > /tmp/ml-server-checkout.py
python3 /tmp/ml-server-checkout.py --repo-root "$PWD" set ml
git branch --show-current
```

SSH 需要服务器已配置你自己的 GitHub 密钥；也可使用 `https://github.com/lb-louisben/ml.git`，推送前配置 GitHub 认证。整个过程不会先检出完整仓库。

DL/LLM 同样操作，将分支、目标文件夹和目录配置按下表替换。一个课程使用一个服务器文件夹，便于保持环境、学习记录与检出范围一致。

| 课程 | 分支 | 服务器文件夹 | 检出配置 | 自己的通用实验 |
|---|---|---|---|---|
| ML | `codex/study-ml` | `ml-server` | `ml` | `work/courses/ml/` |
| DL | `codex/study-dl` | `dl-server` | `dl` | `work/courses/dl/` |
| LLM | `codex/study-llm` | `llm-server` | `llm` | `work/courses/llm/` |

这些配置取用当前已经存在的示例、补充题和模板，并带入对应个人目录与小型进度表；不代表三门课所有实验已经实现。课程路线与概念短章在本机查看。

## 2. 只取更小的一份练习

```bash
python3 scripts/server_checkout.py list
python3 scripts/server_checkout.py set week1
python3 scripts/server_checkout.py set week3
python3 scripts/server_checkout.py set nju-a0
```

切换配置前先提交改动。只选 `nju-a0` 时包含原始模板与 `work/nju-llm-2026/a0/`，不包含通用课程目录；希望继续访问通用实验时保留课程配置，例如 `set dl`。使用 `set ... --dry-run` 预览范围。工具拒绝在完整本机仓库直接切换。

## 3. 编写与运行 ML/DL 代码

ML 环境在服务器仓库根目录创建：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/bootcamp.txt
mkdir -p work/courses/ml
```

现有回归数据随代码检出，分类和 MLP 使用 sklearn 内置小数据。DL 的 PyTorch 示例可使用根目录 `requirements.txt`，GPU 版 PyTorch 按服务器环境配置；LLM 的具体模板按实际依赖安装。

用 VS Code Remote SSH 打开服务器课程文件夹，编辑自己的 `.py` 或 Notebook。选择该文件夹的 `.venv/bin/python`。写好 `work/courses/ml/train.py` 后，在仓库根目录运行：

```bash
.venv/bin/python work/courses/ml/train.py
```

`train.py` 是你创建的训练入口，不是预先提供的文件。Notebook 也可在 VS Code Remote SSH 中直接选择内核运行。复制参考 Notebook 时检查数据、模块导入和 `OUT`，把输出改到自己的实验目录。

## 4. 本机编写、服务器测试学校作业

以 DL 的 NJU A0 为例，先在本机 `codex/study-dl` 分支中，从模板复制到个人目录；仅在目标目录不存在时复制：

```bash
mkdir -p work/nju-llm-2026
if [ ! -e work/nju-llm-2026/a0 ]; then
  cp -R assignments/nju-llm-2026/a0 work/nju-llm-2026/a0
fi
```

完成对应 TODO 后提交推送。在服务器的 `dl-server` 中，使用 `dl` 或 `nju-a0` 配置，运行：

```bash
git pull --ff-only
.venv/bin/python -m pip install -r requirements/nju-a0.txt
(cd work/nju-llm-2026/a0 && ../../../.venv/bin/python -m pytest test_toy.py -q)
```

先用第 3 节的方法建立 `.venv`。A0 公开测试支持 CPU；未实现 TODO 时失败属正常现象。`test_with_ref.py` 需要私有 `ref` 包，自学跳过。其他模板在各自目录运行公开测试并检查实际依赖，不能把 A0 环境套到所有作业。

同样可以直接在服务器复制、编写、测试，然后从服务器提交学习分支。

## 5. 保存到学习分支

在仓库根目录运行，以 A0 为例：

```bash
git branch --show-current
git status --short
git add -- work/nju-llm-2026/a0
git diff --cached --stat
git commit -m "study: implement and test A0"
git push
```

通用 ML 实验改为暂存 `work/courses/ml/`。修改进度表时额外暂存 `course/TRACKER.md`。初次克隆学习分支已设置对应远端，普通 `git push` 推送当前学习分支；不要写 `git push origin main`。

本机提交推送 → 服务器 `git pull --ff-only` → 执行测试；服务器修改推送 → 本机 `git pull --ff-only`。同步前先提交自己的工作；两端同时产生新提交时，在完整本机仓库处理分叉，不强制覆盖。

模板更新先按本机教程合并进学习分支，服务器再拉取该学习分支。浅克隆只追踪所选分支，跨课程时推荐新建对应服务器文件夹，而不是直接在浅克隆里切换另一个远端分支。

模型、环境、数据下载和输出保留在服务器，不提交普通 Git。保存少量指标与结论到任务说明中；完整文档检查用于本机，服务器只运行所选练习的检查。
