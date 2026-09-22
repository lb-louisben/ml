# P2：深度学习复现与消融

来源类型：本仓库自制；参考 CS182/CS231n 的书面+编程作业与研究项目风格。周期 3～4 周。

## 范围

选择一篇有公开代码或足够实现细节、能在现有硬件合理运行的论文/方法。目标不是完全复制大规模 SOTA，而是复现一个核心 claim、图或表，并解释偏差。

可选题：小型 CNN 的 augmentation/normalization；序列模型与 Transformer 的长依赖；自监督表示的小数据迁移；轻量图像分类；小模型文本分类。禁止把“直接运行作者 checkpoint”当作完整复现。

## 四周节奏

- Week 1：一页 proposal、论文 claim、数据/代码许可、计算预算、baseline、成功标准。
- Week 2：baseline 与 sanity checks；先过拟合小 batch，再完整训练。
- Week 3：复现主结果；至少 3 seeds，保留失败运行。
- Week 4：至少两个消融、错误分析、报告与答辩。

## 必须提交的表

原论文报告值（若可比）、你的 baseline、你的 reproduction、ablation 1、ablation 2。每行有 mean/std、seeds、数据版本、参数量、训练时间与硬件。不可比时明确写 N/A，不强行制造一致性。

## 复现差距排查

按顺序检查：数据版本与 split；预处理/augmentation；metric 细节；初始化/seed；optimizer/schedule；batch size 与 gradient accumulation；train/eval mode；checkpoint 选择；软件版本与数值精度。

## 交付

proposal.md、environment、configs、src、tests、runs manifest、results.csv、6 页以内 report、5 分钟 demo。报告必须区分“成功复现”“方向一致但数值有差距”“未复现”，负结果同样可以高分，只要实验严谨。
