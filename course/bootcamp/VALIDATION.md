# Week 2/3 带练教程验证

[前期总览](README.md) · [项目首页](../../README.md)

验证日期：2026-09-22。三本教程分别在干净 Jupyter 内核中从各自所在目录顺序执行，全部通过；源 Notebook 保留空执行输出，执行副本位于各周 `outputs/verified/`。

| 教程 | 代码单元数 | 结果 | 运行环境 |
|---|---:|---|---|
| [分类带练](week2/classification_walkthrough.ipynb) | 29 | 通过 | `.venv` |
| [NumPy 网络](week3/01_numpy_network_walkthrough.ipynb) | 22 | 通过 | `.venv` |
| [PyTorch 对照与训练](week3/02_pytorch_training_walkthrough.ipynb) | 26 | 通过 | `.venv-dl` |

## 验证了什么

- 分类：标签映射、索引互斥、训练集标准化统计、手算指标对照、验证集配置/阈值选择、测试前冻结、切片报告和模型恢复一致性。
- NumPy：shape、稳定交叉熵、平移不变性、batch 平均梯度、17 个参数的中心差分（ReLU 不跨分支）、32 个训练样本的小样本拟合。
- PyTorch：同权重下前向、概率、交叉熵、梯度、一次 SGD 更新的数值对照；两档学习率共用初始化与样本顺序；最佳 checkpoint 独立复制；保存预处理与权重后重载推理一致。
- 教程与导航的本地文件/章节链接、源 Notebook 格式、独立深度学习环境依赖检查。
- 已目视检查树深度比较图和训练曲线，坐标轴、图例与数据可读。

NumPy 全参数梯度检查的最大相对 L2 误差约为 `7.60e-11`，小于预设 `1e-5`。NumPy/PyTorch 数值对照的最大绝对差约为 `1.11e-16`，通过预设容差。

这只证明演示代码及其中的检查可运行，不代表个人练习已经完成。单次划分和一个随机种子的结果也不用于证明某个模型普遍更好。

## 如何复现

在项目根目录运行：

```bash
.venv/bin/python scripts/verify_bootcamp.py
```

仅检查一份教程可加 `--only classification`、`--only numpy` 或 `--only pytorch`。环境配置见 [基础环境](../../docs/setup/README.md) 和 [深度学习环境](../../docs/setup/DEEP_LEARNING.md)；直接依赖版本见 [基础版本记录](../../requirements-tested.txt) 与 [深度学习版本记录](../../requirements-dl-tested.txt)。

示例产物会覆盖各自 `outputs/` 中的同名文件；自己的成果放在 `work/`。训练出现非有限 loss 时教程会停止；修改参数的失败尝试需自行保存 traceback、配置和已生成结果，再另开实验。
