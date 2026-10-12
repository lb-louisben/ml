# 11：深度学习训练模式、CNN 与序列模型

目标：理解训练/验证差距；合理使用 normalization、dropout、weight decay、augmentation；掌握 CNN 和序列模型的主要 inductive bias；设计消融实验。

## 1. SGD、Momentum 与 Adam

SGD 更新直接跟随 mini-batch gradient；Momentum 对历史方向做指数累积，减少震荡；Adam 同时估计一阶与二阶矩，对不同参数调整步长。优化器是实验变量，必须与 learning rate、scheduler、weight decay 一起记录。

## 2. Regularization

- Weight decay/L2：限制权重规模。
- Dropout：训练时随机屏蔽激活；eval 时关闭。
- Data augmentation：注入任务保持不变的输入变换。
- Early stopping：validation 不再改善时停止。

每种方法都含假设。水平翻转适合许多自然图像，不适合左右方向决定标签的医学或交通任务。

## 3. Normalization

BatchNorm 使用 batch 统计，训练与 eval 行为不同；小 batch 统计可能不稳。LayerNorm 在单样本特征维上归一化，常用于序列与 Transformer。忘记 model.eval() 会使 dropout 和 BatchNorm 造成推理漂移。

## 4. CNN 的 inductive bias

卷积使用局部连接和权重共享：同一 pattern 可在不同位置被检测，参数远少于全连接。多层扩大 receptive field。padding、stride、kernel size 决定输出尺寸和信息损失。

CNN 并非天然完全平移不变；边界、stride、pooling 和数据分布都会影响。

## 5. RNN 与长依赖

RNN 顺序更新 hidden state，参数跨时间共享。反向传播跨很多步相乘 Jacobian，容易 gradient vanishing/exploding。LSTM/GRU 用门控改善信息保留，但并未消除所有长依赖和串行计算问题。

## 6. 消融实验

消融不是任意删模块，而是检验明确 claim。一次改变一个核心因素，保持数据、seed、训练预算、评价和 checkpoint 规则相同。至少 3 seeds，报告 mean/std 和成本；保留失败运行。

## 7. 表示学习与自监督

表示学习让模型把输入映射为对下游任务有用的特征。自监督从数据本身构造监督信号，例如遮住一部分预测、对比同一对象的不同视图、预测相邻片段。评价不能只看 pretext loss，还要用 linear probe、fine-tuning、retrieval 或下游数据效率验证表示。

对比学习需要定义正/负样本和 augmentation invariance；错误的正样本或增强会删除任务所需信息。避免把漂亮的二维投影当作表示质量的充分证据。

## 8. 生成模型概览

Autoregressive 模型把 joint probability 分解为条件概率连乘，生成质量强但逐 token/step 生成慢。VAE 使用 latent variable 与变分下界，提供结构化 latent space，但可能出现 posterior collapse。Diffusion 学习逐步去噪，从噪声反复采样，训练较稳定但推理步数较多。

比较生成模型至少考虑：sample quality、diversity、likelihood/代理指标、条件一致性、训练和采样成本、安全与数据记忆。单个视觉样例不是充分评价。

## Worked example

模型加 augmentation 后 validation 提升，但训练轮数也从 20 增至 100。不能直接把提升归因于 augmentation；需在相同预算或相同 early-stopping 规则下比较，并说明增强是否改变了有效数据难度。

## 常见错误

- 用 test 选择 epoch/checkpoint。
- 比较 optimizer 时 learning rate 明显偏向其中一个。
- 报告 best seed 而非预先定义的聚合。
- augmentation 改变了标签语义。
- train/eval mode 不一致。

## 自测

1. BatchNorm 与 LayerNorm 的统计维度有何差别？
2. dropout 为什么在 eval 时关闭？
3. CNN 权重共享带来什么假设？
4. RNN 为什么会 gradient vanishing？
5. 一个可信消融要固定哪些条件？
6. 自监督的 pretext loss 更低为何不保证下游更好？
7. VAE、autoregressive、diffusion 的生成过程各有什么主要特点？

答案要点：跨 batch 与单样本特征；推理用完整期望网络；局部 pattern 可跨位置复用；时间链 Jacobian 连乘；数据/split、预算、seed、评价和选择规则；代理目标与下游需求可不一致；逐步条件生成、latent 变分生成、迭代去噪。

当前练习与掌握标准统一见 [课程路线](../STUDY_GUIDE.md)。
