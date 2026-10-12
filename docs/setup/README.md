# 本机环境与日常使用

[项目首页](../../README.md) · [课程路线](../../course/STUDY_GUIDE.md)

## 首次安装

在项目根目录运行；已有 `.venv` 时跳过创建，只安装所需依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name ml --display-name "ML · Python (.venv)"
```

这些依赖支持现有回归、分类与 NumPy/PyTorch 示例。LLM 模型与专题依赖在选择具体任务时再配置。`requirements-tested.txt` 是现有示例的本机版本记录，不是跨平台锁文件。

## 每次学习

```bash
source .venv/bin/activate
python -m jupyter lab
```

在 JupyterLab 选择 `ML · Python (.venv)`；VS Code 打开 Notebook 后选择项目 `.venv/bin/python`。从项目根目录启动，打开路线指定的练习。结束时按 `Control+C` 停止服务，再运行 `deactivate`。

先运行参考程序并解释各段，再在 `work/<任务>/` 保存自己的改动与结果。复制 Notebook 后检查数据、导入与输出路径，避免新实验仍写回参考示例目录。

## 检查与排错

[环境测试 Notebook](00_环境测试.ipynb) 可检查数据分析与线性回归。先查看 `sys.executable`，缺包时在这个解释器里安装依赖；结果异常先重启内核、从头执行。

```bash
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_week1.py
.venv/bin/python scripts/verify_bootcamp.py
```

两项示例验证使用干净内核，执行副本与结果放进被 Git 忽略的 `outputs/`。无需每次学习全部重跑；修改参考代码或环境后按受影响范围验证。

## 用学习分支保持 main 为空白模板

Git 分支属于整个仓库。在项目根目录操作：`main` 保存课程路线、题目和示例；学习成果保存到对应分支，自己的实验放进 `work/`。每门课一个分支即可，无需给每个模型另建分支。切换前先保存并提交改动；未提交文件可能随切换进入另一个分支。

第一次开始 ML，在工作目录干净时运行：

```bash
git switch main
git pull --ff-only origin main
git switch -c codex/study-ml
mkdir -p work/courses/ml
git push -u origin codex/study-ml
```

创建 DL 或 LLM 时也先回到更新后的 `main`，将分支名分别换成 `codex/study-dl`、`codex/study-llm`，个人目录换成 `work/courses/dl`、`work/courses/llm`。已有分支直接 `git switch codex/study-ml`，不再使用 `-c`。

打开现有示例阅读；自己的代码、改写和笔记放进对应课程个人目录。修改参考程序或进度表也只在学习分支进行。回到 `main` 后，已提交的学习改动不会出现在模板中；被忽略的环境和输出仍保留在本机。

## 保存与本机/服务器同步

在学习分支、仓库根目录运行；按实际修改选择路径：

```bash
git branch --show-current
git status --short
git add -- work/courses/ml
git diff --cached --stat
git commit -m "study: record ML experiment"
git push
```

学校作业实现如果在 `work/nju-llm-2026/a0/`，暂存该路径；进度表有修改时额外暂存 `course/TRACKER.md`。成果提交到当前学习分支，保持 main 的进度和练习为空白模板。

本机编写并推送后，服务器在同一分支执行 `git pull --ff-only`，再测试；服务器修改后提交推送，本机再执行 `git pull --ff-only`。两端轮流工作前先同步。两端已分别产生新提交时，回完整本机仓库解决分叉，再推送；不要用 main 的拉取/推送命令保存学习成果。

模板有更新时，先在完整本机仓库提交自己的改动，然后在学习分支运行：

```bash
git fetch origin
git merge origin/main
git push
```

这样把模板更新带入学习分支。学习成果留在学习分支，不将整条学习分支合并回 main。服务器操作见 [分支与最小检出教程](../SERVER_GUIDE.md)。
