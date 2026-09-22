# T2：研究生机器学习期末

150 分钟，100 分。允许一张 A4 公式纸；要求写关键推导步骤。

## A. 概率模型（25 分）

1. 对 Bernoulli observations 推导参数 theta 的 MLE；加入 Beta(a,b) prior 后写出 MAP。（8）
2. 在 GDA 中，两类共享 covariance 为什么产生线性边界？若各自 covariance 不同，边界通常是什么形状？（7）
3. 解释 Naive Bayes 的条件独立假设。即使假设不真实，它为何仍可能有好分类效果？（5）
4. 判别式模型和生成式模型分别学习什么？各举一例。（5）

## B. 优化、核与泛化（30 分）

5. 写出 soft-margin SVM primal 的结构，并解释 margin、slack、C。（8）
6. kernel trick 避免了什么计算？一个 Gram matrix 要成为有效 kernel matrix 至少应满足什么性质？（6）
7. 训练损失持续下降，验证损失先降后升。给出三个机制不同的干预，并说明它们作用在哪里。（6）
8. 区分 empirical risk、expected risk 与 regularized empirical risk。（5）
9. 超参数搜索越大，最优 validation score 的乐观偏差为何越大？如何用 nested CV 或最终测试集控制？（5）

## C. 无监督学习（25 分）

10. 写出 k-means 的两个交替步骤。它保证全局最优吗？为何要多次初始化？（7）
11. 对 GMM 的 EM，分别说明 E-step 和 M-step 计算/优化什么；为什么 likelihood 不下降？（8）
12. 从“最大方差”与“最小重构误差”两个角度解释 PCA 的等价性。（6）
13. 高维聚类前直接 PCA 可能丢失哪些对聚类有用的信息？（4）

## D. 决策与责任（20 分）

14. 写出有限 MDP 的 Bellman optimality equation，并解释 value iteration 的更新含义。（7）
15. 某模型总体 AUC 提升，但小群体 false negative rate 翻倍。你会如何审计、沟通并决定是否部署？（7）
16. 复现实验结果比论文低 3 个百分点。给出至少六项按优先级排列的排查清单。（6）

答完后再打开 [评分要点](SOLUTIONS.md#t2)。
