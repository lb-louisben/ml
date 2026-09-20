# Machine Learning 学习项目

从 Python 数据分析到第一个回归模型。第一周教材沿用 `week1/dayN/` 和 Jupyter Notebook 格式。

## 从哪里开始

你已完成的第一、二天原笔记保留。现在打开 [第三天 Pandas](week1/day3/03_Pandas_data_cleaning.ipynb)。
完整安排见 [第一周导航](week1/README.md)。先做各天的基础与 Assignment，再按时间补深度、广度和 Bonus；答案在 Notebook 末尾。

## 运行

在本项目根目录终端执行：

```bash
source .venv/bin/activate
python -m jupyter lab
```

VS Code 打开整个项目文件夹，选择 `.venv/bin/python` 作为 Notebook 内核。如果内核为空，先检查是否处于 Restricted Mode；对于你信任的本项目，在 Manage Workspace Trust 中信任该文件夹，然后 Reload Window。

新电脑先 `python3 -m venv .venv`，再运行 `.venv/bin/python -m pip install -r requirements.txt`。
已验证的主要版本见 `requirements-tested.txt`，它固定直接依赖，不是跨平台完整锁文件。当前验证环境为 macOS ARM64 / Python 3.14.6。

第三至七天和综合项目各自可从干净内核独立运行，不依赖前一天变量或导出文件。内核工作目录需位于本项目内。建议 Restart Kernel 后 Run All。
真实数据随项目保存，运行不需要联网。`week1/outputs/` 保存运行生成的结果，已忽略 Git。

## Git

本地分支为 `main`。原笔记已先提交作为起点。没有配置远程仓库，也没有上传到 GitHub。
日常提交与查看历史见 [Git 使用指南](GIT_GUIDE.md)。

## 验证教材

```bash
.venv/bin/python scripts/verify_week1.py
```

脚本只执行新增的 8 本 Notebook，在 `week1/outputs/verified/` 留下执行版与结果，不改动教材或原笔记。
这会重现固定的参考项目评估，不会证明学员已独立完成作业。
