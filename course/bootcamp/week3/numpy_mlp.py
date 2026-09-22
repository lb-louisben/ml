"""入门 3 使用的两层 NumPy 网络；推导和逐步演示见 01_numpy_network_walkthrough.ipynb。

约定：每一行是一个样本，标签是从 0 开始的整数；参数使用 float64。
网络：X @ W1 + b1 → ReLU → h1 @ W2 + b2，输出未经 softmax 的 logits。
这里有意只保留最小实现，方便逐行阅读和与 PyTorch 对照。
"""

import numpy as np


def init_params(input_dim, hidden_dim, output_dim, seed=42):
    """生成独立的参数字典；固定种子只控制本函数的随机生成器。"""
    rng = np.random.default_rng(seed)
    return {
        # W1 之后接 ReLU，用 He 缩放控制激活的初始尺度。
        "W1": rng.normal(size=(input_dim, hidden_dim)) * np.sqrt(2.0 / input_dim),
        "b1": np.zeros(hidden_dim, dtype=np.float64),
        # 输出层后没有 ReLU；这里按输入维度缩放随机权重。
        "W2": rng.normal(size=(hidden_dim, output_dim)) * np.sqrt(1.0 / hidden_dim),
        "b2": np.zeros(output_dim, dtype=np.float64),
    }


def forward(X, params):
    """返回 logits 和反传缓存；不更新参数，不在这里计算概率。"""
    z1 = X @ params["W1"] + params["b1"]  # (B,D) @ (D,H) → (B,H)
    h1 = np.maximum(z1, 0.0)             # 保留正数，负数变为 0
    logits = h1 @ params["W2"] + params["b2"]  # (B,H) @ (H,K) → (B,K)
    return logits, {"X": X, "z1": z1, "h1": h1}


def softmax_cross_entropy(logits, y):
    """用稳定的 log-sum-exp 返回平均交叉熵与各行类别概率。

    y 的 shape 为 (B,)，值域为 [0, K)；不接受 one-hot 标签。
    同一行减一个常数不改变 softmax，先减最大值可防止 exp 溢出。
    不直接对可能下溢成 0 的概率取 log，也不人为截断概率。
    """
    shifted = logits - logits.max(axis=1, keepdims=True)
    exp_shifted = np.exp(shifted)
    normalizer = exp_shifted.sum(axis=1, keepdims=True)
    log_probabilities = shifted - np.log(normalizer)
    probabilities = exp_shifted / normalizer
    loss = -log_probabilities[np.arange(len(y)), y].mean()
    return float(loss), probabilities


def loss_and_gradients(X, y, params):
    """返回平均交叉熵及每个参数的解析梯度；每次从零计算，不累加。"""
    logits, cache = forward(X, params)
    loss, probabilities = softmax_cross_entropy(logits, y)

    # 对平均 CE，dlogits = (概率 - one_hot) / B。平均系数只出现一次。
    dlogits = probabilities.copy()
    dlogits[np.arange(len(y)), y] -= 1.0
    dlogits /= len(y)

    dW2 = cache["h1"].T @ dlogits          # (H,B) @ (B,K) → (H,K)
    db2 = dlogits.sum(axis=0)              # 沿 batch 汇总 → (K,)
    dh1 = dlogits @ params["W2"].T        # (B,K) @ (K,H) → (B,H)
    dz1 = dh1 * (cache["z1"] > 0.0)       # ReLU 的局部导数；0 点约定为 0
    dW1 = cache["X"].T @ dz1              # (D,B) @ (B,H) → (D,H)
    db1 = dz1.sum(axis=0)                  # 沿 batch 汇总 → (H,)
    return loss, {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}


def sgd_step(params, grads, lr):
    """按 θ ← θ - lr × gradient 原地更新参数；调用前先保存需要的旧值。"""
    for name in params:
        params[name] -= lr * grads[name]


def predict(X, params):
    """返回最大 logit 对应的整数类别；argmax 前无需计算 softmax。"""
    logits, _ = forward(X, params)
    return logits.argmax(axis=1)
