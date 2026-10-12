# 10：神经网络与反向传播

目标：从线性层和激活函数构建 MLP；手推和实现 forward/backward；使用 gradient check、训练曲线和 sanity check 找 bug。

## 1. 一层在做什么

线性层 z=XW+b，把输入做仿射变换；激活 a=g(z) 引入非线性。若多层之间没有非线性，多个线性层仍可合并为一层，表达能力不会增加。

常用激活：ReLU=max(0,z)，计算简单但负区间 gradient 为 0；sigmoid 输出 0～1，但大正/负输入容易饱和；GELU 是 Transformer 中常见的平滑门控式激活。

## 2. Loss

回归常用 MSE。多分类常用 softmax cross-entropy。实现时使用框架的数值稳定版本，不先手工 softmax 再 log；log-sum-exp 技巧避免 overflow/underflow。

## 3. Backprop

forward 保存 backward 所需的中间量；backward 接收上游 gradient，计算输入 gradient 与参数 gradient。若同一变量通过多条路径影响 loss，贡献要相加。

线性层形状：X 为 B×D，W 为 D×H，Z 为 B×H。若上游 dZ 为 B×H：

    dW = Xᵀ dZ
    db = 对 batch 维求和 dZ
    dX = dZ Wᵀ

## 4. 初始化

所有权重初始化为 0 会使同层神经元保持对称，学到相同特征。随机初始化打破对称。Xavier/Glorot 适合保持线性/tanh 方差，He 初始化适合 ReLU 风格；原则是让信号和 gradient 不随层数爆炸或消失。

## 5. 训练诊断顺序

1. 检查数据、标签和 shape。
2. 在极小 batch 上过拟合到接近 100%。
3. gradient check 或与框架 autograd 对照。
4. 检查初始 loss 是否合理，例如 K 类随机预测约 log(K)。
5. 再加入 regularization、augmentation、scheduler。

## Worked example

3 类随机分类器的 softmax 概率约各 1/3，单样本 cross-entropy 约 -log(1/3)=log(3)≈1.10。若初始化后的平均 loss 是 100 或 NaN，应先查 logits 尺度、标签和数值稳定性。

## 常见错误

- 训练前就在模型中堆入 dropout、augmentation 等变量。
- ReLU backward 没使用 forward 的 mask。
- db 沿错误 axis 求和。
- 忘记每步清空累计 gradient。
- 把 autograd 能运行当成数学和数据都正确。

## 自测

1. 为什么纯线性层堆叠仍是线性？
2. B×D 输入乘 D×H 权重，输出与 dW shape？
3. 为什么全零初始化失败？
4. K 类随机模型初始 CE 大约是多少？
5. 小 batch 也无法过拟合说明什么？

答案要点：仿射变换可合并；B×H 与 D×H；神经元对称；log(K)；实现、优化、标签或容量存在基本问题。

当前练习与掌握标准统一见 [课程路线](../STUDY_GUIDE.md)。
