# 14：强化学习基础、责任型 ML 与研究复现

目标：理解 MDP 与 Bellman backup；能审计群体风险、隐私和解释；按照可证伪假设组织复现实验。

## 1. MDP

Markov Decision Process 包含 state S、action A、transition P(s'|s,a)、reward R、discount gamma。Markov 假设是：给定当前 state/action，未来与更早历史无关。若 state 没包含必要历史，这个假设不成立。

Policy pi(a|s) 规定行动；return 是折扣奖励之和。state value V^pi(s) 是从 s 开始遵循 policy 的期望 return；action value Q^pi(s,a) 还固定第一步 action。

## 2. Bellman 与动态规划

Bellman optimality equation：

    V*(s) = max_a [R(s,a) + gamma sum_s' P(s'|s,a)V*(s')]

Value iteration 反复应用右侧 backup 直到收敛，再取 greedy policy。Policy iteration 在 policy evaluation 与 policy improvement 间交替。模型已知且状态有限时可精确动态规划；深度 RL 处理的是函数逼近、未知环境和采样带来的额外困难。

## 3. RL 的评价陷阱

离线数据只覆盖 behavior policy 访问的区域，新 policy 的反事实回报难估计。Simulator 结果依赖模型真实性。多 seed 尤其重要，因为训练和环境都随机。必须报告 return 分布、失败率、样本效率和安全约束，而不只最高回报。

## 4. 群体评价与公平

常见群体指标包括 demographic parity、equal opportunity（相等 TPR）、equalized odds（相等 TPR/FPR）和 calibration。它们在 base rate 不同时通常不能同时满足；选择指标是价值和应用问题，不只是数学选择。

审计顺序：核验群体字段与样本量；检查标签/测量偏差；报告总体与交叉 slice；加入区间；测试阈值和漂移；与受影响人群/领域专家讨论代价。公平指标差异不是自动的因果结论。

## 5. 解释与因果边界

Feature importance、SHAP、attention 等通常解释模型输出对输入的关系，不说明改变现实变量会造成什么结果。相关特征会分摊/替代重要性；解释工具也会随背景分布、模型和参数改变。

在报告中区分：global behavior、local explanation、data association、causal effect。没有识别假设和合适设计时，不声称因果。

## 6. 隐私与安全

最小化收集和保留；分离直接标识符；控制访问与日志；明确删除和用途。去掉姓名并不保证匿名，高维准标识符仍可重识别。模型可能记忆训练样本或泄露成员信息，敏感任务需 threat model 和专门测试。

## 7. 研究复现

先写 falsifiable claim，例如“在固定训练预算下，方法 M 使 validation F1 平均提升至少 2 点”。冻结数据、metric、seed 和 checkpoint 规则；先建立作者方法以外的简单 baseline；记录环境与每次运行；报告 mean/std、失败和不可比项。

复现差距依次排查：数据/split、预处理、metric、seed、超参数、optimizer/schedule、batch、train/eval、checkpoint、软件/硬件数值。不要用不断改协议直到接近论文数字的方式制造复现。

## Worked example

总体 AUC 提升，但一个小群体 FNR 翻倍。先核查该群体样本量和标签质量，给区间并检查阈值；再比较相同 operating point、交叉群体和时间稳定性。若伤害真实且无缓解，不能用总体提升直接覆盖，应限制部署或停止。

## 自测

1. V 与 Q 的差别？
2. Value iteration 的一次 backup 在做什么？
3. 为什么离线 RL 的新 policy 难评价？
4. 为什么多个公平指标可能冲突？
5. 复现前必须冻结哪些内容？

答案要点：是否固定第一步 action；用一步 reward 加未来最优价值更新；缺少新 action 的覆盖与反事实；base rate 与错误率约束不兼容；数据/split、metric、seed、预算和选择规则。

配套：[T2](../tests/T2_graduate_ml_final.md) · [P2](../projects/P2_deep_learning_reproduction.md) · [Capstone](../projects/CAPSTONE.md)
