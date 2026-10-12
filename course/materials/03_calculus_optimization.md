# 03：微积分、梯度与优化

目标：能对常见损失求导；理解 chain rule、gradient、Hessian；能实现和诊断 gradient descent，并用数值梯度验证反向传播。

## 1. 导数与梯度

一维导数表示局部斜率。多变量函数 f(w) 的 gradient 是所有偏导数组成的向量，指向局部上升最快方向；负 gradient 是局部下降最快方向。

常用规则：d(x²)/dx=2x；d log(x)/dx=1/x；sigmoid 的导数为 sigmoid(x)(1-sigmoid(x))。向量二次损失 ||Xw-y||² 的梯度为 2Xᵀ(Xw-y)。

## 2. Chain rule 与计算图

若 z=f(y)，y=g(x)，则 dz/dx=(dz/dy)(dy/dx)。反向传播就是在计算图上复用 chain rule：从 loss 向输入传播局部导数并累积多条路径的贡献。反向传播计算梯度；optimizer 使用梯度更新参数，两者不是同一件事。

## 3. Gradient descent

更新式：

    w_next = w - learning_rate × gradient

learning rate 太小则慢；太大可能震荡或发散。batch GD 使用全部样本，SGD 使用单样本，mini-batch 在计算效率与噪声之间折中。Momentum 累积方向，Adam 还按参数调整尺度，但更快收敛不保证更好泛化。

## 4. 凸性、曲率和条件数

凸函数任意局部最优都是全局最优。线性回归的平方损失是凸的；深度网络通常非凸。Hessian 描述曲率。不同方向曲率差异大时，统一 learning rate 难以兼顾，标准化与良好初始化能改善优化几何。

## 5. Gradient check

对第 i 个参数，用中心差分：

    numeric_i = [L(w+epsilon e_i)-L(w-epsilon e_i)] / (2 epsilon)

与 analytic gradient 比较相对误差。epsilon 太大有截断误差，太小有浮点误差；常从 1e-5 附近尝试。ReLU 在 0 附近不可微，检查时应避开 kink。

## Worked example

f(w)=w²，w=4，gradient=8。learning rate=0.1 时新 w=4-0.8=3.2，新 loss 从 16 降到 10.24。若 learning rate=1，新 w=-4，loss 仍为 16；更大时会发散。

## 常见错误

- 求平均 loss 时忘记 gradient 也除以 batch size。
- bias 的 broadcasting 正确但 backward 汇总轴错误。
- 在更新参数前后混用梯度和 loss。
- gradient check 仍开启 dropout 或随机 augmentation。
- 只看 loss，不看 gradient norm、参数 norm 和 train/val gap。

## 自测

1. 对 (wx-y)² 求 dL/dw。
2. 反向传播与 gradient descent 的分工是什么？
3. 学习率过大的训练曲线可能是什么样？
4. 为什么特征标准化常让优化更容易？
5. 数值梯度误差大时先检查哪四件事？

答案要点：2x(wx-y)；前者算梯度、后者更新；震荡/NaN/不降；改善各方向尺度与条件数；公式、shape/axis、随机层、epsilon/精度。

配套：[A01](../../assignments/core/A01/A01_math_and_optimization.md) · [A06](../../assignments/core/A06/A06_backprop_and_training.md)
