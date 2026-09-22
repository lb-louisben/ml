# 12：Embedding、Attention 与 Transformer

目标：理解离散 token 如何变成向量；手算 scaled dot-product attention；解释 multi-head、mask、position、residual 和 normalization；实现小型 Transformer。

## 1. Token 与 embedding

one-hot 向量只表示身份，维度等于词表大小。Embedding matrix E 的一行是 token 的稠密向量；查表等价于 one-hot 乘 E。向量距离来自训练目标和数据，不保证自动等于人类语义，也可能编码偏差。

tokenization 决定序列长度、词表和跨语言成本。相同文本在不同 tokenizer 下不能直接比较 token 数。

Word2vec 的 skip-gram 目标用中心词预测上下文词，使经常处于相似上下文的词得到相似向量。完整 softmax 对大词表昂贵，negative sampling 把任务近似成区分真实词对与噪声词对。Embedding 的结构因此依赖窗口、采样分布、语料和目标。

## 2. Q、K、V

输入 X 经过三个投影得到 Q=XW_Q、K=XW_K、V=XW_V。每个 query 与所有 key 做相似度，再对 value 加权：

    Attention(Q,K,V) = softmax(QKᵀ / sqrt(d_k)) V

除以 sqrt(d_k) 是因为维度增大时点积方差增大，softmax 容易饱和，gradient 变小。

## 3. Mask

- Causal mask：位置 t 看不到未来 token，用于自回归生成。
- Padding mask：忽略补齐位置。
- 任意 attention mask：按任务限制连接。

mask 应在 softmax 前把禁用 logit 设为极小值；softmax 后相应概率为 0。

## 4. Multi-head 与 position

多个 head 在不同投影子空间中建立关系，拼接后再投影。更多 head 不保证更好；固定模型维度时每个 head 维度变小。

Self-attention 本身对输入顺序没有足够区分，需要 absolute、relative 或 rotary 等位置表示。没有位置，交换 token 的顺序主要只会交换输出位置，难以表达先后语义。

## 5. Transformer block

典型 block：attention + residual + normalization，再接 position-wise feed-forward + residual + normalization。Residual 提供短路径，帮助 gradient 流动；LayerNorm 稳定每个 token 的特征尺度。

训练 language model 时，输入前缀预测下一 token，损失为每个有效位置的 cross-entropy。Perplexity=exp(平均 NLL)；只可在相同 tokenizer、语料和处理协议下公平比较。

## Worked example

若一个 query 与两个 key 的 scaled scores 为 [0, ln 3]，softmax 权重为 [1/4, 3/4]。输出是 0.25V1+0.75V2。它表示模型在该 head/层/位置更依赖 V2，但不能自动当作完整因果解释。

## 常见错误

- mask 在 softmax 后才应用且未重新归一化。
- 忘记除 sqrt(d_k)。
- 把 attention weights 直接称为模型解释。
- 用不同 tokenizer 的 perplexity 横向排名。
- 训练时把 padding token 计入 loss。

## 自测

1. embedding lookup 与 one-hot×matrix 有何关系？
2. 为什么 QKᵀ 要缩放？
3. causal 与 padding mask 各防什么？
4. 没有 position 信息会失去什么？
5. perplexity 降低为何不保证任务质量提高？

答案要点：数学等价；控制点积方差/softmax 饱和；未来泄漏与无效 padding；顺序；目标/分布与真实任务不一致。

配套：[A07](../assignments/A07_transformer_from_scratch.md) · [T3](../tests/T3_dl_llm_oral.md)
