# A08：RAG 的检索与答案评价

来源类型：本仓库自制；参考 Stanford CS224N 的 RAG/agent/evaluation 单元。只选与当前单元有关的题，不要求整份完成。

## 目标

建立一个小而可测的语义检索或 RAG 系统。重点是评价，不要求付费 API；可以只做 retrieve-and-display，也可用本地小模型生成答案。

## 数据

选择 20～100 篇有明确许可的文档，自己编写至少 40 个问题及 gold evidence。问题分 factual、multi-hop、unanswerable 三类；先冻结测试题，再调系统。

## 任务

1. baseline：关键词/BM25 或 TF-IDF 检索。
2. dense retrieval：选择一个公开 embedding 模型，记录版本与许可。
3. 比较 chunk size、overlap、top-k 中至少两个因素。
4. 检索指标：Recall@k、MRR 或 nDCG 至少两个。
5. 生成时增加引用；答案指标至少包含 correctness、faithfulness、citation precision/recall 中的两个。
6. unanswerable 问题必须允许拒答，报告错误接受率。
7. 做 10 个失败案例的 taxonomy：检索失败、切块失败、证据冲突、生成幻觉、问题歧义等。
8. 报告延迟、索引大小和每次查询成本（即使成本为 0）。

## 实验纪律

不要用同一个模型自动生成 gold、回答问题并给自己评分作为唯一评价。至少 20 个测试问题由人工核对；任何 LLM judge 都要报告 prompt、模型版本和已知偏差。

提交 corpus_manifest.csv、questions.jsonl、retriever/、eval.py、results.csv、error_analysis.md、README.md。
