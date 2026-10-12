# 06：分类、阈值与可靠评价

目标：从 confusion matrix 推导指标；区分排序、分类和概率质量；根据代价选阈值；对类别不平衡、校准和群体切片做可靠分析。

## 1. Confusion matrix

以正类为关注事件：TP 正确报正；FP 错误报正；FN 漏掉正类；TN 正确报负。

    precision = TP / (TP+FP)
    recall = TP / (TP+FN)
    specificity = TN / (TN+FP)
    F1 = 2 × precision × recall / (precision+recall)

accuracy 在正类稀少时可能误导。正类 2% 而全部预测负类，accuracy 98%，recall 0。

## 2. 三类评价问题

- 分类质量：给定阈值后的 confusion matrix、precision、recall、F1、成本。
- 排序质量：ROC-AUC、PR-AUC，考察正例是否排在负例前面。
- 概率质量：calibration curve、Brier score、log loss，考察概率是否可信。

AUC 高不保证特定阈值成本低，也不保证概率校准。三者不可互相替代。

## 3. ROC 与 PR

ROC 曲线画 TPR 对 FPR；ROC-AUC 对 class prior 相对不敏感。PR 曲线画 precision 对 recall；正类稀少时，PR-AUC 更直接反映命中正类的代价。比较时要确认同一测试分布和正类定义。

## 4. 阈值选择

训练模型产生 score/probability；阈值把它转成动作。应在 validation 上根据代价选择：

    total_cost = cost_FP × FP + cost_FN × FN

阈值降低通常提高 recall，但 precision 不保证单调下降，因为离散分数和样本组成会产生局部变化。部署后 class prevalence 改变，precision 和最优阈值也会改变。

## 5. Calibration 与不确定性

若所有预测约 0.7 的样本中约 70% 为正，模型在该区间校准。reliability curve 需要足够 bin 样本；小样本图很抖。校准方法也必须只在 train/validation 范围内 fit。

## 6. Slice 与公平

总体指标可掩盖群体失败。按时间、设备、地区、数据质量、关键人群切片，并同时报告样本量和区间。发现差异后先核查标签质量、选择偏差和阈值影响，不要把相关差异直接解释为模型歧视或群体本质差异。

## Worked example

TP=40、FP=10、FN=20、TN=130：precision=0.8；recall=40/60≈0.667；accuracy=170/200=0.85；F1≈0.727。

## 自测

1. ROC-AUC、F1 与 Brier score 各回答什么问题？
2. 为什么部署 prevalence 改变会影响 precision？
3. class_weight、resampling、阈值调整分别改变什么？
4. 一个 slice 指标很差但 n=8，可以得出什么结论？
5. 何时宁愿选择 AUC 略低但校准更好的模型？

答案要点：排序/阈值分类/概率；precision 依赖先验；训练目标/训练分布/决策规则；只能视为需更多数据的信号；风险决策需要可信概率时。

配套：[A04](../../assignments/core/A04/A04_classification_evaluation.md) · [T1](../tests/T1_undergraduate_midterm.md)
