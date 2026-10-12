# 02：概率与统计

目标：区分样本与总体、不确定性与噪声；能使用 Bayes rule、期望、方差和常见分布；理解 MLE、MAP、bootstrap 与置信区间。

## 1. 条件概率与 Bayes rule

P(A|B)=P(A∩B)/P(B)。Bayes rule：

    P(A|B) = P(B|A) P(A) / P(B)

P(A) 是 prior，P(B|A) 是 likelihood，P(A|B) 是 posterior。低基准率事件中，即使检测灵敏度高，阳性后的真实概率也可能不高，因为 false positives 来自更大的阴性总体。

## 2. 随机变量、期望和方差

E[X] 是长期平均；Var(X)=E[(X-E[X])²]。线性变换 Y=aX+b 满足 E[Y]=aE[X]+b，Var(Y)=a²Var(X)。独立变量相加时方差相加；相关时还要加 covariance 项。

标准差与原变量同单位，方差是单位平方。standard error 描述估计量随重复抽样的波动，不是样本本身的标准差。

## 3. 常见分布

- Bernoulli：一次 0/1 结果，参数 p。
- Binomial：n 次独立 Bernoulli 的成功次数。
- Gaussian：由均值和方差描述；线性组合仍为 Gaussian。
- Categorical：多类别一次结果。

分布假设是模型，不是事实。应通过残差、Q-Q、分组和敏感性分析检查其影响。

## 4. MLE 与 MAP

MLE 选择使观测数据 likelihood 最大的参数。为避免很多小概率相乘导致下溢，通常最大化 log-likelihood。独立 Bernoulli 样本的 MLE 是样本均值。

MAP 最大化 likelihood × prior，等价于最大化 log-likelihood + log-prior。许多正则化可解释为 prior：L2 对应 Gaussian 风格先验，L1 对应 Laplace 风格先验。

## 5. 抽样、不确定性和 bootstrap

统计量随样本变化。bootstrap 从现有 n 行中有放回抽 n 行，重复计算统计量，得到经验分布。它能估计许多复杂统计量的不确定性，但不能修复系统性选择偏差，也不适合直接打乱有时间/群组依赖的数据。

95% confidence interval 的频率学派解释是：若重复抽样并按同一程序构造区间，长期约 95% 的区间覆盖真实参数；不是“这一次参数有 95% 概率在区间内”。

## Worked example

患病率 1%，sensitivity 90%，specificity 95%。假设 10,000 人：100 人患病，其中 90 阳性；9,900 人未患病，其中 495 false positive。阳性共 585，阳性后患病概率为 90/585≈15.4%。

## 常见错误

- 把 P(A|B) 与 P(B|A) 混淆。
- 把标准差、standard error、confidence interval 当成同一概念。
- 只报告平均分，不报告随机种子或不确定性。
- bootstrap 时破坏患者组、时间顺序或序列结构。
- 把统计显著自动解释为实际重要。

## 自测

1. E[X]=4、Var(X)=9，Y=2X-3 的均值和方差？
2. 为什么低患病率会降低 positive predictive value？
3. MLE 与 MAP 差别在哪里？
4. bootstrap 不能修复哪类问题？
5. “95% CI”最常见的错误解释是什么？

答案要点：5 与 36；假阳性基数大；MAP 加 prior；系统偏差/错误数据生成过程；把固定参数说成有 95% 后验概率。

配套：[A01](../../assignments/core/A01/A01_math_and_optimization.md) · [T0](../tests/T0_math_diagnostic.md)
