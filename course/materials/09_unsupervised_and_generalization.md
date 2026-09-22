# 09：无监督学习、EM 与泛化

目标：理解 k-means、GMM/EM 和 PCA；知道无标签结构不等于真实类别；建立关于泛化、模型选择偏差和分布漂移的基本判断。

## 1. k-means

k-means 最小化每个点到所属 centroid 的平方距离。算法交替进行：把点分给最近 centroid；把 centroid 更新为簇均值。目标每步不增，但只保证局部最优，所以要多次初始化。

尺度会直接影响距离，通常应基于训练数据标准化。k 必须外部选择；elbow、silhouette 只是辅助，最终还要看稳定性和问题意义。

## 2. GMM 与 EM

GMM 把数据看成多个 Gaussian component 的混合，每个点有 soft responsibility。E-step 用当前参数计算 component posterior；M-step 用 responsibilities 加权更新 mixture、mean 和 covariance。

EM 是对 latent-variable likelihood 的迭代优化，每轮不降低观测 likelihood，但仍可能停在局部最优或退化解，需要初始化和 covariance regularization。

## 3. PCA 再提醒

PCA 是线性投影，不是聚类。高方差方向未必是区分类别的方向；在聚类前做 PCA 可能降噪，也可能删除低方差但关键的分离信号。选择维度应在具体下游目标上验证。

## 4. 泛化与选择偏差

empirical risk 是训练样本平均损失；expected risk 是对真实分布的期望损失；regularized empirical risk 加入复杂度惩罚。我们只能观测样本，因此用 holdout、CV、正则化和简化假设控制选择偏差与 variance。

搜索 1,000 个超参数后取最高 validation 分数，会挑中噪声幸运者。搜索越大，validation overfitting 越严重。nested CV 用 inner loop 选择、outer loop 估计；或保留完全未触碰的最终 test。

## 5. Distribution shift

- Covariate shift：p(x) 变。
- Label/prior shift：p(y) 变。
- Concept shift：p(y|x) 变。

离线高分不保证部署稳定。需要监控输入质量、关键特征分布、预测分布、延迟标签后的性能与群体差异。

## Worked example

对含身高（厘米）和收入（元）的数据直接 k-means，收入的数值尺度会主导距离。标准化可平衡尺度，但也隐含“两个维度一个标准差同等重要”的选择，应在报告中说明。

## 自测

1. k-means 为什么需要多次初始化？
2. EM 的 E/M 两步分别做什么？
3. 聚类簇为何不一定等于真实类别？
4. 为什么大规模调参会使 validation 分数乐观？
5. p(y|x) 改变属于哪种 shift，为什么最难？

答案要点：局部最优；算 latent posterior/最大化期望 complete likelihood；目标只优化几何/概率结构；从更多噪声中选极值；concept shift，旧映射本身失效。

配套：[T1](../tests/T1_undergraduate_midterm.md) · [T2](../tests/T2_graduate_ml_final.md)
