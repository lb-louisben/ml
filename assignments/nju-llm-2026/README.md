# NJU 2026 · 作业

[全部作业](../README.md) · [服务器教程](../../docs/SERVER_GUIDE.md) · [课程讲义与本机环境](../../library/nju-llm-2026/README.md)

模板来自 [官方公开作业仓库](https://github.com/NJUDeepEngine/open-llm-assignments) 的一次性分支快照。来源记录中的原始路径和校验值保留在 [SOURCES.json](SOURCES.json)，`local_roots` 记录现在的目录位置。日常同步只补充讲义，不刷新这些模板。

| 作业 | 内容 | 题目 | 模板说明 |
|---|---|---|---|
| A0 | MatMul with Importance | [tasks](a0/tasks/) | [README](a0/README.md) |
| A1 | Norm + Embedding | [tasks](a1/tasks/) | [README](a1/README.md) |
| A2 | MLP | [tasks](a2/tasks/) | [README](a2/README.md) |
| A3 | Attention | [tasks](a3/tasks/) | [README](a3/README.md) |
| A4 | Transformer | [tasks](a4/tasks/) | [README](a4/README.md) |
| A5 | Exploring Llama | [tasks](a5/tasks/) | [README](a5/README.md) |

从项目根目录复制对应模板后修改，已有目录会保留：

```bash
mkdir -p work/nju-llm-2026
if [ ! -e work/nju-llm-2026/a0 ]; then
  cp -R assignments/nju-llm-2026/a0 work/nju-llm-2026/a0
fi
```

当前 A0 学习实现已放在 `work/nju-llm-2026/a0/src/functional.py`，保存原有代码；`assignments/` 中的 A0 恢复为原始 TODO 模板。当前实现是否完成，以自己运行公开测试及题目要求为准。

每份作业在自己的目录单独测试，避免不同作业的同名 `src` 包冲突。A0 最小依赖见 `requirements/nju-a0.txt`；其他作业依赖以各自模板的 `requirements.txt` 为准。A5 的模型与训练数据按题目另行获取，权重、运行输出和环境目录不进 Git。
