# 08：生成式分类、SVM 与 Kernel

目标：区分生成式与判别式；理解 GDA/Naive Bayes 的假设；从 margin 理解 SVM；知道 kernel trick 的能力与代价。

## 1. 生成式与判别式

判别式模型直接学习 p(y|x) 或 decision boundary，例如 Logistic Regression。生成式模型学习 p(x|y)p(y) 或 joint distribution，再用 Bayes rule 分类，例如 GDA 和 Naive Bayes。

生成式强假设在小数据中可降低 variance，但假设错时会引入 bias。判别式通常更灵活，但可能需要更多标签。

## 2. GDA 与 Naive Bayes

GDA 假设每类 x 为 Gaussian。两类共享 covariance 时，log posterior ratio 的二次项抵消，边界是线性的；各类 covariance 不同则通常是 quadratic boundary。

Naive Bayes 假设给定 y 后各特征条件独立。这个假设常不真实，但分类只需 posterior 的相对排序；参数少也可能带来良好样本效率。概率输出可能不校准。

## 3. Margin 与 SVM

线性 SVM 寻找分离超平面并最大化最近样本到边界的 margin。只有靠近/违反 margin 的 support vectors 直接决定解。soft-margin 用 slack 容忍违反；C 大更重视训练错误，边界可能更复杂，C 小正则更强。

## 4. Kernel trick

若算法只依赖样本内积，可用 K(x,z)=phi(x)ᵀphi(z) 直接计算隐式高维空间内积。RBF kernel 根据距离产生局部相似度。gamma 大时影响范围窄，边界可非常曲折；gamma 小则更平滑。

有效 Gram matrix 应对称 positive semidefinite。Kernel SVM 训练与预测成本随样本数增长明显，不总适合大数据。

## Worked example

moons 数据在线性空间不可被一条直线良好分开。RBF kernel 可以形成弯曲边界；若 C 与 gamma 都极大，模型可能围绕单个样本画出局部小岛，在 train 几乎完美但 validation 变差。

## 常见错误

- 认为生成式模型等于生成式 AI。
- 把 Naive Bayes 的概率当成天然校准概率。
- 只调 C 不调 gamma。
- 在 scaler fit 全数据后做 SVM CV。
- 把可视化二维边界的直觉无条件推广到高维。

## 自测

1. GDA 共享 covariance 为何产生线性边界？
2. Naive Bayes 假设错了为何仍可分类？
3. SVM 的 support vector 是什么？
4. C 大与 gamma 大分别意味着什么？
5. kernel trick 避免显式计算什么？

答案要点：二次项抵消；低 variance 且只需相对 posterior；靠近/违反 margin 并决定边界的点；少容错与窄局部相似；高维 feature map。

配套：[A05](../assignments/A05_probabilistic_and_kernel_ml.md) · [T2](../tests/T2_graduate_ml_final.md)
