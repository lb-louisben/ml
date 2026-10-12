# NJU 公开作业模板：按单元选用

[练习索引](../README.md) · [课程路线](../../course/STUDY_GUIDE.md) · [服务器教程](../../docs/SERVER_GUIDE.md)

来自 [公开作业仓库](https://github.com/NJUDeepEngine/open-llm-assignments) 的固定快照，保留原题、许可证与 [来源校验记录](SOURCES.json)。仅选当前单元的模块；不用先刷完六份作业，也不依赖学校账号、Classroom 或私有评分服务。

| 对应单元 | 模板 | 题目 |
|---|---|---|
| D1：张量与矩阵乘法，按需补练 | [A0](a0/README.md) | [tasks](a0/tasks/) |
| D3/D8：归一化与 Embedding | [A1](a1/README.md) | [tasks](a1/tasks/) |
| D2：MLP | [A2](a2/README.md) | [tasks](a2/tasks/) |
| D7：Attention | [A3](a3/README.md) | [tasks](a3/tasks/) |
| D8/L4：Transformer | [A4](a4/README.md) | [tasks](a4/tasks/) |
| L6：模型工程，进阶选用 | [A5](a5/README.md) | [tasks](a5/tasks/) |

开始时把所选模板复制到 `work/nju-llm-2026/a0/`～`a5/` 再修改。每份任务在自己的目录测试，避免同名 `src` 包冲突。A0 的 CPU 最小依赖见 [nju-a0.txt](../../requirements/nju-a0.txt)；实现后运行 `python -m pytest test_toy.py -q`。`test_with_ref.py` 使用未公开的 `ref` 包，自学跳过。

其他任务按实际源码配置依赖；原始 requirements 含 CUDA/Triton，不能在 Mac 原样全装。A5 权重与数据另行获取。未完成的 TODO 测试失败属正常现象；公开测试通过不代表官方隐藏评分。

模板不再自动同步。整套课程讲义及旧的个人 A0 已清理；`source/main/` 只保留原仓库入口与许可证用于溯源。
