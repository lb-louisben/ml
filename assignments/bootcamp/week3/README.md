# 入门 3：把一个小网络训练明白

[前期总览](../README.md) · [整体指南](../../../course/STUDY_GUIDE.md#phase-0) · [上一部分](../week2/README.md)

**10 次学习，每次 90～120 分钟；一个小网络项目。** 前置条件是能完成分类与可靠评价。先补必要的矩阵和梯度，再写 NumPy 网络，最后用 PyTorch 对照。

第一次先在原目录打开下面的带练教程，按单元顺序读解释、运行小例子、修改参数；自己的实验放在 `work/intro-network/`，用 `network.ipynb` 累积独立推导和结果。一次写不完可以跨天，不用赶在一个自然周内结束。

## 先打开什么

| 单元 | 跟着实现 | 辅助材料 |
|---|---|---|
| W3-01～07 | [01 NumPy 网络：手算、前向、反传与梯度检查](01_numpy_network_walkthrough.ipynb) | [带注释的 NumPy 实现](numpy_mlp.py) |
| W3-08～10 | [02 PyTorch：逐项对照、训练、保存与评价](02_pytorch_training_walkthrough.ipynb) | [PyTorch 运行配置](../../../docs/setup/DEEP_LEARNING.md) |

两份 Notebook 都能从新内核独立运行，不依赖上一本的执行状态。教材固定导入本目录的 `numpy_mlp.py`。自己的实现写在 `work/` 中；若复制参考 Notebook，先修改开头的导入路径和 `OUT`，并打印导入模块的 `__file__` 确认正在使用自己的代码。每节包含必要概念、注释示例、应观察的性质、练习与提示。演示运行成功和自己的练习完成分别记录。

## 单元导航

[W3-01 shape](#w3-01) · [W3-02 梯度](#w3-02) · [W3-03 前向](#w3-03) · [W3-04 损失](#w3-04) · [W3-05 反传](#w3-05) · [W3-06 检查](#w3-06) · [W3-07 小样本](#w3-07) · [W3-08 框架](#w3-08) · [W3-09 训练](#w3-09) · [W3-10 整理](#w3-10)

<a id="w3-01"></a>

## W3-01｜把 shape 和一次前向算清楚

**材料：** [线代 §1](../../../course/materials/01_linear_algebra.md)、[神经网络 §1](../../../course/materials/10_neural_networks_and_backprop.md)。

**独立练习：** 设 `X:2×3、W:3×4、b:4`，先预测 `XW+b` 的 shape；自己取小整数，手算其中一个输出，再用 NumPy 核对。加入 ReLU，列出哪些元素变为 0；写出两层 `3→4→2` 网络每个中间量的 shape。

**完成标准：** 解释 batch、输入维数、隐藏维数、类别数；说明广播在哪一维发生；理解没有激活的多层仿射变换仍可合并。保存 shape 表和手算例子。

<a id="w3-02"></a>

## W3-02｜梯度与链式法则

**材料：** [微积分 §1～3、§5](../../../course/materials/03_calculus_optimization.md)。

**独立练习：** 对 `L(w)=(2w-3)²` 推导梯度，从 `w=0` 出发手算学习率 0.1 的一步更新；写 20 步循环，并比较学习率 0.01、0.1、1 的轨迹。再把它拆成 `z=2w、L=(z-3)²`，解释两段导数怎样相乘。

**完成标准：** 能说明为什么减去梯度、梯度和损失不是同一量、过大学习率怎样导致失败。不能独立完成链式法则时停在这里补练，再写网络。

<a id="w3-03"></a>

## W3-03｜NumPy 两层网络的前向传播

**材料：** [神经网络 §1、§4](../../../course/materials/10_neural_networks_and_backprop.md)。

**独立练习：** 实现 `Linear → ReLU → Linear`，输入用小型随机矩阵，输出 logits；保存反传所需的 X 和激活前值。使用固定随机种子、小随机权重与零 bias，写出参数量和各中间量的 shape。

**完成标准：** 相同参数和输入产生相同输出；改变 batch 大小只改变输出第一维；能解释为何隐藏层权重不全初始化为 0。此时不加 softmax、不训练真实数据。

<a id="w3-04"></a>

## W3-04｜稳定 softmax 与交叉熵

**材料：** [神经网络 §2 与例题](../../../course/materials/10_neural_networks_and_backprop.md)。

**独立练习：** 对每行 logits 先减最大值，再算 softmax；用稳定的 log-sum-exp 计算交叉熵，batch 损失取平均。检查普通 logits、全相同 logits、整体加 1000 的 logits；比较“正确且自信”和“错误且自信”的损失。

**完成标准：** 每行概率和接近 1；整体加常数后概率与损失不变，无 NaN/Inf；K 类均匀概率时损失约为 `log(K)`。保存数值检查；不靠任意截断概率掩盖溢出。

<a id="w3-05"></a>

## W3-05｜从损失反传到每个参数

**材料：** [神经网络 §3](../../../course/materials/10_neural_networks_and_backprop.md)、[A06 Part A](../../core/A06/A06_backprop_and_training.md) 作为实现要求参考。

**独立练习：** 先在纸上画 logits → loss 的计算链，再从末端依次写 `dlogits`、第二层 `dW/db`、ReLU mask、第一层 `dW/db`；平均交叉熵对应 `(probabilities - one_hot)/batch_size`。每写一个梯度就标 shape，再实现一次参数更新。

**完成标准：** 每个梯度 shape 与对应参数一致；bias 沿 batch 维求和；平均系数只计算一次；能逐步解释一个参数如何影响 loss。不要把“loss 下降一次”当作反传正确的充分证据。

<a id="w3-06"></a>

## W3-06｜有限差分验证反传

**材料：** [微积分 §5](../../../course/materials/03_calculus_optimization.md)，回看自己的 W3-05 推导。

**独立练习：** 用 `2→3→2` 的微型网络与 float64，对全部权重和 bias 分别计算中心差分 `(L(θ+ε)-L(θ-ε))/(2ε)`，取 `ε=1e-5`；与解析梯度比较。取远离 ReLU 零点的输入，扰动前后不跨越不可导点。

**完成标准：** 对各参数张量记录相对 L2 误差 `||g-num||/(||g||+||num||+1e-12)`，目标 `<1e-5`；近零梯度同时检查绝对误差。失败时逐层检查平均系数、转置、bias 轴和缓存，不靠不断放宽容差通过。

保存梯度检查表。只有解释并解决不一致后才进入真实数据训练。

<a id="w3-07"></a>

## W3-07｜先让小样本过拟合

**材料：** [神经网络 §5](../../../course/materials/10_neural_networks_and_backprop.md)。

**独立练习：** 读取 `sklearn.datasets.load_digits()`，查看 8×8 图像与 64 维向量的关系；以种子 42 分层划分约 60%/20%/20%，StandardScaler 只在训练集拟合。建立 `64→32→10` NumPy 网络，取 32 个训练样本，先用全 batch SGD，不加正则化。

**完成标准：** 记录 loss 和训练 accuracy，争取让这 32 个样本接近完全拟合；解释这只是实现与优化检查，不能证明泛化。达不到时依次检查标签、shape、梯度与学习率，记录失败证据；验证/测试数据不用于这个排错实验。

保存划分索引、预处理参数、小样本曲线与配置。

<a id="w3-08"></a>

## W3-08｜PyTorch 对照同一个计算

**材料：** 本地 [PyTorch 练习](../../../library/stanford-cs231n-2025/unpacked/47b3a1b8-assignment2/PyTorch.ipynb)，只读 Tensor、autograd、模型与训练循环部分。

进入本单元前按 [PyTorch 环境指南](../../../docs/setup/DEEP_LEARNING.md) 准备 `.venv` 并选好内核；配置时间单独记录。先确认 `import torch` 和一个最小 Tensor 梯度例子能运行。

**独立练习：** 用 `nn.Linear → ReLU → nn.Linear` 建等价网络，复制 NumPy 权重和 bias；注意 `nn.Linear.weight` 与前面 `X @ W` 的权重排列需要转置。用相同输入、float64、相同平均交叉熵，对照 logits、loss、每个参数梯度和一次 SGD 更新。

**完成标准：** 使用预先记录的数值容差（例如 `atol=1e-8, rtol=1e-6`）核对一致；解释 `zero_grad → backward → step` 的职责。传入 CrossEntropyLoss 的是 logits，不先 softmax。保存对照表。

<a id="w3-09"></a>

## W3-09｜训练、学习率实验与冻结

**材料：** [训练模式 §1、§2、§6](../../../course/materials/11_deep_learning_patterns.md)，本次只执行下面的单因素比较。

**独立练习：**

1. 使用 W3-07 的划分与预处理，先训练逻辑回归 baseline，记录验证 accuracy。
2. 用 PyTorch 的 `64→32→10` 网络和 SGD，比较学习率 0.01、0.1；两次都从同一初始权重出发，使用相同 seed、batch_size=64、50 epochs 和批次顺序。
3. 保存 train/validation loss 与 accuracy；提前规定每轮仅在 validation loss 创新低时保存 checkpoint，平局保留较早轮次。
4. 按各自最佳 validation loss 选一个网络配置，记录实际 epoch；暂不看测试表现。

**完成标准：** 能从曲线解释优化情况与泛化差距，说明两次实验只有学习率这一核心变量不同；一个种子的教学比较不作稳健性结论。保留失败运行，不另外增加 Adam、dropout 或 BatchNorm 搜索。

<a id="w3-10"></a>

## W3-10｜重新加载、最终评价与讲解

**材料：** 自己保存的配置、梯度检查、训练记录和 checkpoint。

**独立练习：** 先冻结预处理、网络与 checkpoint；重建模型、加载 state_dict，在 `eval()` 和关闭梯度的条件下推理，与保存前的同一输入 logits 对照。对冻结网络和 baseline 做最终测试评价，报告 accuracy、逐类指标与混淆矩阵；展示最多 10 张错误图片，不足 10 张则全部展示。

**最终目录应包含：** `network.ipynb` 或对应代码、梯度/框架对照表、训练曲线、结果文件、权重、预处理与配置、README。README 记录环境、运行方法、数据划分、参数选择规则、误差案例及局限。

**过关检查：** 能手写一轮训练流程、解释各 shape、解释梯度检查、区分训练失败和过拟合、从新内核重新加载并复现推理。按 [通用项目评分](../../../course/ASSESSMENT.md#project-rubric) 自评 ≥70，且无泄漏、可复现，再勾选进度表 0c。

完成后另安排 75 分钟做 [T0](../../../course/tests/T0_math_diagnostic.md)，按错题进入 [数学基础阶段](../../../course/STUDY_GUIDE.md#phase-1)。第一次诊断不设通过门槛。

## 前期范围到这里为止

当前只完成 A06 的入门范围，多优化器、多 seed、归一化和系统故障诊断在阶段 4 补齐。Transformer、RAG、Agent 的系统实现见阶段 5；好奇时可选读概念，但不增加当前验收任务。
