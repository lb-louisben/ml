> 历史方案，已停止执行。本文中的周数、必做项和晋级安排仅供追溯；当前顺序以 [学习指南](../../course/STUDY_GUIDE.md) 为准。

# 长期学习时间表

这不是把名校课表简单堆在一起，而是一条适合自学者的先修链：先建立可工作的能力，再补数学与理论，之后进入深度学习、Transformer 和独立研究。标准版为 53 周、每周 8～12 小时；已经有较强数学或编程基础时，可按“加速规则”压缩到约 36 周。

> 本仓库与 Stanford、UC Berkeley、MIT 无隶属关系。“官方”只表示链接指向相应学校公开页面；“自制”表示本仓库根据学习目标重新设计。来源、公开程度和采用方式见 [SOURCES.md](../../course/SOURCES.md)。

## 怎么执行

每周完成阅读、纸笔推导、编程和复盘。具体原版讲义、slides、作业顺序以 [课程学习指南](../../course/STUDY_GUIDE.md) 为准，原件在 [本地资料库](../../library/README.md)。下面保留长期时间规划；表中的中文短章用于预习与复习，不能替代整门课程。

晋级不只看“看完视频”：阶段测试至少 70%，作业至少 75%，项目 rubric 至少 70%，并且能够在不看代码的情况下解释数据划分、指标、主要假设和失败案例。评分规则见 [ASSESSMENT.md](../../course/ASSESSMENT.md)，勾选进度见 [TRACKER.md](../../course/TRACKER.md)。

## 一眼看懂路线

| Phase | 周数 | 大学课程定位 | 必做考核 |
|---|---:|---|---|
| 0 | 1～3 | 入门桥梁 | Week 1 项目、A04 精简版、T0 |
| 1 | 4～9 | 本科数学先修 | A01、T0 ≥ 70 |
| 2 | 10～21 | Berkeley Data 100 / ISLP / CS189 入门段 | A02～A04、T1、P1 |
| 3 | 22～33 | Stanford CS229 + Berkeley CS189 | A05、T2、P2 proposal |
| 4 | 34～43 | Berkeley CS182 + Stanford CS231n | A06、P2 |
| 5 | 44～49 | Stanford CS224N | A07、A08、T3 |
| 6 | 50～53 | 研究式 Capstone | proposal、milestone、report、demo |

<a id="phase-0"></a>

## Phase 0（第 1～3 周）：三周系统入门

目标是形成最小闭环，而不是假装三周学完 ML。

- 第 1 周：[Python、数据分析与线性回归](../../assignments/bootcamp/week1/README.md)。沿用现有学生成绩 Notebook。
- 第 2 周：[分类、树模型与可靠评估](../../assignments/bootcamp/week2/README.md)。主作业为 [A04 分类与阈值](../../assignments/core/A04/A04_classification_evaluation.md)。
- 第 3 周：[神经网络、现代 AI 与综合项目](../../assignments/bootcamp/week3/README.md)。结束时做 [数学诊断 T0](../../course/tests/T0_math_diagnostic.md)。
- 阶段出口：能从原始表格到 Pipeline、验证集选择、一次性测试集评价，并写出模型的局限。

<a id="phase-1"></a>

## Phase 1（第 4～9 周）：数学桥梁

详细材料采用 [MIT 原版课程](../../library/mit-1806sc-f11/README.md) 与 [CS229 数学复习](../../library/stanford-cs229-see/README.md)。表中中文导读用于预习；具体读写顺序见 [学习指南](../../course/STUDY_GUIDE.md)。

| 周 | 主题 | 学习材料 | 输出 |
|---|---|---|---|
| 4 | 向量、矩阵、线性方程组、秩 | [01 线性代数](../../course/materials/01_linear_algebra.md) §1～2 | MIT 对应 Problems + NumPy 验证 |
| 5 | 正交、投影、最小二乘 | [01 线性代数](../../course/materials/01_linear_algebra.md) §3 | [A01 Part A](../../assignments/core/A01/A01_math_and_optimization.md) |
| 6 | 特征值、正定矩阵、SVD、PCA | [01 线性代数](../../course/materials/01_linear_algebra.md) §4～5 | 手算 2×2 SVD + 图像压缩实验 |
| 7 | 条件概率、Bayes、期望、方差、常见分布 | [02 概率与统计](../../course/materials/02_probability_statistics.md) | CS229 概率复习 + A01 Part B |
| 8 | 多元微积分、矩阵求导、梯度下降 | [03 微积分与优化](../../course/materials/03_calculus_optimization.md) | [A01 Part C](../../assignments/core/A01/A01_math_and_optimization.md) |
| 9 | 综合复习 | 错题本与重做 | 闭卷 [T0](../../course/tests/T0_math_diagnostic.md) |

若 T0 低于 70%，只补对应模块；不要把整个阶段重学一遍。

<a id="phase-2"></a>

## Phase 2（第 10～21 周）：本科核心

主课采用 [Data 100 本地材料](../../library/berkeley-data100-sp25/README.md)，之后接 [CS189](../../library/berkeley-cs189-sp25/README.md) 的建模主题。下面短章辅助预习和复盘。

| 周 | 主题 | 主材料 | 作业/项目 |
|---|---|---|---|
| 10 | 数据生命周期、Pandas、可复现 EDA | [04 数据与实验设计](../../course/materials/04_data_and_experiment_design.md) | [A02](../../assignments/core/A02/A02_data_audit.md) |
| 11 | 清洗、缺失、正则、可视化 | [04 数据与实验设计](../../course/materials/04_data_and_experiment_design.md) | A02 提交 |
| 12 | 抽样、估计、偏差与方差 | [02 概率与统计](../../course/materials/02_probability_statistics.md) | 统计模拟 Notebook |
| 13 | 线性回归与几何解释 | [05 线性模型](../../course/materials/05_linear_models.md) | [A03](../../assignments/core/A03/A03_regression_from_scratch.md) |
| 14 | 特征工程、正则化、交叉验证 | [05 线性模型](../../course/materials/05_linear_models.md) | A03 提交 |
| 15 | 逻辑回归、生成式分类 | [05 线性模型](../../course/materials/05_linear_models.md) · [08 概率模型](../../course/materials/08_probabilistic_and_kernel_ml.md) | [A04](../../assignments/core/A04/A04_classification_evaluation.md) |
| 16 | kNN、决策树、随机森林、boosting | [07 树与集成](../../course/materials/07_trees_and_ensembles.md) | A04 提交 |
| 17 | 指标、阈值、校准、类别不平衡 | [06 分类与评价](../../course/materials/06_classification_and_metrics.md) | 错误切片报告 |
| 18 | SVM 与核方法 | [08 概率模型与核](../../course/materials/08_probabilistic_and_kernel_ml.md) | 核技巧推导练习 |
| 19 | 聚类、PCA、无监督学习 | [09 无监督与泛化](../../course/materials/09_unsupervised_and_generalization.md) | 无监督小实验 |
| 20 | 复习与闭卷 | 重做错题 | [T1](../../course/tests/T1_undergraduate_midterm.md) |
| 21 | 端到端项目 | 自选公开表格数据 | [P1](../../course/projects/P1_tabular_benchmark.md) |

出口标准：给定陌生表格数据，能定义目标、建立基准、预防泄漏、比较模型、解释不确定性和错误样本。

<a id="phase-3"></a>

## Phase 3（第 22～33 周）：研究生机器学习核心

主课采用 [CS229 本地完整档案](../../library/stanford-cs229-see/README.md)，用 [CS189 原版作业与考试](../../library/berkeley-cs189-sp25/README.md) 补强薄弱部分；中文短章用于预习。

| 周 | 主题 | 必须会做 | 对应考核 |
|---|---|---|---|
| 22 | MLE、MAP、指数族、GLM | [02 概率](../../course/materials/02_probability_statistics.md) · [05 线性模型](../../course/materials/05_linear_models.md) | 推导题 |
| 23 | GDA、Naive Bayes | [08 概率模型与核](../../course/materials/08_probabilistic_and_kernel_ml.md) | [A05 Part A](../../assignments/core/A05/A05_probabilistic_and_kernel_ml.md) |
| 24 | margin、SVM、kernel | [08 概率模型与核](../../course/materials/08_probabilistic_and_kernel_ml.md) | A05 Part B |
| 25 | bias–variance、正则化、学习曲线 | [05 线性模型](../../course/materials/05_linear_models.md) · [09 泛化](../../course/materials/09_unsupervised_and_generalization.md) | 实验备忘录 |
| 26 | 决策树、boosting | [07 树与集成](../../course/materials/07_trees_and_ensembles.md) | 模型比较 |
| 27 | k-means、GMM、EM | [09 无监督与泛化](../../course/materials/09_unsupervised_and_generalization.md) | 手推 + 实现 |
| 28 | PCA 与表示学习 | [01 线性代数](../../course/materials/01_linear_algebra.md) · [09 无监督](../../course/materials/09_unsupervised_and_generalization.md) | 小型复现 |
| 29 | 学习理论、generalization | [09 无监督与泛化](../../course/materials/09_unsupervised_and_generalization.md) | 书面题 |
| 30 | MDP、value/policy iteration | [14 RL 与责任](../../course/materials/14_rl_responsibility_and_research.md) | 手算小型 MDP |
| 31 | 公平、隐私、可解释性 | [14 RL 与责任](../../course/materials/14_rl_responsibility_and_research.md) | audit memo |
| 32 | 闭卷复习 | 不查资料完成推导 | [T2](../../course/tests/T2_graduate_ml_final.md) |
| 33 | 研究准备 | 选论文、建 baseline、冻结协议 | [P2 proposal](../../course/projects/P2_deep_learning_reproduction.md) |

官方题的正确用法：先限时独立作答，再看官方解答。CS189 历年考试适合计时训练；Stanford SEE 的旧版 CS229 提供完整 problem sets 与 solutions，适合作为补充，不当作当前课程原题。

<a id="phase-4"></a>

## Phase 4（第 34～43 周）：深度学习核心

主课采用 [CS182](../../library/berkeley-cs182-sp21/README.md) 和 [CS231n](../../library/stanford-cs231n-2025/README.md) 原版讲义、课件与作业，中文短章用于预习。

| 周 | 主题 | 实践 |
|---|---|---|
| 34 | 计算图、反向传播、梯度检查 | [10 神经网络](../../course/materials/10_neural_networks_and_backprop.md) · [A06](../../assignments/core/A06/A06_backprop_and_training.md) |
| 35 | 优化器、初始化、归一化 | [10 神经网络](../../course/materials/10_neural_networks_and_backprop.md) · [11 训练模式](../../course/materials/11_deep_learning_patterns.md) |
| 36 | MLP 与训练诊断 | [10 神经网络](../../course/materials/10_neural_networks_and_backprop.md)；完成 A06 |
| 37 | CNN、感受野、卷积输出尺寸 | [11 深度学习训练模式](../../course/materials/11_deep_learning_patterns.md) |
| 38 | regularization、augmentation、dropout | [11 深度学习训练模式](../../course/materials/11_deep_learning_patterns.md)；消融表 |
| 39 | sequence model、RNN/LSTM | [11 深度学习训练模式](../../course/materials/11_deep_learning_patterns.md)；长依赖失败实验 |
| 40 | attention 与 Transformer 预备 | [12 Embedding 与 Transformer](../../course/materials/12_embeddings_and_transformers.md) |
| 41 | 表示学习、自监督 | [11 训练模式](../../course/materials/11_deep_learning_patterns.md) §7；小实验 |
| 42 | 生成模型概览 | [11 训练模式](../../course/materials/11_deep_learning_patterns.md) §8；VAE / diffusion 选一复现 |
| 43 | 深度学习复现项目 | [P2](../../course/projects/P2_deep_learning_reproduction.md) |

CS231n 官方 2025 三个 assignment 从 kNN/Softmax/全连接网络，推进到 CNN、RNN，再到 Transformer、自监督、diffusion、CLIP/DINO。建议只选与你项目相关的部分，不必机械全做。

<a id="phase-5"></a>

## Phase 5（第 44～49 周）：NLP、Transformer 与 LLM

主课采用 [CS224N Winter 2025 本地材料](../../library/stanford-cs224n-w25/README.md)，按 A1～A4 顺序推进。中文短章用于预习，项目材料用于 Capstone。

| 周 | 主题 | 输出 |
|---|---|---|
| 44 | tokenization、word2vec、embedding | [12 Embedding 与 Transformer](../../course/materials/12_embeddings_and_transformers.md) |
| 45 | RNN、seq2seq、attention | [11 训练模式](../../course/materials/11_deep_learning_patterns.md) · [12 Transformer](../../course/materials/12_embeddings_and_transformers.md) |
| 46 | Transformer 从公式到实现 | [12 Transformer](../../course/materials/12_embeddings_and_transformers.md) · [A07](../../assignments/core/A07/A07_transformer_from_scratch.md) |
| 47 | pretraining、SFT、PEFT、DPO 概念 | [13 LLM 系统](../../course/materials/13_llm_systems.md) |
| 48 | RAG、agent、评估与安全 | [13 LLM 系统](../../course/materials/13_llm_systems.md) · [A08](../../assignments/core/A08/A08_rag_evaluation.md) |
| 49 | 综合口试与方向选择 | [T3](../../course/tests/T3_dl_llm_oral.md) |

出口标准：能解释 embedding、self-attention、预训练/后训练的差别；能把 RAG 拆成检索、生成和评估，并用证据说明系统是否真的改进。

<a id="phase-6"></a>

## Phase 6（第 50～53 周）：Capstone

按照 CS229/CS224N 常见的 proposal → milestone → report → poster/demo 节奏执行，具体要求见 [Capstone](../../course/projects/CAPSTONE.md)。

- 第 50 周：问题定义、相关工作、数据许可、baseline、评价协议。
- 第 51 周：可运行 baseline 与第一轮错误分析。
- 第 52 周：一个有明确假设的改进 + 消融实验。
- 第 53 周：6～8 页报告、README、环境文件、结果表、5 分钟演示、10 分钟答辩。

## 方向分叉

完成 Phase 3 后再选，不要在数学和评估基础未稳时过早分流。

- 传统 ML / 数据科学：继续 ISLP 高级章节、因果推断、时间序列，Capstone 做严谨的表格预测或估计问题。
- 计算机视觉：完整完成 CS231n A1～A3，Capstone 做复现 + 新数据集迁移。
- NLP / LLM 应用：完成 CS224N A1～A4，Capstone 做检索、微调或评估；优先小模型和可重复实验。
- 强化学习：先通过 Phase 3，再进入 [Berkeley CS285](https://rail.eecs.berkeley.edu/deeprlcourse/)；它明确要求 CS189 或同等基础，不建议提前。
- 研究准备：每两周精读一篇论文，提交一页 review，复现一个表格或图，所有负结果也保留。

## 36 周加速规则

不是删掉考核，而是压缩输入：Phase 1 用 4 周、Phase 2 用 8 周、Phase 3 用 8 周、Phase 4 用 7 周、Phase 5 用 4 周、Capstone 用 5 周。满足以下条件才加速：T0 首次 ≥ 85%；能独立写 sklearn Pipeline；每周稳定投入至少 14 小时。任何阶段测试低于 70%，恢复标准节奏。

## 下一步

当前最合理的入口仍是 [week1](../../assignments/bootcamp/week1/README.md)。第一周项目通过后进入 [week2](../../assignments/bootcamp/week2/README.md)，不要同时开十门课。
