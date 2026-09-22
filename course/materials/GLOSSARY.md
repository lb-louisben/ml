# 术语表

## A–D

- Ablation：删除或改变一个组件以检验其贡献的对照实验。
- Agent：由模型根据中间观察动态选择行动/工具的系统。
- Baseline：最简单、可复现的比较起点。
- Batch：一次用于计算梯度的一组样本。
- Bias：估计或模型的系统性偏离；在 bias–variance 中指模型假设造成的误差。
- Calibration：预测概率与实际频率的一致程度。
- Confounder：同时影响特征/处理与结果，造成非因果关联的变量。
- Cross-validation：轮换训练/验证子集估计选择表现的方法。
- Data leakage：训练或选择过程使用了部署时不可得或测试信息。
- Distribution shift：训练与部署的数据生成分布不同。

## E–M

- Embedding：把离散对象映射到可学习稠密向量。
- Epoch：模型完整遍历训练集一次。
- Feature：模型输入变量。
- Fine-tuning：在预训练模型参数基础上继续用任务数据训练。
- Generalization：模型在未见、同目标分布数据上的表现能力。
- Gradient：函数对各参数的局部变化率向量。
- Hyperparameter：训练外选择的配置，如树深、C、learning rate。
- Label/target：要预测的结果。
- Loss：单个或一批预测的优化目标。
- MLE/MAP：最大似然估计 / 最大后验估计。

## N–R

- Overfitting：学习了训练集特有噪声，train 好而新数据差。
- Parameter：由训练数据学得的模型量，如权重。
- PEFT：只训练少量参数的参数高效微调方法族。
- Pipeline：把 fit/transform/model 顺序与数据边界封装起来。
- Precision：预测为正的样本中真实为正的比例。
- Pretraining：在大规模通用数据上训练基础表示/生成能力。
- RAG：先从外部语料检索证据，再让生成模型基于证据回答。
- Recall：真实正类中被模型找出的比例。
- Regularization：限制有效复杂度以改善泛化的方法。

## S–Z

- Seed：控制伪随机过程以帮助复现的初始值；一个 seed 不是不确定性分析。
- Self-attention：序列中每个位置按内容对其他位置加权聚合。
- Slice：按人群、时间、质量等条件划分的评价子集。
- Split：train/validation/test 等互斥数据分区。
- Test set：方案完全冻结后用于最终估计的独立数据。
- Token：tokenizer 切分后的离散文本单元，不一定等于词。
- Transformer：以 attention、feed-forward、residual、normalization 等构成的序列架构。
- Underfitting：模型/特征/优化不足，train 与 validation 都差。
- Validation set：用于模型、超参数和阈值选择的数据。
- Variance：估计对训练样本变化的敏感程度。

## 容易混淆的对

- 参数 vs 超参数：训练学得 vs 训练外选择。
- validation vs test：反复选择 vs 冻结后一次评价。
- ranking vs calibration：排序对不对 vs 概率准不准。
- correlation vs causation：一起变化 vs 干预会改变结果。
- backprop vs optimizer：计算梯度 vs 使用梯度更新。
- RAG vs fine-tuning：外部证据注入 vs 参数更新。
- workflow vs agent：预定义路径 vs 动态选择路径。

返回：[材料导航](README.md) · [公式卡](REFERENCE_CARD.md)
