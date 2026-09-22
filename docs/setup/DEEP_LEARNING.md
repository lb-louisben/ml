# Week 3：PyTorch 环境与第一次运行

[项目首页](../../README.md) · [基础环境](README.md) · [Week 3 教程](../../course/bootcamp/week3/README.md)

Week 2 分类教程与 Week 3 NumPy 教程使用原 `.venv`。进入 PyTorch 教程时使用独立 `.venv-dl`，示例默认 CPU，使用 scikit-learn 自带的 digits 数据，无需下载训练数据或购买 GPU。

## 建立环境

在项目根目录运行。若 `.venv-dl` 已存在，先做下一节的导入检查，无需重建。

```bash
python3 -m venv .venv-dl
.venv-dl/bin/python -m pip install -r requirements-dl.txt
.venv-dl/bin/python -m ipykernel install --prefix .venv-dl --name ml-dl --display-name "ML · PyTorch (.venv-dl)"
```

本机已于 2026-09-21 建立 `.venv-dl`，确认 Python 3.14.6 / PyTorch 2.14.0 可导入且依赖检查通过；直接选择该环境即可。版本记录见 [requirements-dl-tested.txt](../../requirements-dl-tested.txt)，这是当前机器的直接依赖记录，不是跨平台锁文件。

依赖声明见 [requirements-dl.txt](../../requirements-dl.txt)。PyTorch 的可用安装包随 Python、系统和架构而变；若提示 `No matching distribution`，先记录 `python3 --version` 和系统信息，再按 [PyTorch 官方安装页](https://docs.pytorch.org/get-started/locally/) 选择受支持的组合。教程不需要 torchvision、torchaudio 或 CUDA。

## 确认导入并启动

```bash
.venv-dl/bin/python -c "import sys, torch, sklearn; print(sys.executable); print('torch:', torch.__version__); print('sklearn:', sklearn.__version__)"
.venv-dl/bin/python -m jupyter lab
```

打开 [PyTorch 带练 Notebook](../../course/bootcamp/week3/02_pytorch_training_walkthrough.ipynb)。在内核选择器中选 `.venv-dl/bin/python` 对应的内核；第一段代码打印的 Python 路径应包含 `.venv-dl`。

如果习惯从原 `.venv` 启动 JupyterLab，可把新内核注册到原项目环境中：

```bash
.venv-dl/bin/python -m ipykernel install --prefix .venv --name ml-dl --display-name "ML · PyTorch (.venv-dl)"
```

刷新 JupyterLab 后选 `ML · PyTorch (.venv-dl)`。这个注册写在项目内，不修改全局 Python 环境。VS Code 可直接选择 `.venv-dl/bin/python`。

## 遇到问题

| 现象 | 先做什么 |
|---|---|
| `No module named torch` | 打印 `sys.executable`，确认正在使用 `.venv-dl`，而非仅在另一个终端激活环境 |
| 找不到 `numpy_mlp` | 保留 Notebook 与同目录的 `numpy_mlp.py`；从项目目录内启动，运行开头的路径初始化单元 |
| dtype 或 shape 不一致 | 数值对照部分两边均用 float64；注意 NumPy 与 Linear 权重的转置关系 |
| 重新运行时结果异常 | 重启内核，从头顺序执行；比较学习率前每次重置权重与数据顺序 |

## 运行验证

在项目根目录运行：

```bash
.venv/bin/python scripts/verify_bootcamp.py
```

它分别启动干净内核执行三本带练 Notebook，原文件不写入执行输出；执行副本保存到各周的 `outputs/verified/`。示例的结果表、图像和模型保存在各周 `outputs/` 下。通过验证表示示例可运行，自己的练习仍需独立完成。
