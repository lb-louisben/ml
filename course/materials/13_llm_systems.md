# 13：预训练、微调、RAG 与 Agent

目标：区分 LLM 生命周期中的不同环节；能为问题选择 prompting、RAG、PEFT/微调或 agent；为系统建立离线评价、引用、拒答和监控。

## 1. Pretraining 与 post-training

Pretraining 从大规模语料学习 next-token 或 masked-token 目标，得到通用表示和生成能力。SFT 用任务示范调整行为。Preference optimization（如 RLHF/DPO 家族）利用偏好数据改变回答排序与风格。它们会影响模型参数，但不保证精确、可追踪地写入事实。

PEFT 只训练少量新增/低秩参数，降低训练与存储成本；仍需要高质量数据、评价和版本管理。

## 2. Prompt、RAG、fine-tuning 的选择

- Prompt/workflow：任务规则可用上下文表达，先作为最低成本 baseline。
- RAG：知识经常更新、需要引用或来自私有文档；知识主要放在外部索引。
- Fine-tuning/PEFT：需要稳定改变格式、领域行为或任务策略，有足够训练样本。
- 组合：RAG 提供事实，fine-tuning 改善使用证据的行为。

不要默认微调是“教模型记住所有新资料”，也不要默认 RAG 能修复推理、指令遵循或生成幻觉。

## 3. RAG pipeline

Ingestion：解析、清洗、分块、元数据与版本。Index：sparse/dense/hybrid。Retrieve：query 处理、top-k、过滤、rerank。Generate：把证据与指令传入模型，要求引用与拒答。Evaluate：分别测 retrieval 和 answer。

检索指标：Recall@k、MRR、nDCG。答案指标：correctness、faithfulness、citation precision/recall、拒答准确率。还要报告 latency、成本和索引大小。

高 Recall@k 但答案差，可能因为生成器忽略证据、chunk 含噪、证据冲突、context 排序/长度问题或 prompt 不允许拒答。

## 4. Agent 与 workflow

Workflow 的步骤由程序预先定义；agent 让模型动态选择工具和下一步。任务路径可预知时，固定 workflow 更易测试、更便宜、更安全。只有需要根据中间观察动态规划时才增加 agent 自主性。

Agent 风险包括 prompt injection、越权工具调用、循环、不可预测成本、错误累积和数据外泄。工具应最小权限，写操作需验证/确认，设置步数和预算上限，并保留 trace。

## 5. 评价设计

测试集至少包含正常、边界、对抗、无答案和分布外问题。不要让同一模型生成 gold、回答并作为唯一裁判。LLM-as-judge 可扩展，但要固定 prompt/版本，校准到人工样本，检查位置、长度和风格偏差。

上线门槛应预先定义：核心质量、危险错误率、拒答、引用、延迟、成本、隐私。上线后监控输入 drift、检索空结果、citation failure、工具错误和用户纠正。

## Worked example

课程资料问答需要内容更新和原文引用，优先 RAG：文档按标题/段落切块，保留文件与页码元数据；构造有答案和无答案集；先测 Recall@k，再测引用支持率。若主要失败是固定格式不稳定，再考虑 PEFT，而不是先微调事实。

## 常见错误

- 只展示几个成功对话，不建立冻结测试集。
- 只测最终答案，不知道失败来自 retrieval 还是 generation。
- 没有 unanswerable 问题，无法测幻觉与拒答。
- 把 agent 用于完全可预测的两步流程。
- 不记录模型、embedding、index 和 prompt 版本。

## 自测

1. RAG 与 fine-tuning 的知识更新路径有何不同？
2. 为什么必须分开评价 retrieval 与 generation？
3. Recall@5=1 仍可能答错的原因？
4. 固定 workflow 何时优于 agent？
5. 为什么 LLM judge 不能是唯一评价者？

答案要点：外部上下文与参数更新；定位失败并避免指标抵消；证据噪声/冲突/忽略/生成错误；路径可知且要求可靠可审计；存在共同偏差、自评和版本漂移。

当前练习与掌握标准统一见 [课程路线](../STUDY_GUIDE.md)。
