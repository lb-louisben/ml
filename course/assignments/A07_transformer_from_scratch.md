# A07：从零实现 Self-Attention

来源类型：本仓库自制；参考 Stanford CS224N 的 attention/Transformer 单元与 CS231n A3。预计 10～14 小时，100 分。

## 任务

1. 手算 3 个 token、2 维向量的 Q、K、V、scaled dot-product attention 和输出。
2. 只用基础 PyTorch tensor 操作实现 single-head attention，不调用 MultiheadAttention。
3. 扩展到 multi-head、causal mask、padding mask、residual、LayerNorm、position encoding。
4. 为每个组件写 shape test；mask 后概率必须为 0，非 mask 行概率和为 1。
5. 构建一个小型 character-level 或 token-level language model，在小语料上训练。
6. 与 unigram/bigram baseline 比较 validation perplexity。
7. 做至少两个消融：去掉 positional encoding、改变 head 数、改变 context length 三选二。

## 必答题

- 为什么除以 sqrt(d_k)？
- causal mask 和 padding mask 各防止哪类错误？
- 没有位置编码时，模型丢失什么信息？
- attention weights 为什么不一定是可靠解释？
- 训练 perplexity 下降而生成质量变差，可能有哪些原因？

## 资源限制

模型参数建议 < 10M，单次训练目标 < 30 分钟。分数来自正确性、实验和解释，不来自大模型效果。

提交 src/model.py、tests/、train.py、config、results.json、report.md。
