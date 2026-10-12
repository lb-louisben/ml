# 05：线性回归、逻辑回归与正则化

目标：理解线性模型的几何、概率和优化视角；正确解释系数；使用 Ridge/Lasso 控制复杂度；知道线性预测不等于线性特征工程。

## 1. 线性回归

模型 y_hat=wᵀx+b。ordinary least squares 最小化残差平方和。若假设 y|x 为均值 wᵀx+b、方差固定的 Gaussian，最小平方也等价于 maximum likelihood。

“线性”是对参数线性。加入 x²、log(x)、交互 x1x2 后，模型仍可对扩展特征线性。特征工程可以产生弯曲边界，但也增加过拟合风险。

## 2. 回归指标

- MAE：平均绝对误差，与目标同单位，对极端值相对稳健；最优常数为 median。
- MSE：平均平方误差，对大残差惩罚更重；最优常数为 mean。
- RMSE：sqrt(MSE)，恢复目标单位，但仍强调大残差。
- R²=1-SSE/SST：SST 使用当前评估集的目标均值，衡量相对该常数预测的改善；测试 R² 可以为负。它与用训练集均值预测的 Dummy baseline 不完全相同。

指标应由决策代价决定，而不是哪个数字更好看。

## 3. 逻辑回归

逻辑回归先计算 score=wᵀx+b，再通过 sigmoid 得到 p(y=1|x)。它最小化 binary cross-entropy。阈值把概率变成类别，阈值不是模型训练后不可改变的常数。

系数 w_j 表示其他特征固定时，x_j 增加 1 单位带来的 log-odds 改变量；exp(w_j) 是 odds ratio。相关特征、缩放和正则化会影响解释。

## 4. GLM 与指数族直觉

Generalized Linear Model 把三件事分开：输入的线性 score；适合标签的数据分布；把分布均值和 score 连接起来的 link function。Gaussian + identity link 给线性回归；Bernoulli + logit link 给逻辑回归；count 数据常用 Poisson + log link。

指数族把许多分布写成共同形式，使 log-likelihood、充分统计量和凸优化有统一结构。学习阶段不必死背一般式，但要会从选择的标签分布推出相应 negative log-likelihood，并检查 support 是否匹配数据。

## 5. Ridge 与 Lasso

Ridge 在损失上加 alpha||w||²，使相关特征的权重收缩，降低 variance，通常不产生精确 0。Lasso 加 alpha||w||_1，可产生稀疏，但在高度相关特征间选择可能不稳定。

惩罚依赖尺度：一个单位代表的变化不同，惩罚含义就不同。因此数值特征通常先用 train 数据标准化；截距通常不惩罚。

## 6. Bias–variance

模型过简单会有高 bias：train 和 validation 都差。模型过复杂可能高 variance：train 很好，validation 明显差。增加数据主要降 variance；增强模型主要降 bias；正则化通常升 bias、降 variance。

## Worked example

模型 A 的 MAE 与模型 B 相同，但 A 的 RMSE 更高，说明 A 更可能有少量特别大的误差。若这些误差对应高风险个体，平均 MAE 会掩盖问题，应查看残差分布和 slice。

## 常见错误

- 把预测系数当因果效应。
- 类别 one-hot 全列加截距造成完全共线。
- 在标准化前比较 Ridge 系数大小。
- 用训练 R² 选复杂度。
- 报告平均残差接近 0 就认为模型很好。

## 自测

1. 为什么测试 R² 可以为负？
2. MAE 与 RMSE 相等或接近时说明什么？
3. 逻辑回归输出的 0.8 一定是校准后的 80% 概率吗？
4. Ridge 为什么通常能处理共线性？
5. 增加多项式特征后为何仍叫线性模型？
6. 为什么 count target 直接用 Gaussian/MSE 可能不理想？

答案要点：比测试集均值 baseline 更差；误差幅度较一致；不一定，需要校准检查；增加对角项、稳定解并收缩；对参数仍线性；可能产生负预测且方差结构/support 不匹配。

配套：[A03](../../assignments/core/A03/A03_regression_from_scratch.md) · [T1](../tests/T1_undergraduate_midterm.md)
