# 04：数据、划分与实验设计

目标：把现实问题转成可评价的学习任务；识别数据泄漏；建立 train/validation/test、Pipeline、baseline 和可复现实验。

## 1. 从决策开始，不从模型开始

先回答：谁在什么时候用预测做什么决定？一行代表谁/什么？标签在何时可知？false positive 与 false negative 的代价是什么？如果无法回答，复杂模型只会让问题更难看清。

预测时点决定可用特征。贷款申请时预测违约，最终催收次数不可用；即使它与标签高度相关，也是 post-outcome leakage。

## 2. Train、validation、test

- Train：估计模型参数和预处理参数。
- Validation/CV：选择特征、模型、超参数和阈值。
- Test：方案冻结后一次性估计泛化表现。

重复查看 test 会把它变成 validation。若发生污染，应承认并建立新的 holdout，而不是继续称它为测试集。

## 3. 划分单位

随机按行划分只适合近似独立同分布的行。患者多次就诊应按 patient group split；面向未来应 time split；图像增强版本、同一用户文本、同一设备记录都应保持在同一 split。

## 4. Pipeline 与泄漏

任何从数据学习参数的步骤都只能 fit train：imputation、scaling、category vocabulary、feature selection、PCA、target encoding、resampling。Pipeline 的价值不仅是代码整洁，而是把正确的 fit/transform 边界固化。

典型结构：

    numeric: imputer -> scaler
    categorical: imputer -> one-hot
    both: ColumnTransformer -> model

交叉验证时整条 Pipeline 进入 CV，让每个 fold 单独 fit 预处理。

## 5. Baseline 与实验记录

回归 baseline 可预测训练集均值/中位数；分类 baseline 可预测多数类或按先验概率随机。baseline 回答“模型是否比不学习更好”。每次运行记录数据版本、split、seed、特征、参数、指标、耗时与代码版本。

## 6. 数据审计

审计 schema、单位、合法范围、主键、重复、缺失编码、rare category、标签分布与时间/群体漂移。删除任何行都报告数量和原因。缺失本身可能携带过程信息，也可能造成偏差。

## Worked example

同一学生有三个学期记录。若随机按行划分，模型可能通过前两个学期识别同一个学生，在 test 中预测第三学期，分数虚高。若目标是预测新学生，应按 student_id 分组；若目标是预测未来学期，还需保证 train 时间早于 test。

## 自测

1. 为什么在全数据上 fit scaler 是泄漏？
2. group split 与 time split 分别解决什么？
3. 为什么特征选择也必须放入 CV 内？
4. baseline 的主要作用是什么？
5. 哪些操作通常不需要 fit，可以安全对所有 split 应用？

答案要点：测试统计参与训练；身份依赖与时间因果顺序；否则 validation 信息进入特征集合；判断学习是否带来价值并校验流程；基于固定规则且不读取数据统计的纯变换。

配套：[A02](../../assignments/core/A02/A02_data_audit.md) · [P1](../projects/P1_tabular_benchmark.md)
