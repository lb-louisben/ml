# 第一周：Python 数据分析与机器学习基础

目标：用真实学生成绩数据完成读取、清洗、探索、训练、评价和解释，交付完整 Notebook。

每天主线约 2～3 小时；深度理解“为什么”，广度认识其他常见工具，Bonus 为可选挑战，额外 20～40 分钟。

| 天 | 主线与材料 | 深度 | 广度 | Bonus | 交付 |
|---|---|---|---|---|---|
| 1 | [原笔记](day1/01_Python_basic_and_score_analyze.ipynb) · [补充](day1/01_Python_depth_breadth_bonus.ipynb) | 空列表、边界、引用 | zip、enumerate、异常 | 并列最高分、输入不变 | 成绩分析函数 |
| 2 | [原笔记](day2/02_NumPy.ipynb) · [补充](day2/02_NumPy_depth_breadth_bonus.ipynb) | axis、广播、视图 | NaN、标准差、标准化 | 最小二乘直线 | NumPy 成绩报告 |
| 3 | [Pandas 清洗](day3/03_Pandas_data_cleaning.ipynb) | 缺失与零、索引对齐、清洗依据 | groupby、merge、CSV 导出 | 幂等清洗函数 | 数据质量报告 |
| 4 | [可视化](day4/04_Visualization_EDA.ipynb) | 图表误导、相关与因果 | 分组统计、图像导出 | 分组散点与联合分布 | 四图及解释 |
| 5 | [机器学习流程](day5/05_ML_workflow_and_splits.ipynb) | 数据泄漏、预测时点 | 分组/时间拆分、均值基准 | KFold | 任务定义与划分说明 |
| 6 | [线性回归](day6/06_Linear_regression.ipynb) | 损失、共线性、系数解释 | 类别编码、Pipeline | Ridge 交叉验证 | 验证集实验记录 |
| 7 | [指标与评估](day7/07_Metrics_and_final_evaluation.ipynb) | R²、残差、测试边界 | 基准比较、结果导出 | MAE bootstrap | 最终报告 |

综合参考：[学生成绩端到端项目](project/08_Student_performance_project.ipynb)。先自己做，再对照参考。

## 第三天具体安排

1. 20 分钟：读取分号分隔 CSV，检查 shape/info/head，解释行列含义。
2. 25 分钟：Series/DataFrame、loc/iloc、条件筛选、排序，完成 Assignment 1。
3. 15 分钟：检查教学副本，列出缺失、重复、类型与范围问题。
4. 40 分钟：理解每条清洗规则，运行并检查 13 行变为 10 行的证据。
5. 20 分钟：分组、连接、导出、重新读取。
6. 30 分钟：独立完成质量报告与作业；Bonus 幂等性另加 30 分钟。

## 数据与实验约定

- 前两天是 100 分制模拟数据；第三天起真实数据为 20 分制，练习以 10 分为及格线。
- 原始数据和说明见 [数据来源](data/README.md)，原始文件只读使用。
- 原始数据无缺失。教学错误仅注入训练集小副本，模型使用真实数据。
- 从第三天起，固定 random_state=42，得到 276/59/60 的训练/验证/测试划分。
- 训练集用于探索与拟合，验证集用于选择，最后一次用测试集评价冻结方案。
- 主线是假设第二学期成绩已知后的预测，不是开学预警。缺少时间戳限制了真实可用性判断。
- 每天 Notebook 独立导入和拆分。无需按文件顺序运行才能复现，但学习应按顺序。

## 每日学习方法

先读 Markdown，猜输出，再运行代码。作业区自行填写；参考答案不会自动证明你完成了练习。
完成后重启内核 Run All，补写“观察、证据、局限”，用 Git 提交当天笔记。
若出现 NameError，优先检查单元执行顺序；若数据路径找不到，检查是否在本项目内启动内核。

## 最终验收（100 分）

| 项目 | 分值 | 通过条件 |
|---|---:|---|
| 数据理解 | 15 | 来源、单位、标签、预测时点准确 |
| 清洗与质量报告 | 20 | 缺失/重复/范围规则有依据，原始数据保留 |
| 探索与图表 | 15 | 四张图及有证据的解释，仅用训练数据 |
| 实验流程 | 20 | 划分互斥、Pipeline、基准、验证选择 |
| 评价与误差 | 20 | 四指标、残差、极端误差与局限 |
| 可复现与表达 | 10 | 干净内核运行、固定种子、五条结论、Git 提交 |

Bonus 不替代核心：独热编码、Ridge/CV、bootstrap、跨学校评估作为后续研究方向。

## 参考

- [Pandas 入门](https://pandas.pydata.org/docs/user_guide/10min.html)
- [NumPy 基础](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Matplotlib 入门](https://matplotlib.org/stable/users/explain/quick_start.html)
- [scikit-learn 数据泄漏与常见陷阱](https://scikit-learn.org/stable/common_pitfalls.html)
- [UCI Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance)
