# 本机环境与日常使用

[项目首页](../../README.md) · [课程路线](../../course/STUDY_GUIDE.md)

## 首次安装

在项目根目录运行；已有 `.venv` 时跳过创建，只安装所需依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name ml --display-name "ML · Python (.venv)"
```

这些依赖支持现有回归、分类与 NumPy/PyTorch 示例。LLM 模型与专题依赖在选择具体任务时再配置。`requirements-tested.txt` 是现有示例的本机版本记录，不是跨平台锁文件。

## 每次学习

```bash
source .venv/bin/activate
python -m jupyter lab
```

在 JupyterLab 选择 `ML · Python (.venv)`；VS Code 打开 Notebook 后选择项目 `.venv/bin/python`。从项目根目录启动，打开路线指定的练习。结束时按 `Control+C` 停止服务，再运行 `deactivate`。

先运行参考程序并解释各段，再在 `work/<任务>/` 保存自己的改动与结果。复制 Notebook 后检查数据、导入与输出路径，避免新实验仍写回参考示例目录。

## 检查与排错

[环境测试 Notebook](00_环境测试.ipynb) 可检查数据分析与线性回归。先查看 `sys.executable`，缺包时在这个解释器里安装依赖；结果异常先重启内核、从头执行。

```bash
.venv/bin/python -m pip check
.venv/bin/python scripts/verify_week1.py
.venv/bin/python scripts/verify_bootcamp.py
```

两项示例验证使用干净内核，执行副本与结果放进被 Git 忽略的 `outputs/`。无需每次学习全部重跑；修改参考代码或环境后按受影响范围验证。

## 保存到 GitHub

按实际任务选择文件，提交前检查内容：

```bash
git status --short
git add -- work/<任务>
git diff --cached --stat
git commit -m "study: record experiment"
git pull --rebase origin main
git push origin main
```

`<任务>` 替换为自己的目录名。修改课程文档或示例时同样明确选择对应文件。遇到冲突先检查并解决；模型、缓存、环境和运行输出由 `.gitignore` 隔离。
