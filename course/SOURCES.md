# 官方公开材料与来源索引

最后核对日期：2026-09-21。官方公开材料已下载到 [library/](../library/README.md)，按课程与学期保存原件；文件目录、原始 URL、下载日期、大小和 SHA256 见 [manifest](../library/manifest.json)。本页保留课程背景及外部更新入口。

## 核心来源

| 来源 | 层次与用途 | 公开内容 | 本路径如何采用 |
|---|---|---|---|
| [MIT 18.06SC Linear Algebra](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/) | 本科数学先修 | 视频、讲义、题目、答案、考试；OCW 页面标注 Creative Commons | Phase 1 主线，选做投影、最小二乘、特征值、SVD |
| [UC Berkeley Data 100 SP25](https://ds100.org/sp25/) | 本科数据科学 | 课程表、讲义、lab、homework、exam prep；部分平台需账户 | Phase 2 数据生命周期与 EDA 主线 |
| [Data 100 Course Notes](https://ds100.org/course-notes/) | 本科教材 | 可直接阅读的课程讲义 | Data 100 链接受限时的首选替代 |
| [ISLP](https://www.statlearning.com/) | 本科统计学习 | Python 版教材、章节实验与配套资源 | Phase 2 回归、分类、重采样、树、SVM、无监督 |
| [UC Berkeley CS189 SP25](https://people.eecs.berkeley.edu/~jrs/189/) | 高年级本科/研究生 ML | 完整讲义、历年期中/期末及解答；视频有的需 bCourses | Phase 2～3 理论、限时测试 |
| [Stanford CS229 Fall 2025](https://cs229.stanford.edu/index.html-fall25) | 研究生 ML | 课程顺序、讲义/复习入口、problem set 与 project 节奏 | Phase 3 的知识顺序与项目结构 |
| [Stanford Engineering Everywhere CS229](https://see.stanford.edu/Course/CS229) | 经典研究生 ML 档案 | 20 讲视频、讲义、4 套题与答案 | 无法访问当期材料时补充；明确标为旧版 |
| [UC Berkeley CS182 SP21](https://cs182sp21.github.io/) | 高年级本科/研究生 DL | 公开视频、讲义、discussion、homework、practice midterm | Phase 4 理论与讨论题 |
| [Stanford CS231n 2025](https://cs231n.stanford.edu/2025/) | 研究生视觉/DL | slides、notes、3 个公开 assignment、project 说明 | Phase 4 实现与消融训练 |
| [Stanford CS224N Winter 2025](https://web.stanford.edu/class/archive/cs/cs224n/cs224n.1254/) | 研究生 NLP/LLM | slides、notes、4 个作业、项目材料；视频有公开历史版 | Phase 5 主线与 Capstone 节奏 |
| [UC Berkeley CS188 AI Materials](https://ai.berkeley.edu/home.html) | 本科 AI | Pacman projects、讲义、section、历年考试 | Phase 3 的 MDP/RL 可选实践 |
| [UC Berkeley CS285](https://rail.eecs.berkeley.edu/deeprlcourse/) | 研究生 Deep RL | slides、5 个 homework、project outline | 只作为 Phase 3 后的方向分叉 |

## 可直接使用的官方作业与考试

优先打开 [本地逐主题文件索引](READING_LIST.md)，其中直接链接讲义、作业、考试与解答。Data 100、CS224N、CS231n 和部分 CS182 发布包已解压，可从各课程目录打开 Notebook。原课程网页用于查更新和观看尚未归档的视频。

- Data 100：从 [SP25 schedule](https://ds100.org/sp25/) 进入 lab、homework 与 exam prep。部分 Datahub 或 Gradescope 环节可能需要登录；遇到限制就做本仓库 A02～A04，不寻找非官方转载。
- CS189：课程主页列出多年份无答案与有答案的 midterm/final。计时先做“without solutions”，交卷后再核对对应解答。
- CS231n：[2025 assignments](https://cs231n.stanford.edu/2025/assignments.html) 包含 A1（kNN、Softmax、全连接网络）、A2（归一化、CNN、RNN）和 A3（Transformer、自监督、diffusion、CLIP/DINO）。
- CS224N：Winter 2025 课程页链接 A1～A4 的 code/handout，覆盖 word vectors、神经网络基础与 parsing、seq2seq/attention、Transformer fine-tuning。
- MIT 18.06SC：课程自带 problem sets、problem-solving videos、exams 和 solutions，适合完整自学闭环。
- 经典 CS229：SEE 档案提供 Problem Set 1～4 及 solution。它们是旧版公开材料，不代表 Fall 2025 当期作业。

## 本地教材与来源映射

本地章节是重新组织、重写并加入例题与自测后的原创学习材料，不是对校方文本的逐句翻译。

| 本地材料 | 主要课程结构参考 |
|---|---|
| [01 线性代数](materials/01_linear_algebra.md) | MIT 18.06SC；CS229 线性代数复习 |
| [02 概率](materials/02_probability_statistics.md) · [03 优化](materials/03_calculus_optimization.md) | CS229 概率复习、线性/逻辑回归与优化主题；CS182 优化/反传单元 |
| [04 数据设计](materials/04_data_and_experiment_design.md) | Berkeley Data 100 的 data lifecycle、cleaning、EDA 与建模流程 |
| [05～09 经典 ML](materials/05_linear_models.md) | ISLP Python、Berkeley CS189、Stanford CS229 的主题顺序 |
| [10～11 深度学习](materials/10_neural_networks_and_backprop.md) | Berkeley CS182；Stanford CS231n |
| [12～13 Transformer/LLM](materials/12_embeddings_and_transformers.md) | Stanford CS224N Winter 2025 |
| [14 RL、责任与复现](materials/14_rl_responsibility_and_research.md) | CS229 的 RL/公平主题；Berkeley CS285 的 MDP 与实验结构 |

每章只保留理解该主题所需的核心范围；需要完整证明、大量题目或教授原始讲解时，再访问上方官方页面。

## 选择原则

1. 课程主页与讲义优先于二手博客；论文优先原论文或官方 proceedings。
2. 同一主题只设一条主线，其他材料只补洞，避免收藏代替学习。
3. 官方答案只用于提交后的复盘；公开不等于可以不注明来源。
4. 若链接失效，先从课程的 Previous Offerings 找稳定档案，不从答案聚合站下载。
5. 课程时间、作业内容、开放权限会变化；本路径引用的是上表具体版本，不声称与最新在校课程完全一致。

返回：[完整路径](README.md)
