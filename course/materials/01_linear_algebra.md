# 01：机器学习所需线性代数

目标：读懂向量化公式；从几何角度理解最小二乘、PCA 和神经网络层；能检查 shape、rank 与数值稳定性。

## 1. 向量、矩阵与 shape

约定 n 是样本数，d 是特征数。设计矩阵 X 的 shape 为 n×d；参数 w 为 d×1；预测 Xw 为 n×1。矩阵乘法 A(m×n)B(n×p) 的结果是 m×p，中间维必须相同。

向量点积 xᵀw 同时有三种理解：加权和；两个方向的相似度；把 x 投影到 w 方向后乘以尺度。线性模型和神经元都以它为核心。

## 2. 线性组合、span、basis、rank

X 的 column space 是所有 Xw 能产生的向量集合。rank 是独立列的数量。若两列完全相同，参数可能不唯一：可以把权重从一列移到另一列而保持预测不变。

null space 是满足 Xv=0 的所有 v。若存在非零 v，则 w 与 w+v 给出相同预测；这就是参数不可辨识的一种形式。

## 3. 投影与最小二乘

最小二乘选择 w，使残差 r=y-Xw 的平方长度最小。最优点满足 Xᵀr=0，即残差与 X 的每一列正交：Xw 是 y 在 column space 上的投影。

由 Xᵀ(y-Xw)=0 得 normal equation：

    XᵀXw = Xᵀy

若 XᵀX 可逆，w=(XᵀX)^(-1)Xᵀy。实际计算不应显式求逆；使用 least-squares solver、QR 或 SVD 更稳定。若不可逆，可用 pseudoinverse，或 Ridge 的 XᵀX+alpha I。

## 4. 特征值、正定与优化

Av=lambda v 表示 v 经过 A 变换后方向不变，只缩放 lambda。对称矩阵有正交 eigenvectors 和实 eigenvalues。Hessian 的 eigenvalues 描述不同方向的曲率；条件数很大时，梯度下降会在狭长谷底来回震荡。

对任意非零 x，xᵀAx>0 的对称矩阵为 positive definite。若二次损失的 Hessian 正定，目标严格凸，最优解唯一。

## 5. SVD 与 PCA

任何矩阵可写为 X=U Sigma Vᵀ。V 的列给输入空间方向，Sigma 的 singular values 给各方向强度，U 给输出空间方向。rank-k 近似只保留最大的 k 个 singular values，是平方重构误差下的最佳 rank-k 近似。

PCA 对中心化数据计算主要方向。保留前 k 个方向既最大化投影方差，也最小化线性 rank-k 重构误差。必须只在训练集 fit 均值和方向，再 transform 验证/测试集。

## Worked example

X 的两列分别为 [1,2]ᵀ 和 [2,4]ᵀ。第二列是第一列的两倍，所以 rank=1。向量 v=[-2,1]ᵀ 满足 Xv=0。参数 [0,1] 与 [2,0] 都产生预测 [2,4]ᵀ：系数不同，预测相同。

## 常见错误

- 把 element-wise multiplication 当成 matrix multiplication。
- 在包含截距时忘记 one-hot 全列会产生完全共线。
- 认为 PCA 的最大方差方向一定最利于分类。
- 显式求大矩阵 inverse，而不是使用稳定 solver。
- 未中心化就直接把 PCA 方向解释为协方差主轴。

## 自测

1. X 为 100×5，w 为 5×1，Xw 和 XᵀX 的 shape 各是什么？
2. 为什么完全共线会影响系数，但 fitted values 仍可能唯一？
3. 最小二乘残差为何与 column space 正交？
4. SVD 中 singular value 很小说明什么？
5. 为什么 PCA 必须只 fit 训练集？

答案要点：100×1、5×5；存在 null-space 参数方向；一阶最优条件；对应方向信息/能量弱且反演不稳定；避免泄漏并保持同一坐标系。

配套：[A01](../assignments/A01_math_and_optimization.md) · [T0](../tests/T0_math_diagnostic.md)
