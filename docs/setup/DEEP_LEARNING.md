# Week 3：PyTorch 环境与第一次运行

[项目首页](../../README.md) · [环境配置](README.md) · [Week 3 教程](../../assignments/bootcamp/week3/README.md)

全部课程统一使用项目原有的 `.venv`，包含分类、NumPy 和 PyTorch 示例。示例默认 CPU，使用 scikit-learn 自带的 digits 数据，无需下载训练数据或购买 GPU。

## 安装依赖

在项目根目录运行；仅在 `.venv` 不存在时执行创建命令：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name ml --display-name "ML · Python (.venv)"
```

依赖统一声明在 [requirements.txt](../../requirements.txt)，本机验证版本记录见 [requirements-tested.txt](../../requirements-tested.txt)，后者不是跨平台锁文件。教程不需要 torchvision、torchaudio 或 CUDA。

NJU 大语言模型课程也使用这个环境，额外依赖和 Graphviz 说明见 [NJU 课程环境](../../library/nju-llm-2026/README.md#环境与模型)。

## 确认导入并启动

```bash
.venv/bin/python -c "import sys, torch, sklearn; print(sys.executable); print('torch:', torch.__version__); print('sklearn:', sklearn.__version__)"
.venv/bin/python -m jupyter lab
```

打开 [PyTorch 带练 Notebook](../../assignments/bootcamp/week3/02_pytorch_training_walkthrough.ipynb)。在 JupyterLab 中选择 `ML · Python (.venv)` 内核，在 VS Code 中选择项目的 `.venv/bin/python`。第一段代码打印的 Python 路径应位于本项目的 `.venv` 中。

环境合并后，已打开的 Notebook 需要重新选择内核并重启，再从头运行。

## 遇到问题

| 现象 | 先做什么 |
|---|---|
| `No module named torch` | 打印 `sys.executable`，确认使用本项目的 `.venv`，并在该环境安装 `requirements.txt` |
| 找不到 `numpy_mlp` | 保留 Notebook 与同目录的 `numpy_mlp.py`；从项目目录内启动，运行开头的路径初始化单元 |
| dtype 或 shape 不一致 | 数值对照部分两边均用 float64；注意 NumPy 与 Linear 权重的转置关系 |
| 重新运行时结果异常 | 重启内核，从头顺序执行；比较学习率前每次重置权重与数据顺序 |

## 运行验证

在项目根目录运行：

```bash
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_bootcamp.py
```

验证脚本使用 `.venv` 启动干净内核执行三本带练 Notebook，原文件不写入执行输出；执行副本保存到各周的 `outputs/verified/`。示例的结果表、图像和模型保存在各周 `outputs/` 下。通过验证表示示例可运行，自己的练习仍需独立完成。
