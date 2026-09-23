# 机器学习学习项目 · 使用指南

这个项目集中管理机器学习学习所需的 **课程、练习、原版资料和个人实验**。内容从 Python 与数据分析入门，延伸到经典机器学习、深度学习和 NLP / LLM；本页是整个项目的入口。

**NJU 2026：** [课程总入口：讲义、作业、环境和操作说明](library/nju-llm-2026/README.md)

[快速跳转](#quick-links) · [目录总览](#layout) · [如何使用](#usage) · [启动环境](#run)

<a id="quick-links"></a>

## 快速跳转

| 我想…… | 打开这里 |
|---|---|
| 查看整体学习路线与当前任务 | [学习指南](course/STUDY_GUIDE.md) |
| 按次推进前期学习：材料、练习、完成标准 | [27 次学习总览](course/bootcamp/README.md) |
| 学第一部分：Python、数据处理与回归 | [Week 1 目录](course/bootcamp/week1/README.md) |
| 第一次实现分类与模型评估 | [Week 2 目录](course/bootcamp/week2/README.md) · [带注释教程](course/bootcamp/week2/classification_walkthrough.ipynb) |
| 第一次实现神经网络 | [Week 3 目录](course/bootcamp/week3/README.md) · [NumPy 带练](course/bootcamp/week3/01_numpy_network_walkthrough.ipynb) · [PyTorch 对照](course/bootcamp/week3/02_pytorch_training_walkthrough.ipynb) |
| 查中文讲义、术语或公式 | [讲义目录](course/materials/README.md) · [术语表](course/materials/GLOSSARY.md) · [公式卡](course/materials/REFERENCE_CARD.md) |
| 找作业、测验或项目要求 | [作业](course/assignments/README.md) · [测验](course/tests/README.md) · [项目](course/projects/README.md) |
| 找学校原版课件、题目与代码包 | [官方资料库](library/README.md) · [逐主题文件索引](course/READING_LIST.md) |
| 直接跟随 NJU 2026 年大语言模型课程 | [2026 讲义、配套 Notebook 与作业入口](library/nju-llm-2026/README.md) |
| 记录自己的进度与成果 | [进度表](course/TRACKER.md) · [个人实验目录](work/README.md) |
| 配置环境或检查是否能运行 | [基础环境](docs/setup/README.md) · [环境测试](docs/setup/00_环境测试.ipynb) · [PyTorch 环境](docs/setup/DEEP_LEARNING.md) |
| 保存学习记录、了解项目维护 | [Git 指南](docs/GIT_GUIDE.md) · [技术文档](docs/README.md) |

<a id="layout"></a>

## 目录总览

```text
machine learning/
├── README.md                     ← 使用指南与项目总入口（本页）
├── course/                       ← 学什么：学习安排、教材与任务要求
│   ├── README.md                 ← 课程内容索引
│   ├── STUDY_GUIDE.md             ← 学习顺序与验收范围
│   ├── TRACKER.md                 ← 当前任务与完成证据
│   ├── bootcamp/                 ← 入门实践，三部分同级
│   │   ├── week1/                ← Python、数据分析、回归
│   │   │   ├── day1/ … day7/      ← 逐日 Notebook
│   │   │   ├── data/             ← 配套数据与来源说明
│   │   │   └── project/           ← 端到端参考项目
│   │   ├── week2/                ← 分类任务与完整带练 Notebook
│   │   └── week3/                ← NumPy / PyTorch 带练与网络实现
│   ├── materials/                ← 中文导读、术语表、公式卡
│   ├── assignments/              ← A01～A08 补充作业
│   ├── tests/                    ← 阶段测验与答案
│   └── projects/                 ← 项目题目、要求与评分依据
├── library/                      ← 查什么：学校原版资料，按课程归档
├── work/                         ← 自己做什么：独立练习、实验与项目成果
├── docs/                         ← 怎样使用与维护项目
│   ├── setup/                    ← 环境指南与环境测试 Notebook
│   ├── GIT_GUIDE.md               ← Git 使用方法
│   ├── PROJECT_STRUCTURE.md       ← 文件归属规则与迁移记录
│   ├── VALIDATION.md              ← 资料验证记录
│   └── archive/                  ← 历史方案
├── scripts/                      ← 资料下载、索引生成、Notebook 验证
├── requirements.txt              ← 全部课程依赖（含 PyTorch）
└── requirements-tested.txt       ← 本机已验证版本
```

`course/projects/` 保存项目要求，自己的实现放在 `work/`。`library/` 保存学校原件；要修改其中的作业代码时，先复制到 `work/`。

`.venv/` 是全部课程共用的 Python 环境，包含 PyTorch，`.cache/`、`.jupyter/` 是运行缓存和配置；它们不属于课程内容。

<a id="usage"></a>

## 如何使用

**第一次打开：** 按 [环境指南](docs/setup/README.md) 启动 JupyterLab，运行 [环境测试](docs/setup/00_环境测试.ipynb)，再查看 [前期学习总览](course/bootcamp/README.md)，按已有基础选择起点。

**日常学习：** 从 [进度表](course/TRACKER.md) 找到当前单元编号（如 W1-03），打开周目录中的具体任务及对应 Notebook；需要解释时查中文讲义，需要原课细节时进入资料库。完成后记录成果链接、卡点与下一步。

**做独立实验：** 在 [work/](work/README.md) 下按任务建目录，保存代码、结果和运行说明。Week 1 的现有学习笔记保留在对应日目录，可以继续在那里填写作业。

**第一次实现：** Week 2/3 的带练 Notebook 已把概念、材料、注释示例和练习放在一起。先读解释并预测输出，再逐段运行，随后改一个条件观察结果；最后在 `work/` 中独立重建。源教程中的 TODO 是练习提示，不会阻塞示例运行。

**找具体文件：** 从周目录按单元编号查找对应章节。Week 3 的两个 Notebook 统一导入教材目录中的 `numpy_mlp.py`；第一次直接在原位置学习。自己的实现写在 `work/` 中，修改导入路径与输出路径后再运行，不要只复制一个同名文件就以为已替换教材实现。

<a id="run"></a>

## 启动环境

在项目根目录运行：

```bash
source .venv/bin/activate
python -m jupyter lab
```

环境尚未建立时，按 [安装说明](docs/setup/README.md) 创建。其他学校作业的依赖和数据以各自包内 README 为准。

维护与检查命令也在项目根目录运行：

| 操作 | 命令 |
|---|---|
| 验证 Week 1 的 8 本教学 Notebook | `.venv/bin/python scripts/verify_week1.py` |
| 验证 Week 2/3 的 3 本带练 Notebook | `.venv/bin/python scripts/verify_bootcamp.py` |
| 下载或重试学校资料 | `python3 scripts/download_courses.py` |
| 同步 NJU 2026 讲义 | `python3 scripts/sync_nju.py lectures` |
| NJU 固定作业模板（已一次性归档） | [A0–A5 源码、题目与测试](library/nju-llm-2026/README.md#作业) |
| 重建资料库目录与文件索引 | `python3 scripts/build_library_catalog.py` |

Notebook 验证副本保存在各周的 `outputs/verified/`；示例导出的图表与模型也在各周 `outputs/`，不会覆盖源 Notebook。详细目录规则见 [项目结构说明](docs/PROJECT_STRUCTURE.md)。
