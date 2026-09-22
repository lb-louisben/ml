# 项目目录与文件归属

[返回项目首页](../README.md) · [技术文档](README.md)

## 放置规则

| 内容 | 位置 |
|---|---|
| 项目总览、快速跳转、启动方法 | 根目录 `README.md` |
| 学习顺序、进度、评分与来源说明 | `course/` |
| 第一、二、三部分入门内容 | `course/bootcamp/week1/`、`week2/`、`week3/` |
| 入门配套数据、参考项目 | 所属课程内部，如 `course/bootcamp/week1/data/` |
| 中文教材、作业、测验、项目要求 | `course/materials/`、`assignments/`、`tests/`、`projects/` |
| 学校原版材料 | `library/<课程与学期>/` |
| 自己的独立实验与项目实现 | `work/<任务名>/` |
| 环境和维护说明、历史记录 | `docs/`；环境指南和测试集中在 `docs/setup/` |
| 下载、索引和验证脚本 | `scripts/` |

根目录保留总入口和项目级依赖文件。课程内容归入 `course/`，同一系列的周目录保持同级。

## 当前运行约定

从项目根目录启动 `.venv` 和 JupyterLab。Week 1 Notebook 会向上查找包含 `course/bootcamp/week1/data/` 的项目根目录，因此也能从各自日目录运行。输出位于该课程的 `outputs/`，由 Git 忽略。

Week 2/3 的带练教程位于各周目录，材料解释和示例代码整合在 Notebook 中；Week 3 共用 `numpy_mlp.py`。演示产物和执行副本保存到各周 `outputs/`，自己的独立练习放在 `work/`。PyTorch 使用 `.venv-dl`，配置见 [深度学习环境](setup/DEEP_LEARNING.md)。

`library/manifest.json` 记录原始 URL、来源页面、下载状态、大小、SHA256 和获取日期。ZIP 原件与已解压的 `unpacked/` 按课程保存；要修改作业时复制到 `work/`，依赖与额外数据按包内 README 准备。

下载资料运行 `python3 scripts/download_courses.py`，随后运行 `python3 scripts/build_library_catalog.py` 重建索引。下载器会复用已有下载并重试失败项，不会安装或执行课程代码。

## 迁移记录

2026-09-21：

- 将原 `curriculum/` 归入 `course/`，原 `week2/`、`week3/` 归入 `course/bootcamp/`。
- 将原根目录 `week1/` 整体移入 `course/bootcamp/week1/`，包括现有笔记、数据与输出；更新 Notebook 数据路径、验证脚本、Git 忽略规则和文档链接。
- 将环境说明与原根目录 `00_环境测试.ipynb` 集中到 `docs/setup/`，Git 和技术说明集中到 `docs/`。
- 根目录 `README.md` 作为项目使用指南和快速导航；个人独立实验统一使用 `work/`。
- 原 53 周规划保存在 [历史记录](archive/learning-plan-53-weeks.md)。当前学习安排见 [学习指南](../course/STUDY_GUIDE.md)。

迁移脚本为 `scripts/reorganize_learning.py`；当前目录下重复执行会直接退出，不重复搬移。
