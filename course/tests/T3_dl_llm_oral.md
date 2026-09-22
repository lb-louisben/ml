# T3：深度学习与 LLM 口试

45～60 分钟，100 分。请学习伙伴提问并追问；独学时录音，不看笔记回答。每题先用 90 秒给核心答案，再接受追问。

## 问题池

随机抽 8 题，每题 10 分；最后用 20 分完成白板设计题。

1. 反向传播是在做什么？它与 gradient descent 有何区别？
2. 为什么深层网络容易出现梯度消失/爆炸？residual、normalization、初始化分别如何帮助？
3. train/eval mode 会改变哪些常见层？忘记切换会产生什么现象？
4. CNN 的 inductive bias 是什么？它与全连接网络相比为何更适合图像？
5. embedding 与 one-hot 的关系是什么？embedding 中“距离近”一定代表语义相似吗？
6. 从 Q、K、V 解释 self-attention；为什么要除以 sqrt(d_k)？
7. causal mask、padding mask 和 attention mask 有何区别？
8. Transformer 没有 recurrence，如何表达顺序？
9. pretraining、SFT、PEFT、RLHF/DPO 分别改变什么？
10. fine-tuning 与 RAG 的知识更新路径有何不同？何时组合？
11. RAG 中 Recall@k 很高但答案仍幻觉，可能有哪些原因？
12. 为什么不能只用另一个 LLM 自动评价 LLM 系统？如何建立较可信的评价？
13. agent 与固定 workflow 的边界是什么？增加 agent 自主性带来哪些风险？
14. 模型 perplexity 降低是否保证用户任务改善？举反例。
15. 训练数据、benchmark、部署流量不同分布时如何监控 drift？

## 白板设计题（20 分）

设计一个“课程资料问答系统”。要求：只根据给定材料回答；答案必须引用来源；遇到无答案问题应拒答；预算有限。画出 ingestion、index、retrieval、generation、evaluation、monitoring，并说明离线数据集、核心指标、三个失败模式和上线门槛。

## 评分

每个口答题：定义 3、机制 3、例子/边界 2、面对追问 2。白板题：架构 5、评价 7、安全与失败 5、取舍 3。总分 ≥70 且白板题 ≥12 才通过。

口试者只依据 [评分要点](SOLUTIONS.md#t3) 追问，不应照读答案。
