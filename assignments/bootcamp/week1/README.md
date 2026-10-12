# 回归与基础工具索引

[示例总览](../README.md) · [课程路线](../../../course/STUDY_GUIDE.md)

M1–M2 先打开 [学生成绩完整项目](project/08_Student_performance_project.ipynb)。以下为查漏补缺索引，不要求依次补完。

| 内容 | Notebook | 需要确认什么 |
|---|---|---|
| Python | [基础](day1/01_Python_basic_and_score_analyze.ipynb) · [补充](day1/01_Python_depth_breadth_bonus.ipynb) | 函数、列表、循环 |
| NumPy | [数组](day2/02_NumPy.ipynb) · [补充](day2/02_NumPy_depth_breadth_bonus.ipynb) | shape、axis、广播 |
| Pandas | [读表与清洗](day3/03_Pandas_data_cleaning.ipynb) | 字段、索引、清洗依据 |
| EDA | [可视化](day4/04_Visualization_EDA.ipynb) | 图表回答什么，局限是什么 |
| 实验流程 | [划分与泄漏](day5/05_ML_workflow_and_splits.ipynb) | 训练、验证、测试的职责 |
| 回归 | [线性回归与 Pipeline](day6/06_Linear_regression.ipynb) | fit/predict、参数、预处理 |
| 评价 | [指标与误差](day7/07_Metrics_and_final_evaluation.ipynb) | MAE/RMSE/R²，冻结后评价 |

## 练习定位

<a id="w1-01"></a>**Python：** 写一个成绩统计函数，验证空列表和并列最高分。

<a id="w1-02"></a>**NumPy：** 对 4×3 矩阵计算行列均值，先写 shape 再运行。

<a id="w1-03"></a>**读表：** 解释一行、一个字段及目标变量的含义。

<a id="w1-04"></a>**清洗：** 在教学副本记录每条规则及影响，不改原始数据。

<a id="w1-05"></a>**EDA：** 仅在训练集画图，分别写观察、证据、局限。

<a id="w1-06"></a>**划分：** 验证索引互斥，说明预测时能使用哪些特征。

<a id="w1-07"></a>**回归：** 手算一条记录的预测，与程序对照。

<a id="w1-08"></a>**Pipeline：** 比较 Dummy、单特征与固定多特征模型，预处理仅在训练集拟合。

<a id="w1-09"></a>**评价：** 冻结方案后查看测试指标与错误案例，不将结果用于调参。

<a id="w1-10"></a>**整理：** 在 `work/bootcamp/week1/` 保存自己的实验，重启内核后复现并解释。

## 数据约定

[数据来源与字段](data/README.md)：真实学生成绩为 20 分制；前两份基础示例使用模拟数据。真实数据原件不含缺失，教学错误只注入副本。示例在第二学期成绩已知后预测最终成绩，不作开学预警。

真实数据示例固定种子 42，划分为 276/59/60 条训练/验证/测试记录。只在训练集探索与拟合，验证集选方案，测试集评价冻结方案。现有 Notebook 可独立执行，无需先运行其他文件。
