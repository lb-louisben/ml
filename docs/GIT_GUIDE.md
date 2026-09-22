# 本项目 Git 使用

本地仓库已初始化，默认分支 `main`。初次提交保存已有笔记；后续提交加入教材。
没有远程地址，当前提交仅存于这台电脑。

## 每天学习结束

先保存 Notebook，再在项目根目录运行：

```bash
git status
git diff --stat
git add course/bootcamp/week1/day3/03_Pandas_data_cleaning.ipynb
git diff --cached --stat
git commit -m "study: complete day 3 pandas exercises"
```

下一天替换对应路径。只暂存确认要保存的文件；虚拟环境、缓存、检查点、outputs、.env 已排除。
`library/` 各课程目录中的原始资料、网页快照和解压副本也已忽略，仅保留课程 `README.md` 索引；资料库总索引、`manifest.json` 来源清单及下载脚本仍提交。忽略不会删除本地文件。
新克隆的仓库不含这些资料，需要在项目根目录运行 `python3 scripts/download_courses.py`，再运行 `python3 scripts/build_library_catalog.py` 下载并解压后，才能打开索引中的本地资料链接。
Notebook 是 JSON，单元输出也可能造成大量差异。可以在编辑器 Clear All Outputs 后保存再提交，但先确认不需要保留输出。不要随便清除自己的学习记录。

## 查看历史与比较

```bash
git log --oneline --decorate -10
git show --stat HEAD
git diff
```

查看某个旧版本文件可用 `git show 提交号:相对路径`，不会覆盖工作文件。

## 可选：独立实验分支

```bash
git switch -c experiment/ridge
```

分支适合尝试新模型。已有未提交修改时先保存并提交，避免混淆实验。
需要 GitHub 备份时再决定远程仓库、可见性和推送；本次没有自动发布。
