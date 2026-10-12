# 服务器：只拉作业

[项目首页](../README.md) · [练习索引](../assignments/README.md)

服务器使用 partial clone 减少文件传输，再用 sparse checkout 选择练习；`--depth=1` 跳过历史，`--no-tags` 跳过旧标签。只使用 sparse checkout 不能保证减少首次下载。依据：[Git clone](https://git-scm.com/docs/git-clone)、[sparse checkout](https://git-scm.com/docs/git-sparse-checkout)。

## 第一次克隆

在服务器运行，`ml-server` 使用一个尚不存在的新目录：

```bash
git clone --filter=blob:none --depth=1 --no-tags --no-checkout   https://github.com/lb-louisben/ml.git ml-server
cd ml-server
git show HEAD:scripts/server_checkout.py > /tmp/ml-server-checkout.py
python3 /tmp/ml-server-checkout.py --repo-root "$PWD" set week1
```

这只检出所选练习、对应个人实验目录，以及小型操作说明和配置；不会检出课程概念短章。需要推送时配置自己的 GitHub 认证，也可使用 `git@github.com:lb-louisben/ml.git`。

## 选择练习

```bash
python3 scripts/server_checkout.py list
python3 scripts/server_checkout.py set week2
python3 scripts/server_checkout.py set week3
python3 scripts/server_checkout.py set nju-a0
python3 scripts/server_checkout.py set week1 --add nju-a0
```

`week1/2/3` 是已有代码的目录编号，不是必须花三周完成的先修课。`core-a01`～`core-a08` 是按主题选题；`nju-a0`～`nju-a5` 是公开模板；`all-exercises` 检出全部练习。工具会同时包含所选练习的 `work/` 路径。

切换前提交自己的改动。使用 `set ... --dry-run` 预览；工具拒绝在完整本机仓库直接切换，避免影响日常学习目录。

## 安装与运行

回归、分类示例：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements/bootcamp.txt
python -m jupyter lab --no-browser
```

第 1 部分的小数据随代码检出，第 2/3 部分使用 sklearn 内置数据。第 3 部分另安装适合服务器的 PyTorch。依赖只装当前练习需要的部分。

NJU A0 使用公开 CPU 测试，最小依赖是 `requirements/nju-a0.txt`；其他模板按各自任务配置，不能套用 A0 环境。复制模板后再实现：

```bash
python -m pip install -r requirements/nju-a0.txt
mkdir -p work/nju-llm-2026
cp -R assignments/nju-llm-2026/a0 work/nju-llm-2026/a0
cd work/nju-llm-2026/a0
python -m pytest test_toy.py -q
```

仅在个人 A0 目录尚不存在时复制。模板有 TODO，未实现时测试失败属正常现象。仅用公开测试，自学不依赖 Classroom、学校账号或私有 `ref` 评分包。

## 保存与更新

在仓库根目录运行；示例路径替换为实际任务：

```bash
git status --short
git add -- work/nju-llm-2026/a0
git diff --cached --stat
git commit -m "study: update experiment"
git pull --rebase origin main
git push origin main
```

更新会保持所选检出范围。模型与大数据按任务获取，不存普通 Git；运行环境和输出留在服务器。完整文档检查在本机完整仓库执行，服务器只运行当前练习的检查。

旧服务器目录如果已使用 sparse checkout，先 `git pull --ff-only origin main`，再重新运行 `set <配置>`；旧的已跟踪文件会随更新删除。此前手动下载的资料和缓存不会由 Git 自动删除，确认无用后自行清理。
