# 机器学习 → 深度学习 → LLM

一条以工程实践为主的学习路线：认识经典模型，读懂完整训练代码，改写关键模块，再完成小项目。本科核心与研究生扩展放在同一份课程设计里。

**学习入口：[三门课路线与模型地图](course/STUDY_GUIDE.md)** · [当前学习记录](course/TRACKER.md)

从 M1–M3 的训练与评估开始，再进入 D1–D3 的 PyTorch/MLP；之后学习 CNN、序列模型、Attention、Transformer，最后进入 LLM。数学按使用需要补充，具体串行与并行安排以路线为准。

## 现在能做的练习

| 要学什么 | 直接打开 |
|---|---|
| 回归与完整实验流程 | [学生成绩预测](assignments/bootcamp/week1/project/08_Student_performance_project.ipynb) |
| 分类、逻辑回归与决策树 | [分类带练](assignments/bootcamp/week2/classification_walkthrough.ipynb) |
| PyTorch 训练与 MLP | [训练带练](assignments/bootcamp/week3/02_pytorch_training_walkthrough.ipynb) |
| 按需补基础或实现核心模块 | [练习索引](assignments/README.md) |

现有示例可运行；课程设计中的其余单元会按需要补实验。公开高校 GitHub 仓库是后续片段的候选来源，未集成的代码不标成已完成。

## 怎么运行和保存

本机按 [环境教程](docs/setup/README.md) 启动 Notebook；服务器按 [只拉作业教程](docs/SERVER_GUIDE.md) 选择练习。`main` 保持课程模板；在对应学习分支将新成果放进 `work/`，完成后在该分支的学习记录里留下链接与解释。分支创建与本机/服务器同步步骤已合并在这两份教程中。

| 目录 | 用途 |
|---|---|
| `course/` | 唯一课程路线、当前记录和按需查阅的概念短章 |
| `assignments/` | 可运行示例、补充题目与公开作业模板 |
| `work/` | 学习时新建的个人实验与项目 |
| `docs/` | 本机环境和服务器使用教程 |
| `scripts/`、`config/` | 运行检查与服务器练习选择工具 |

课程文本、源码、小型示例数据及新成果用普通 Git 保存。模型权重、环境、下载缓存和运行输出按需获取并由 Git 忽略。整套讲义、参考书与旧资料 Release 已退出当前项目；历史提交仍可查阅旧文件。

维护命令见 [工具说明](scripts/README.md)。
