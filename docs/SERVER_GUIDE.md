# 服务器只拉作业：操作教程

[项目首页](../README.md) · [存储方案](GITHUB_STORAGE.md) · [作业目录](../assignments/README.md)

服务器使用 partial clone 获取必要 Git 对象，再用 sparse checkout 选择作业路径。讲义、参考书和海外资料归档默认不下载。只用 sparse checkout 只能缩小工作目录；减少网络传输还需要 `--filter=blob:none`，跳过历史用 `--depth=1`。依据：[Git clone 文档](https://git-scm.com/docs/git-clone)、[sparse checkout 文档](https://git-scm.com/docs/git-sparse-checkout)。

## 第一次：只拉 NJU A0

在服务器运行；`ml-server` 必须是尚不存在的新目录：

```bash
git clone --filter=blob:none --depth=1 --no-tags --no-checkout \
  git@github.com:lb-louisben/ml.git ml-server
cd ml-server
# 只取启动脚本；不先检出整个仓库
git show HEAD:scripts/server_checkout.py > /tmp/ml-server-checkout.py
python3 /tmp/ml-server-checkout.py --repo-root "$PWD" set nju-a0
```

公共仓库也可将地址改为 `https://github.com/lb-louisben/ml.git`。SSH 方式需要服务器 GitHub SSH 密钥已配置。

这个配置检出 A0 模板、已有个人 A0 实现、来源清单、最小依赖和操作工具。它不检出 `course/`、`library/`，也不带入 `work/nju-llm-2026/lecture*.ipynb` 或个人讲义。

查看和切换配置：

```bash
python3 scripts/server_checkout.py list
python3 scripts/server_checkout.py set nju-a1
python3 scripts/server_checkout.py set nju
python3 scripts/server_checkout.py set week1
python3 scripts/server_checkout.py set core-a01
python3 scripts/server_checkout.py set all-exercises
# 同时做多个部分
python3 scripts/server_checkout.py set week1 --add nju-a0
```

切换前保存并提交自己的改动，避免未提交文件使旧路径留在工作目录。工具在完整的本机学习仓库中拒绝直接切换，只允许新克隆的空工作目录或已使用 sparse checkout 的服务器目录。`set ... --dry-run` 可以预览选中的路径。

## 建环境与做 NJU A0

在仓库根目录建立独立环境；A0 的公开 CPU 测试使用 torch 和 pytest：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/nju-a0.txt
mkdir -p work/nju-llm-2026
if [ ! -e work/nju-llm-2026/a0 ]; then
  cp -R assignments/nju-llm-2026/a0 work/nju-llm-2026/a0
fi
cd work/nju-llm-2026/a0
python -m pytest test_toy.py -q
```

已有 A0 实现保留在个人目录，测试结果以实际运行和题目要求为准。原始模板中的 TODO 没有完成时测试失败是预期现象，不是目录下载故障。

A1～A5 同样复制对应模板，使用各自任务与 `requirements.txt` 配置独立环境；GPU/CUDA 包按服务器实际硬件准备。不要把 A0 的两项依赖当作全部 NJU 作业的环境。A5 模型和数据按任务 README 获取，不随代码检出。

## Bootcamp 和中文作业

```bash
python3 scripts/server_checkout.py set week1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/bootcamp.txt
python -m jupyter lab --no-browser
```

Notebook 位于 `assignments/bootcamp/week1/`。Week 1 小数据已随所选练习检出；Week 2 使用 sklearn 自带数据；Week 3 另需安装适合服务器的 PyTorch。Notebook 从项目根目录或自己的日目录运行均可定位数据。

中文作业题目在 `assignments/core/A01/`～`A08/`；个人实现建在 `work/assignments/A01/`～`A08/`。具体实验依赖按题目需要安装。

<a id="overseas"></a>

## 做海外课程时只取一个作业 ZIP

服务器已检出归档清单与下载工具；先在清单中查找所需 ZIP 的 `library/` 相对路径，例如 CS224N A1：

```bash
# 需要 gh CLI；公共资料可按其下载能力访问，私有仓库先 gh auth login
python3 scripts/library_archive.py fetch --file stanford-cs224n-w25/ff665a15-a1.zip
mkdir -p work/cs224n/a1
python3 -m zipfile -e library/stanford-cs224n-w25/ff665a15-a1.zip work/cs224n/a1
```

这只获取对应作业 ZIP，包含包内题目、代码及配套数据；不下载该课程的讲义归档。进入包内 README 指定目录再安装依赖和测试。解压的新目录需要后续检出范围包含它才能长期维护：

```bash
git sparse-checkout add --no-cone '/work/cs224n/a1/'
```

ZIP 和大规模数据属于运行所需材料，不直接提交；保留原始获取方式。自己的修改代码、Notebook 和报告可提交到 `work/`，超过普通 Git 大小限制的数据需单独归档。

## 保存成果、拉取更新

从仓库根目录运行，按实际作业选择路径：

```bash
git status --short
git add -- work/nju-llm-2026/a0
git diff --cached --stat
git commit -m "study: update NJU A0"
git pull --rebase origin main
git push origin main
```

遇到冲突时按文件检查并解决；不要强制推送。普通拉取更新维持 sparse checkout 的选择，不会自动下载 Releases。换做其他作业时重新 `set`，下载海外 ZIP 时显式调用 `fetch`。

服务器上不要运行用于完整资料库的 `download_courses.py` 或 `restore --all`，除非确实需要全部资料。全量结构检查用于本机完整仓库；服务器验证所选作业的测试和运行情况。
