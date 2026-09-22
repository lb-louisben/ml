# P3：最终 Capstone

来源类型：本仓库自制；里程碑借鉴 Stanford CS229/CS224N 的 proposal、milestone、final report、poster/demo 结构。周期至少 4 周。

## 可选方向

1. 传统 ML：高质量表格/时间序列问题，重点是严谨评价与可解释性。
2. 视觉：复现后迁移到新数据或测试一个明确的 augmentation/representation 假设。
3. NLP/LLM：小模型 fine-tuning、语义搜索、RAG 或系统化评价。
4. RL：只有完成 Phase 3 后选择，优先小环境和稳定 baseline。

## Week 50：Proposal（10%）

最多 2 页：问题和用户；相关工作 3～5 项；数据、许可和伦理；baseline；一个主要假设；指标与统计协议；计算预算；风险与 fallback。必须定义“不成功也能得到什么结论”。

## Week 51：Baseline（20%）

数据 pipeline 和最简单模型从干净环境可运行；冻结 test；登记 seed/config；生成第一张结果表和第一版错误 taxonomy。没有 baseline 不进入复杂方法。

## Week 52：Milestone（20%）

提交 3 页进度：当前结果、与计划差异、一个关键失败、下一周最小可行范围。至少完成一个有假设的改进，并开始消融。此时允许缩小目标，不允许隐藏负结果。

## Week 53：Final（50%）

- 6～8 页报告：abstract、problem、related work、data、method、experiments、results、error/ablation、limitations、ethics、references。
- README：环境、数据获取、训练、评价、预期输出、硬件与耗时。
- results.csv/JSON 与运行 manifest；图表必须可从保存结果重新生成。
- 5 分钟演示或 poster；10 分钟口试。

## 最低研究质量

- 明确 baseline 和 falsifiable hypothesis。
- 至少 3 seeds 或合理的不确定性分析；昂贵实验需解释例外。
- 至少两个消融或一个消融 + 一个强错误切片。
- 测试集只在方案冻结后使用；若污染，必须重新建立 holdout。
- 所有外部数据、代码、模型、论文和 AI 协助有引用。
- 结果既报告效果，也报告成本、延迟或资源。

## 答辩问题

1. 你的结果最可能被哪个 hidden assumption 推翻？
2. 为什么选择这个指标？换一个利益相关者会改变吗？
3. 哪个实验真正支持主要 claim，哪个只是相关现象？
4. 如果再多一周，只做哪个实验？为什么？
5. 你如何证明代码没有泄漏、选择偏差或评估错误？

项目按 [通用 rubric](../ASSESSMENT.md#project-rubric) 评分，另要求 report、demo 和口试各自不低于 60%。
