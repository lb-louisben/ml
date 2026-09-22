# 测试答案与评分要点

请只在完成对应测试后打开。这里给评分要点，不替代完整推导。

## T0

1. rank=1；null space 可取 (-2,1)；不可逆。2. normal equation 使残差与 column space 正交。3. (9+3)/(9+3+1)=12/13，约 92.3%。4. 系数不唯一；在同一 column space 上的 fitted values 可以唯一。
5. 0.9×0.01 / [0.9×0.01 + 0.05×0.99]，约 15.4%。6. E[Y]=5，Var(Y)=36。7. 过拟合、泄漏/分布差异等；正则化/简化/更多数据与修正划分等，原因和措施需对应。8. 有关联不能排除混杂与反向因果。
9. 2x(wx-y)。10. gradient=8，新 w=3.2，新 f=10.24。11. p→1 时 loss→0；p→0 时 loss→∞。12. analytic gradient 与 finite-difference gradient；实现错误、步长不当、非光滑点、数值精度等。
13. 否则测试分布参与参数估计。14. accuracy≈98%，recall=0；少数正类完全漏掉。15. parameter 由训练学得，如系数/权重；hyperparameter 在训练外选择，如深度/C。16. validation overfitting 与 test contamination；train/CV 选择，冻结后单次 test。

## T1

1. 同一患者泄漏；按 patient group split，若面向未来再按时间。2. 不能，申请时不可得，是 post-outcome leakage。3. MCAR 与已观测/未观测均无关；MAR 在给定已观测变量后独立；MNAR 仍依赖缺失值本身/未观测因素，无法仅靠现有数据验证修正。4. 探索结果会影响特征/模型选择。
5. ||y-Xw||² + alpha||w||²（按约定可有常数）；alpha 增大通常 bias 上升、variance 下降。6. A 有更大的尾部/极端误差。7. 比预测均值 baseline 更差。8. drop 一类或去截距以避免完全共线；encoder 只 fit train。
9. precision=.8，recall=2/3，accuracy=.85，F1≈.727。10. 极不平衡通常 PR-AUC 更能反映正类性能，但最终按成本和阈值选。11. 一般 recall 上升、precision 下降；分数 ties、异常排序/离散输出可打破严格趋势。12. 若成本定义可信且分布相符，优先 B；还需不确定性、校准、切片和部署漂移证据。13. discrimination 是排序/区分能力；calibration 是概率与频率的一致性。
14. train error 通常降；validation 先降后升或趋平。15. bagging 并行拟合 bootstrap 后平均，主要降 variance；boosting 顺序纠错；RF 还随机抽特征。16. k 大计算高、训练集更大但 folds 相关且方差可能高；时间序列要保持时间顺序。17. 极复杂局部边界，易过拟合。18. train 学出固定投影，其他 split 只能应用；各自 fit 会改变特征空间并泄漏/失去可比性。

## T2

1. MLE theta=sum(x)/n；MAP mode 为 (sum(x)+a-1)/(n+a+b-2)，需说明边界情形。2. log posterior ratio 的二次项在共享 covariance 时抵消，留下线性项；不同 covariance 通常为 quadratic boundary。3. 特征在给定类别下独立；参数少、方差低，分类只需 posterior ordering 而非完美密度。4. 判别式学 p(y|x) 或边界，如 logistic；生成式学 p(x|y)p(y) 或 joint，如 GDA/NB。
5. 目标为 1/2||w||² + C sum xi，约束 y_i(wᵀx_i+b)≥1-xi、xi≥0；各项解释完整。6. 用内积替代显式高维映射；Gram 应对称 positive semidefinite。7. early stopping、regularization/dropout、augmentation/更多数据、减小容量等，需解释机制。8. 分别为样本平均损失、真实分布期望损失、样本损失加复杂度惩罚。9. 多重比较选择噪声极值；inner 选择、outer 估计，或保留一次性 test。
10. assignment 到最近 centroid；更新为簇均值；仅收敛到局部解，多初始化。11. E 计算 latent responsibilities 的 posterior；M 最大化 expected complete log likelihood；每步优化下界/坐标上升使观测 likelihood 不减。12. 投影到前 k eigenvectors 最大化保留方差，也最小化 rank-k squared reconstruction error。13. 低方差但区分类别的方向可能被丢弃，且非线性结构不保留。
14. V*(s)=max_a [R(s,a)+gamma sum P(s'|s,a)V*(s')]；反复用 Bellman backup 更新。15. 先核验样本/标签/阈值/置信区间，再分群与交叉因素审计，和利益相关者沟通代价，未达到门槛则不部署或限定使用并监控。16. 数据版本/划分、预处理、metric 实现、seed、超参数、checkpoint、软件硬件数值、论文未写细节；顺序合理即可。

## T3

评分者关注四件事：定义准确；能说清因果机制；能给反例或适用边界；能把概念落到可观测指标。白板题必须分开评价 retrieval 与 generation，包含 unanswerable set、citation 检查、人工抽样、版本记录、隐私/注入风险和可回滚门槛。只堆技术名词不给实验协议，最高 60%。
