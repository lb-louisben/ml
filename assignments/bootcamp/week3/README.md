# 小网络与 PyTorch 章节索引

[示例总览](../README.md) · [课程路线](../../../course/STUDY_GUIDE.md) · [环境](../../../docs/setup/README.md)

D1–D3 从 [PyTorch 训练带练](02_pytorch_training_walkthrough.ipynb) 开始；需要解释反传时查 [NumPy 网络带练](01_numpy_network_walkthrough.ipynb) 和 [参考实现](numpy_mlp.py)。两本都可独立执行，使用 sklearn 内置 digits 小数据，默认 CPU。

| 定位 | 内容 |
|---|---|
| <a id="w3-01"></a>[shape](01_numpy_network_walkthrough.ipynb#w3-01) | batch 经过线性层和 ReLU |
| <a id="w3-02"></a>[梯度](01_numpy_network_walkthrough.ipynb#w3-02) | 链式法则与学习率 |
| <a id="w3-03"></a>[前向](01_numpy_network_walkthrough.ipynb#w3-03) | 中间量与初始化 |
| <a id="w3-04"></a>[损失](01_numpy_network_walkthrough.ipynb#w3-04) | logits 与稳定交叉熵 |
| <a id="w3-05"></a>[反传](01_numpy_network_walkthrough.ipynb#w3-05) | 逐层梯度与维度 |
| <a id="w3-06"></a>[梯度检查](01_numpy_network_walkthrough.ipynb#w3-06) | 有限差分核对实现 |
| <a id="w3-07"></a>[小样本排错](01_numpy_network_walkthrough.ipynb#w3-07) | 过拟合训练小 batch |
| <a id="w3-08"></a>[Autograd](02_pytorch_training_walkthrough.ipynb#w3-08) | Tensor、计算图与 NumPy 对照 |
| <a id="w3-09"></a>[训练循环](02_pytorch_training_walkthrough.ipynb#w3-09) | optimizer、train/eval、学习率 |
| <a id="w3-10"></a>[评价与保存](02_pytorch_training_walkthrough.ipynb#w3-10) | 冻结模型、错误分析与推理恢复 |

自己的实验放进 `work/bootcamp/week3/`。复制 Notebook 时先调整 `numpy_mlp` 导入和 `OUT` 输出路径，并打印模块位置确认。能解释训练循环、各 shape 和一次失败实验后进入 CNN；不额外安排数学考试或第三份项目。
