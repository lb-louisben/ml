# A01：线性代数、概率与优化

来源类型：本仓库自制；主题顺序参考 MIT 18.06SC 与 Stanford CS229 先修复习。预计 8～10 小时，100 分。

## Part A：线性代数（35 分）

1. 给定一个 4×3 矩阵，手算 rank、null space 的一组基，并解释线性回归中列相关意味着什么。
2. 从最小化 ||Xw-y||² 推导 normal equation。说明 XᵀX 不可逆时会发生什么，并给出 pseudoinverse 或 regularization 的解决方式。
3. 对一个 2×2 对称矩阵求 eigenvalues/eigenvectors；用 NumPy 验证。
4. 用 SVD 对一张灰度图做 rank-k 近似，画 k 与重构误差、存储量的关系。

## Part B：概率（25 分）

1. 用 Bayes 定理计算一个低基准率筛查问题，解释 accuracy 为什么会误导。
2. 推导 Bernoulli 的 MLE；加入 Beta prior 后写出 MAP 目标。
3. 用 10,000 次模拟验证样本均值的期望与方差；比较 n=10、100、1000。

## Part C：优化（30 分）

1. 推导 MSE 对 w 和 b 的梯度。
2. 不调用优化器，实现 batch gradient descent；记录 loss、gradient norm 和参数误差。
3. 比较三个学习率，解释发散、慢收敛和合理收敛。
4. 用有限差分做 gradient check，相对误差目标 < 1e-5。

## Part D：解释（10 分）

用不超过 500 字回答：投影、最大似然和梯度下降分别解决模型训练中的哪一层问题？三者有什么联系、又不可互相替代在哪里？

## 提交

- derivations.pdf 或清晰 Markdown
- a01.ipynb
- figures/ 中的 SVD 与 loss 图
- README：运行方式、结论、assistance 与引用

最低通过证据：normal equation 推导正确；梯度检查通过；能解释不可逆与学习率问题。
