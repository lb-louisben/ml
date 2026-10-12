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

## VS Code：跳转、补全与调试

用“打开文件夹”打开项目根目录。项目已推荐 Python、Pylance、Python Debugger 和 Jupyter；本机这四项均已安装。选择项目 `.venv/bin/python`，Notebook 的内核也选择同一个环境。默认解释器配置只对首次选择生效，已有错误选择时运行 `Python: Select Interpreter` 手动修正。

- 函数跳转：`F12` 或按住 Command 点击；Mac 的 F12 如果控制媒体键，使用 Fn+F12，或右键“Go to Definition”。
- 查看引用：右键“Find All References”；悬停查看参数与类型；`Control+Space` 请求补全。
- 调试：打开自己的 `.py`，设断点，选择“Python: 当前文件（项目根目录）”。
- 学校作业中的同名 `src` 按各作业目录独立解析，不把六份作业同时加入一条全局导入路径。代码中新建包时保留 `__init__.py`，避免用 `torch.py`、`numpy.py` 等名字遮蔽第三方库。

解释器同时决定运行、调试与第三方库的代码提示；设置依据：[VS Code Python 设置](https://code.visualstudio.com/docs/python/settings-reference)。

## PyCharm：项目环境与源码根目录

本机已配置项目 `.venv`、正确的项目根目录、NumPy 示例源码目录，以及六份独立作业模块。打开整个项目，等待索引完成；右键“Go to Declaration or Usages”可跳转，Mac 默认键位通常为 Command+B，也可 Command 点击函数名。

换电脑或复制新的 NJU 模板到 `work/` 后，先关闭 PyCharm 中的当前项目，再运行下面命令生成该电脑的本地配置，然后重新打开项目：

```bash
python3 scripts/configure_pycharm.py
```

在 PyCharm 的 Settings → Python Interpreter 选择 **Existing environment**，指向当前项目 `.venv/bin/python`。生成器保留现有 SDK 设置，未知的新电脑需要完成这次选择；不会在全局注册解释器或自动安装包。项目运行目录设为项目根目录；独立学校作业的 pytest 运行目录设为自己的作业目录。

各作业模块不互相依赖，避免 `src.functional` 跳到另一份模板。复制了新的个人作业目录后重新生成配置。PyCharm 的 `.idea/` 只保存在本机，不提交 Git。依据：[PyCharm 解释器](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html)、[源码与排除目录](https://www.jetbrains.com/help/pycharm/configuring-project-structure.html)。

## 三种“忽略”分别做什么

- `.gitignore`：环境、模型、缓存与运行输出不上传 GitHub。
- VS Code 的文件、搜索、监听与 Python 分析排除：这些目录不干扰浏览和代码分析。
- PyCharm 的 Excluded：排除缓存、环境副本、模型与输出的项目索引；第三方库仍通过选定解释器提供补全和跳转。

参考源码、自己的 `work/` 代码和教学小数据保留可见。排除目录不删除文件，也不等于关闭 Python 库的导航。PyCharm 的项目树若仍显示被排除文件，可在 Project 面板的 Options 关闭“Show Excluded Files”。

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
