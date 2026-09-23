# 环境配置与运行指南

[返回项目首页](../../README.md) · [环境测试 Notebook](00_环境测试.ipynb)

## 启动 JupyterLab

打开“终端”，依次运行：

```bash
cd "/Users/louis/Documents/workspace/School/cources/machine learning"
source .venv/bin/activate
python -m jupyter lab
```

浏览器会自动打开 JupyterLab。完成学习后，在终端按 `Control+C` 停止服务，再运行：

```bash
deactivate
```

## 在 VS Code 中使用

1. 用 VS Code 打开本课程文件夹。
2. 打开任意 `.ipynb` 文件。
3. 点击右上角的“选择内核”或 `Select Kernel`。
4. 选择当前项目的 `.venv/bin/python`。
5. 点击代码单元左侧的运行按钮。

项目已经配置默认解释器，通常会自动找到 `.venv`。

## 验证环境

打开并逐个运行 [环境测试 Notebook](00_环境测试.ipynb) 中的单元格。如果最后显示预测值约为 `10.0`，说明环境正常。

也可以在终端运行：

```bash
source .venv/bin/activate
python -c "import numpy, pandas, matplotlib, seaborn, sklearn, torch; print('环境正常')"
```

## 重新安装依赖

如果以后删除或损坏了 `.venv`，在项目根目录（包含 requirements.txt 的目录）重新创建环境：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

不要使用 `sudo pip install`，以免修改或破坏系统 Python 环境。

## 进入神经网络教程

分类、NumPy 和 PyTorch 示例统一使用本页的 `.venv` 环境。`requirements.txt` 已包含 PyTorch 与 Notebook 验证依赖；运行方法见 [PyTorch 指南](DEEP_LEARNING.md)。

NJU 2026 课程也使用同一个 `.venv`，已补充 Transformers、分词、模型加载、计算图和作业测试依赖。具体版本、检查命令和模型文件准备见 [NJU 环境说明](../../library/nju-llm-2026/README.md#环境与模型)。
