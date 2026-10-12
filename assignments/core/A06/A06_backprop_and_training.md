# A06：反向传播与训练诊断

来源类型：本仓库自制；参考 Berkeley CS182 HW1/讨论与 Stanford CS231n A1/A2。只选与当前单元有关的题，不要求整份完成。

## Part A：NumPy 网络

实现 Linear、ReLU、SoftmaxCrossEntropy 的 forward/backward，以及两层 MLP。不得在这一部分使用 autograd。每个参数做有限差分 gradient check，相对误差目标 < 1e-5。

必须写出 batch 维度和矩阵维度；用小数据过拟合到接近 100% 作为 sanity check。

## Part B：PyTorch 对照

在相同数据与初始化上搭建等价 PyTorch 网络，对照前向值、梯度和一步更新。随后比较：

- SGD、Momentum、Adam；
- 有/无 weight decay；
- 至少两种初始化；
- 有/无 BatchNorm 或 LayerNorm（二选一）。

每次只改变一个因素，至少 3 个随机种子。报告 train/val loss、accuracy、gradient norm、运行时间。

## Part C：诊断

人为制造并修复四个故障：学习率过大、标签错位、忘记 eval mode、训练/验证预处理不一致。对每个故障记录症状、证据、根因和最小修复。

提交 src/、tests/、a06.ipynb、ablation.csv、debugging_log.md。不能只交最终成功曲线。
