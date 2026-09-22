# P1：表格模型 Benchmark

来源类型：本仓库自制；项目结构参考 Berkeley Data 100 与 Stanford CS229 的端到端训练方式。周期 1～2 周。

## 目标

在一个有现实语境的回归或分类数据集上，证明你能把“高分模型”变成“可信实验”。建议选择 UCI 或政府开放数据，至少 5,000 行；若不足，重点加强不确定性分析。

## 必须比较

- 简单 baseline：均值/中位数或 majority/Dummy。
- 可解释线性模型：Ridge 或 Logistic Regression。
- 树模型：Decision Tree/Random Forest。
- boosting：XGBoost、LightGBM 或 sklearn HistGradientBoosting 三选一。

## Milestones

1. Proposal：一页，定义用户、预测时点、标签、指标、代价、数据许可和风险。
2. Data freeze：保存原始数据 hash、split seed 或时间切点；测试标签之后不再查看。
3. Baseline：一条命令生成 baseline 指标。
4. Model selection：同一 CV/验证协议比较模型；报告分布和训练成本。
5. Final：冻结后一次测试；至少 10 个错误案例和两个 slice。

## 最低实验表

每行包括 model、features、hyperparameters、CV mean/std、test metric（仅最终行）、fit time、seed、notes。回归报告 MAE/RMSE/R²；分类报告 confusion matrix、F1、ROC-AUC，类别不平衡时加入 PR-AUC 与 calibration。

## 交付

README.md、data card、src/、notebooks/、configs/、tests/、results.csv、model card、最多 4 页 report。README 必须给出从新环境获取数据、训练和复现最终表格的命令。

## Demo 提问

- 如果测试分布变了，哪个指标最先坏？
- 哪个特征最可能泄漏？
- 为什么当前最佳模型优于 baseline？证据来自哪里？
- 移除一个关键特征后会怎样？
- 你明确不建议把模型用在哪里？
