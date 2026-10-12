# 07：决策树与集成学习

目标：理解树如何分裂；区分 bagging 与 boosting；诊断深度、叶子大小和数据泄漏；公平比较训练效果与成本。

## 1. k-Nearest Neighbors

kNN 不显式拟合参数：预测时寻找训练集中距离最近的 k 个样本并投票/平均。k 小时边界灵活、variance 高；k 大时更平滑、bias 高。距离对尺度和无关维度敏感，所以数值特征通常要标准化，高维中还会出现 distance concentration。

## 2. 决策树

树递归选择 feature 和 threshold，把数据分到更纯或更低误差的子节点。分类常用 Gini/entropy，回归常用 squared error。树能自动表达非线性和交互，也不要求特征缩放。

深树的 train error 往往持续下降，但叶子样本很少时 variance 高。主要控制项包括 max_depth、min_samples_leaf、max_leaf_nodes 和 pruning。

## 3. Bagging 与 Random Forest

Bagging 在 bootstrap 样本上并行训练多个高 variance 模型，再平均/投票，主要降低 variance。Random Forest 还在每个节点只看随机特征子集，降低树之间相关性，使平均更有效。

OOB 样本可用于内部估计，但不能替代最终独立测试集，尤其在 group/time 依赖数据上。

## 4. Boosting

Boosting 顺序添加弱学习器，每一步修正当前模型的残差或负梯度。常见控制项：n_estimators、learning_rate、tree depth/leaves、subsample。小 learning rate 通常需要更多树。

Boosting 很强，但对错误标签、目标泄漏和不当 validation 同样敏感。更高分不代表实验更可信。

## 5. Feature importance

Impurity-based importance 可能偏好高基数或有更多切点的特征。Permutation importance 衡量打乱某特征后性能下降，但相关特征会互相替代。SHAP 等解释工具描述模型行为，不自动给因果效应。

## Worked example

max_depth 从 2 增至 50：train error 通常单调下降；validation error 常先下降后上升或趋平。最佳深度应通过 CV/validation 选，不看 test。

## 常见错误

- 对一个时间序列使用随机 CV，再称模型能预测未来。
- 只报告单个 seed 的森林结果。
- 把 feature importance 当作变量真实影响。
- 调了大量超参数却仍用同一 validation 分数作无偏结果。
- 比较模型时预处理、split 或 metric 不同。

## 自测

1. kNN 中 k 增大通常如何改变 bias 与 variance？
2. Bagging 为什么能降低 variance？
3. Random Forest 为什么随机选特征？
4. boosting 中 learning_rate 与树数量有什么关系？
5. 树为何通常不需要标准化？
6. 两个高度相关特征对 permutation importance 有何影响？

答案要点：bias 上升、variance 下降；平均弱相关误差；降低树间相关；小步长通常需更多轮；分裂依赖排序/阈值而非尺度；互相替代导致单个重要性低估。

当前练习与掌握标准统一见 [课程路线](../STUDY_GUIDE.md)。
