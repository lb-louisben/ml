# NJU 2026 · 我的学习记录

[个人练习总览](../README.md) · [课程、题目与环境](../../library/nju-llm-2026/README.md) · [老师全部讲义](../../library/nju-llm-2026/LECTURES.md)

本目录保存个人修改、笔记和作业实现。老师资料和固定作业模板位于 `library/nju-llm-2026/`。

| 讲次 | 我的文件 | 老师原件 |
|---|---|---|
| 1 · 课程简介 | [本地模型 Notebook](lecture1.ipynb) | [讲义](../../library/nju-llm-2026/2026/lecture1.md) |
| 2 · 特征空间的变换 | [个人讲义](lecture2.md) | [讲义](../../library/nju-llm-2026/2026/lecture2.md) · [Notebook](../../library/nju-llm-2026/2026/notebook/lecture2.ipynb) |
| 3 · 反向传播 | [学习 Notebook](lecture3.ipynb) | [讲义](../../library/nju-llm-2026/2026/lecture3.md) |
| 4 · 大语言模型解析 I | [本地模型 Notebook](lecture4.ipynb) | [讲义](../../library/nju-llm-2026/2026/lecture4.md) |

在项目根目录执行 `bash scripts/start_nju.sh` 启动环境。模型配置和验证方法统一见课程入口；运行输出位于 `.cache/nju-validation/`。

个人讲义复用资料库中的图片，使用相对路径 `../../library/nju-llm-2026/images/`；移动或复制讲义后需要重新核对图片引用。

作业从 [独立模板目录](../../assignments/nju-llm-2026/README.md) 复制到本目录的 `a0/`～`a5/` 后再修改，并在各自目录运行公开测试。开始时再创建目录；每份作业记录运行方式、结果和引用。已有学习内容继续保留在原文件中。

已有 [A0 学习实现](a0/src/functional.py) 已从原件目录转存；完整原有代码保留，题目与公开测试一并保存，是否完成以实际验证为准。
