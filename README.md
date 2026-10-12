# 机器学习学习项目

本项目按 **机器学习 → 深度学习 → LLM** 的先修关系学习：先认识模型家族，再通过完整代码、局部实现和小项目掌握它们。本科核心与研究生扩展使用同一张课程地图。

**先打开：[三门课课程设计与正确起点](course/STUDY_GUIDE.md)**

[可用练习](assignments/README.md) · [本机环境](docs/setup/README.md) · [服务器只拉作业](docs/SERVER_GUIDE.md)

<a id="quick-links"></a>

## 从哪里开始

| 我想…… | 入口 |
|---|---|
| 在服务器只做 NJU、Bootcamp 或某份中文作业 | [最小检出与使用教程](docs/SERVER_GUIDE.md) |
| 了解内容存放与完整恢复 | [GitHub 存储方案](docs/GITHUB_STORAGE.md) |
| 先认识模型和学习顺序 | [模型地图、三门课大纲与先修关系](course/STUDY_GUIDE.md) |
| 记录当前任务与成果 | [进度表](course/TRACKER.md) |
| 做入门实践 | [27 次学习总览](assignments/bootcamp/README.md) · [Week 1](assignments/bootcamp/week1/README.md) · [Week 2](assignments/bootcamp/week2/README.md) · [Week 3](assignments/bootcamp/week3/README.md) |
| 找 A01～A08 补充题目或 NJU A0～A5 | [中文作业](assignments/core/README.md) · [NJU 作业](assignments/nju-llm-2026/README.md) |
| 跟随 NJU 大语言模型课程 | [讲义、Notebook、环境](library/nju-llm-2026/README.md) · [我的学习记录](work/nju-llm-2026/README.md) |
| 查中文概念、术语或公式 | [讲义目录](course/materials/README.md) · [术语表](course/materials/GLOSSARY.md) · [公式卡](course/materials/REFERENCE_CARD.md) |
| 找学校原版材料与海外作业包 | [资料库](library/README.md) · [文件索引](course/READING_LIST.md) · [Releases](https://github.com/lb-louisben/ml/releases/tag/materials-2026-10-12) |
| 做独立实验、阶段测验或项目 | [个人成果](work/README.md) · [测验](course/tests/README.md) · [项目要求](course/projects/README.md) |
| 配置本机环境或维护仓库 | [环境安装](docs/setup/README.md) · [Git 操作](docs/GIT_GUIDE.md) · [工具命令](scripts/README.md) |

<a id="layout"></a>

## 目录总览

```text
machine learning/
├── assignments/                  # 服务器所需练习，按任务选择
│   ├── bootcamp/week1..3/        # 入门 Notebook、小数据与网络实现
│   ├── core/A01..A08/            # 中文补充题目
│   └── nju-llm-2026/a0..a5/      # 原始模板、题目、公开测试
├── work/                         # 个人代码、作业、笔记与报告
│   ├── nju-llm-2026/a0/          # 已有 A0 学习实现
│   ├── nju-llm-2026/lecture*     # 个人课程 md/ipynb 文件
│   └── scratch/                  # 临时草稿
├── course/                       # 学习路线、中文教材、测验、项目要求
├── library/                      # NJU 原件与海外资料本地恢复位置
├── config/                       # 服务器检出配置与归档校验清单
├── requirements/                 # 按任务安装的最小依赖
├── docs/                         # 使用教程、环境、结构和历史记录
├── scripts/                      # 检出、资料归档、同步与验证工具
│   └── tests/                    # 维护工具的离线回归测试
├── requirements.txt              # 本机完整学习环境
├── requirements-tested.txt       # 本机已验证版本
└── pytest.ini                    # 默认只收集维护工具测试
```

海外 PDF、参考书、原始 ZIP 与来源 HTML 位于 GitHub Releases，本地 `library/*/unpacked/` 从保存的 ZIP 重建。`.venv/`、`.cache/`、模型权重及运行输出由 Git 忽略；来源和依赖说明仍保留。详细规则见 [目录说明](docs/PROJECT_STRUCTURE.md)。

<a id="usage"></a>

## 两种使用方式

**本机学习与查资料：** 打开学习指南或 NJU 课程入口，使用个人笔记和完整材料；每次结束记录成果、卡点和下一步。现有 Bootcamp 笔记继续保留在移动后的同一 Notebook 中，独立练习放 `work/`。

**服务器做作业：** 按服务器教程以 `--filter=blob:none --no-checkout --depth=1` 克隆，再选择 `nju-a0`、`week1`、`core-a01` 等配置。讲义目录、个人课程 Notebook 与资料归档不自动下载。不要先普通克隆完整工作树再缩减目录。

<a id="run"></a>

## 本机环境与维护

```bash
source .venv/bin/activate
python -m jupyter lab
# NJU 本地模型与课程环境
bash scripts/start_nju.sh
```

新电脑按 [环境指南](docs/setup/README.md) 安装；完整资料恢复见 [存储教程](docs/GITHUB_STORAGE.md)。服务器按任务安装 `requirements/` 中的依赖或作业包内依赖。

```bash
python3 scripts/check_structure.py --strict-library
python3 -m unittest discover -s scripts/tests -v
.venv/bin/python scripts/verify_week1.py
.venv/bin/python scripts/verify_bootcamp.py
```

结构检查用于完整本机仓库；Notebook 验证只写 `outputs/verified/`，不覆盖原 Notebook。服务器直接验证所选作业。下载、归档和 Git 操作的完整命令见 [工具入口](scripts/README.md)。
