# A04：分类、阈值与错误切片

来源类型：本仓库自制；参考 Data 100 的建模/评估结构与 CS189 分类主题。只选与当前单元有关的题，不要求整份完成。

## 场景

选一个二分类问题，并写出 false positive 与 false negative 的实际代价。若数据没有真实业务语境，明确把代价设定标为假设。

## 任务

1. 建立 majority/Dummy baseline。
2. 用同一数据划分比较 Logistic Regression、Decision Tree、Random Forest，另选一个 boosting 模型为 Bonus。
3. 所有缺失处理、缩放、编码放入 Pipeline。调参只使用训练/CV 或验证集。
4. 报告 confusion matrix、precision、recall、F1、ROC-AUC；不平衡任务增加 PR-AUC。
5. 用验证集选择阈值，使显式代价函数最小；与阈值 0.5 比较。
6. 检查概率校准（reliability curve 或 Brier score）。
7. 选两个有意义的 slice 比较错误率，同时报告样本量和置信区间或 bootstrap 波动。
8. 冻结全部选择后，在测试集运行一次。

## 必答题

- 为什么 ROC-AUC 高不保证部署阈值好？
- class_weight、resampling、改阈值分别改变了什么？
- feature importance 为何不自动等于因果重要性？
- 如果测试集表现远低于 CV，给出至少四个可能原因和排查顺序。

## 可保留的成果

classification.ipynb、model_pipeline.joblib、metrics.json、model_card.md、README.md。模型卡必须包含预期用途、不适用范围、训练数据、指标和已知失败模式。
