# 本项目 Git 使用

本地仓库已初始化，默认分支 `main`。初次提交保存已有笔记；后续提交加入教材。
远程 `origin` 为 `git@github.com:lb-louisben/ml.git`，本机默认推送到这个自己的仓库。

NJU 的资料同步、作业与推送操作统一见 [NJU 课程总入口](../library/nju-llm-2026/README.md#同步与保存)。

## 推送自己的仓库

自己的改动完成提交后：

```bash
git push
# 首次推送并建立 main 的上游跟踪：
git push -u origin main
```

`git push` 的目标是自己的仓库。建立上游后，`git pull` 同步自己的提交；老师资料使用独立同步命令，不通过 `git pull` 混入本项目。资料同步的文件位置与规则见 [NJU 课程入口](../library/nju-llm-2026/README.md)。

## 每天学习结束

先保存 Notebook，再在项目根目录运行：

```bash
git status
git diff --stat
git add assignments/bootcamp/week1/day3/03_Pandas_data_cleaning.ipynb
git diff --cached --stat
git commit -m "study: complete day 3 pandas exercises"
```

下一天替换对应路径。只暂存确认要保存的文件；虚拟环境、缓存、检查点、outputs、.env 已排除。
NJU 讲义在 `library/`，作业在 `assignments/nju-llm-2026/`，个人实现放 `work/`，三类内容均由 Git 保存。
其他学校原始资料和网页快照存放在 GitHub Releases；Git 保存索引、来源和归档校验清单。完整恢复用 `python3 scripts/library_archive.py restore --all`，随后按需运行目录生成器；服务器只选作业，见 [服务器教程](SERVER_GUIDE.md) 和 [存储方案](GITHUB_STORAGE.md)。
本机 Git 简写与推送配置不随仓库克隆，Python 同步命令可直接使用。
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
远程地址已配置；提交和推送由你按学习进度执行。
