# A05：概率模型与核方法

来源类型：本仓库自制；主题参考 Stanford CS229 与 Berkeley CS189。只选与当前单元有关的题，不要求整份完成。

## Part A：GDA 与 Logistic Regression

1. 假设两类共享协方差，从 Bayes rule 推导线性 decision boundary。
2. 只用 NumPy 实现 GDA，加入协方差稳定项。
3. 在 2D 合成数据上比较 GDA 与 Logistic Regression：小样本、类不平衡、非 Gaussian、协方差不共享四种情形。
4. 解释何时生成式假设带来样本效率，何时带来偏差。

## Part B：SVM 与 Kernel

1. 画图解释 margin、support vectors、C 的作用。
2. 实现 linear kernel 与 RBF kernel 的 Gram matrix，并检查对称性和数值特征值。
3. 在 moons/circles 数据上比较 linear、polynomial、RBF；控制同一划分。
4. 画 C、gamma 的验证热图；解释极端区域为何欠拟合或过拟合。

## Part C：研究式表达

写 800～1200 字 memo：问题、假设、实验、结果、反例和下一步。引用实际使用的公开来源，并标出访问日期。

提交 derivations.pdf、a05.ipynb、src/、report.md。实验种子至少运行 5 次，报告均值与标准差。
