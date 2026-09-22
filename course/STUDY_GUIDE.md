# 学习指南

[工作台](../README.md) · [进度表](TRACKER.md) · [材料目录](README.md)

**本页安排整体阶段；前期的逐次任务统一写在各周 README 中。先完成当前任务，再打开下一阶段。** Week 1/2/3 保留为文件位置和内容编号，不代表必须在三个自然周内完成。长期路线按能力推进，先不承诺固定总周数。

## 当前怎样接续

先完成学生成绩回归项目。前期已拆成 [27 次学习](bootcamp/README.md)，每次 90～120 分钟；这是内容单元，可以跨天完成。

原指南从 Day 3 接续，但进度表尚无完成证据。先用 [W1-01/02](bootcamp/week1/README.md#w1-01) 的独立练习确认 Python / NumPy 基础，再按下面三步推进：

| 顺序 | 具体安排 | 本次成果 |
|---|---|---|
| 建议接续点 | [W1-03：读懂真实表](bootcamp/week1/README.md#w1-03) | 数据说明、条件筛选、按学校分组统计 |
| 下一次 | [W1-04：有依据地清洗](bootcamp/week1/README.md#w1-04) | 教学副本清洗规则、质量报告、导出检查 |
| 再下一次 | [W1-05：用图回答问题](bootcamp/week1/README.md#w1-05) | 四张训练集图表及证据、局限 |

已有成果满足某个单元的完成标准时，记录证据后跳过。随后继续 W1-06～10，完成回归项目再进入 W2-01。每天只需打开 [进度表](TRACKER.md) 和当前周的任务说明。

## 全程只有这一条顺序

| 阶段 | 要解决的问题 | 默认主材料 | 阶段成果 |
|---|---|---|---|
| 0 入门实践 | 能否独立完成一个可信的小实验？ | 本地入门任务 | 回归 → 分类 → 小网络，依次完成 |
| 1 数学基础 | 能否解释模型里的矩阵、概率与梯度？ | MIT 线代；概率/微积分用 CS229 复习补齐 | 推导与数值验证、T0 |
| 2 数据科学 | 面对陌生数据，能否独立设计实验？ | Data 100 | P1 表格项目、T1 |
| 3 ML 理论 | 能否从目标函数解释算法？ | CS229 SEE | 原课对应题、T2 |
| 4 深度学习 | 能否实现、诊断并复现网络？ | CS182 | 网络练习、P2 |
| 5 NLP / LLM | 能否理解 Attention 并评价文本系统？ | CS224N | 词向量到 Transformer 的练习、T3 |
| 6 综合项目 | 能否独立验证一个改进假设？ | 已学领域材料 | Capstone |

这些是学习阶段，不代表学历层级。CV、RL 等专题在共同基础完成后按项目需要扩展，不同时开课。

<a id="phase-0"></a>

## 阶段 0：先做出三个小实验

严格顺序：[回归](bootcamp/week1/README.md) → [分类](bootcamp/week2/README.md) → [小网络](bootcamp/week3/README.md)。每次只保留一个正在做的项目。

第一次实现分类与网络，使用 [三本带练教程](bootcamp/README.md)：必要解释、材料链接、中文注释示例和独立变式已按单元整合。先跟做，再自己重建；不要求面对任务清单直接从空白实现。

- 回归：按上方当前任务表完成，验收用第一阶段已有评分表。
- 分类：Dummy + 逻辑回归 + 决策树，完成合法划分、验证集选阈值、最终评价与错误分析；具体任务见分类页面。
- 小网络：先补 shape、链式法则与梯度下降，再做 NumPy 两层 MLP 和一个 PyTorch 对照；具体任务见小网络页面。

入门只做这些页面列出的基础范围。完整 A04、A06、A07、A08，以及学校整套作业，留给后续阶段。T0 在进入数学阶段时用于诊断，首次分数不阻塞入门验收；T3 留到阶段 5。

<a id="phase-1"></a>

## 阶段 1：补数学，并解释入门实验

主材料：[MIT 18.06SC](../library/mit-1806sc-f11/README.md)，用 [CS229 复习材料](../library/stanford-cs229-see/README.md) 补概率与微积分。

学习顺序：矩阵与子空间 → 投影与最小二乘 → 特征值/SVD → 条件概率与期望 → 梯度与链式法则。对应 [中文导读 01～03](materials/README.md)，原件见 [数学文件索引](READING_LIST.md#math)。

每个主题做配套练习并用 NumPy 验证；[A01](assignments/A01_math_and_optimization.md) 可替换同主题练习。入口做 T0 找弱项，出口重测 [T0](tests/T0_math_diagnostic.md) ≥70；保留最小二乘推导、Bayes 计算与梯度检查。已通过的主题不用整章重做。

<a id="phase-2"></a>

## 阶段 2：把入门方法迁移到陌生数据

主材料：[Data 100](../library/berkeley-data100-sp25/README.md)。顺序为数据粒度与清洗 → EDA → 特征工程 → 回归/分类 → 交叉验证与错误分析。

只选上述主题对应的原课练习；已掌握的 Pandas 操作用独立练习确认后跳过。[A02～A04](assignments/README.md) 是对应主题的替代练习，不额外叠加。

阶段成果是 [P1](projects/P1_tabular_benchmark.md) 与 [T1](tests/T1_undergraduate_midterm.md) ≥70。P1 使用新的数据或问题验证迁移能力；可以复用入门项目的代码结构，需补齐 P1 的完整要求。

<a id="phase-3"></a>

## 阶段 3：系统学习机器学习理论

主材料：[CS229 SEE](../library/stanford-cs229-see/README.md)。这是旧版公开档案，按其中 Schedule 和讲义标题推进：监督学习 → 概率模型与核方法 → 泛化与模型选择 → 无监督学习 → 课程其余主题。

每学完一组讲义，做原 Problem Sets 中对应题，记录推导、实现与订正；MATLAB/Octave 题可以用 Python 完成并注明移植。[A03/A05](assignments/README.md) 可替换同主题实现练习。

[CS189](../library/berkeley-cs189-sp25/README.md) 仅用于卡点补充或考题自测，不单列为第二门必修。阶段验收为原课对应题的独立尝试与订正、[T2](tests/T2_graduate_ml_final.md) ≥70。

<a id="phase-4"></a>

## 阶段 4：深度学习与复现

主材料：[CS182](../library/berkeley-cs182-sp21/README.md)。顺序为反传 → 优化与初始化 → 正则化与训练诊断 → CNN → 序列与 Attention。生成模型按项目需要选学。

完成相关原课网络练习，或用 [A06](assignments/A06_backprop_and_training.md) 替代同主题部分；在入门已有代码上补齐梯度对照、多随机种子和故障诊断。[CS231n](../library/stanford-cs231n-2025/README.md) 用于视觉专题或缺失练习的补充，不要求整套叠加。其 2025 页面归档的作业 ZIP 存在跨年份情况，以包内说明为准。

阶段成果为 [P2](projects/P2_deep_learning_reproduction.md)：先选范围可控的论文与 baseline，再做至少两项消融、错误分析和复现报告。进入本阶段后才写 P2 proposal。

<a id="phase-5"></a>

## 阶段 5：NLP、Transformer 与 LLM

主材料：[CS224N Winter 2025](../library/stanford-cs224n-w25/README.md)。按词向量 → 神经网络 → RNN/Attention → Transformer → 预训练与适配 → 评价的顺序学习。

原课 A1～A4 随对应主题推进；[A07](assignments/A07_transformer_from_scratch.md) 可替换其中 self-attention 实现练习，但不能算作整份学校作业完成。先运行小样本和包内检查，再决定完整训练规模。

选做 RAG 应用时再完成 [A08](assignments/A08_rag_evaluation.md)；Agent 作为应用扩展，不单独设入门门槛。阶段验收为所学核心练习与 [T3](tests/T3_dl_llm_oral.md) ≥70。

<a id="phase-6"></a>

## 阶段 6：只选一个综合项目

按 [Capstone](projects/CAPSTONE.md) 执行：问题与协议 → baseline → 一个改进假设 → 消融与错误分析 → 报告和演示。范围以已有数据、时间与算力为准。项目满足评分标准后完成本路线。

## 每次怎样执行

先花 10～15 分钟读当前任务需要的中文导读，再读一小段主课材料；余下时间用于独立练习。材料较难时可分两次完成，不要求一次学习同时读完讲义、做完作业和项目。

结束时只记录三件事：成果文件、一个卡点、下一步。每完成一个阶段，再细化下一阶段的任务与时间。没有实际用时记录前，不据此排一年日历。

[评分规则](ASSESSMENT.md) 用于已选的完整作业、测试和项目；入门部分练习按对应页面验收。相同成果可以复用并补缺项，不重复提交，也不把选做项计为欠账。学校原件放在 `library/`，自己的后续代码放在 `work/`；各课程依赖按包内 README 单独准备。
