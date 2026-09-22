# 公式与决策卡

这是一页复习索引，不替代正文。闭卷测试前应能从空白纸重建这些关系，并解释每个符号。

## Shape

- X：n×d；w：d×1；y 与 y_hat：n×1。
- Linear layer：X(B×D) W(D×H) + b(H) -> Z(B×H)。
- Attention：Q(B×T×d_k)，K 同形；QKᵀ -> B×T×T；乘 V -> B×T×d_v。

## 回归

    y_hat = Xw + b
    MSE = mean((y_hat-y)^2)
    grad_w SSE = 2 Xᵀ(Xw-y)
    normal equation: XᵀXw = Xᵀy
    Ridge: loss + alpha ||w||²
    R² = 1 - SSE/SST

选择指标：一般误差可解释用 MAE；极端误差代价高用 RMSE/MSE；R² 只表示相对均值 baseline 的改善。

## 分类

    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    specificity = TN/(TN+FP)
    F1 = 2PR/(P+R)
    sigmoid(z) = 1/(1+exp(-z))
    binary CE = -[y log p + (1-y) log(1-p)]

选择指标：不平衡排序看 PR-AUC；固定决策看 confusion/cost；需要概率决策看 calibration/Brier/log loss。

## 概率

    P(A|B) = P(B|A)P(A)/P(B)
    Var(aX+b) = a² Var(X)
    log product_i p_i = sum_i log p_i

MLE 只用 likelihood；MAP 加 prior。相关不等于因果，预测好不等于干预有效。

## 优化

    w_next = w - learning_rate × gradient
    numeric_grad_i = [L(w+eps e_i)-L(w-eps e_i)]/(2eps)

Loss 不降：先查数据/标签/shape，再查 gradient，再查 learning rate 和数值稳定，最后才换复杂 optimizer。

## 无监督

- k-means：assignment step ↔ centroid update；局部最优，多初始化。
- EM：E-step 算 latent posterior；M-step 优化 expected complete log likelihood。
- PCA：中心化后取 covariance/SVD 主方向；只 fit train。

## 神经网络

    dW = Xᵀ dZ
    db = sum_batch dZ
    dX = dZ Wᵀ
    random K-class initial CE ≈ log(K)

小 batch 不能过拟合时，不要继续加模型；先查实现。

## Attention

    softmax(QKᵀ/sqrt(d_k))V

Causal mask 防未来泄漏；padding mask 防无效 token；position 表达顺序；residual 提供短路径；LayerNorm 稳定特征尺度。

## 模型选择决策

1. 明确用户、预测时点、代价。
2. 定 split，冻结 test。
3. 建最简单 baseline。
4. 预处理放 Pipeline。
5. validation/CV 选择模型与阈值。
6. 冻结后一次 test。
7. 报告不确定性、slice、错误、成本和限制。

## LLM 系统选择

- 规则可写进上下文：prompt/workflow。
- 知识变化、需引用：RAG。
- 稳定改变行为/格式：PEFT 或 fine-tuning。
- 需要动态工具规划：agent；否则固定 workflow。
- 所有方案：先冻结 eval set，再开发。

返回：[材料导航](README.md)
