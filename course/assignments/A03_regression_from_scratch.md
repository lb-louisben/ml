# A03：从零实现回归

来源类型：本仓库自制；参考 ISLP 回归章节、MIT 18.06 最小二乘与 CS229 线性回归主题。预计 8～10 小时，100 分。

## 任务

1. 只用 NumPy 实现带截距的 ordinary least squares：normal equation/pseudoinverse 与 gradient descent 两个版本。
2. 用合成数据验证参数恢复；逐步增加噪声和共线性，记录参数与预测误差变化。
3. 实现 Ridge 的闭式解（截距不惩罚），至少比较 8 个对数尺度 alpha。
4. 用 sklearn Pipeline 在一个真实数据集上建立 mean baseline、LinearRegression、Ridge。
5. 使用交叉验证选择 alpha；最终只在测试集评价一次。
6. 报告 MAE、RMSE、R²、残差图；bootstrap 估计 MAE 的 95% 区间。

## 书面问题

- 为什么训练误差不会因增加特征而上升，而测试误差可能上升？
- 标准化为何影响 Ridge 的惩罚含义？
- R² 为负意味着什么？它是否一定表示代码有错？
- 系数能否解释为因果效应？列出至少三个必要但当前不满足的条件。

## 测试

至少写 5 个自动测试：维度、已知小例、奇异矩阵、梯度检查、与 sklearn 的容差比较。禁止调用 sklearn 的模型来实现“from scratch”部分。

## 提交

src/linear_models.py、tests/、a03.ipynb、report.md、requirements 或 environment 说明。
