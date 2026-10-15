# 文献筛选与证据范围

检索与读取日期：2026-10-15。以下只使用原论文、作者预印本和出版方页面；搜索摘要用于导航，不代替正文。以下为历史阅读范围，公开整理时未重新下载论文。

1. **Wei Zhang, Asymptotic Analysis of Multiscale Markov Chain, arXiv:1512.08944v2（2016-01-27）。**
   原文：https://arxiv.org/abs/1512.08944v2 。历史阅读范围：§1.1，§2.2，Appendix B。原文给出快块内/慢块间生成矩阵分解、约化链及后向方程分析。PDF 的 Theorem 2.1 对应 HTML 的 Theorem 1，假设整个链可逆；不能把其定理直接套到本单元的吸收链。这里沿用标准平均化结构，另行展示有限矩阵恒等式及其保守界；不声称重新发现平均化或其误差阶。

2. **George Yin and Hanqin Zhang, Singularly perturbed Markov chains: Limit results and applications, Annals of Applied Probability 17(1), 207–229（2007），DOI 10.1214/105051606000000682。**
   作者预印本：https://arxiv.org/abs/math/0703017v1 。实际读取引言及问题结构；该文主要研究中心化占用过程等极限行为，不把这些定理当作本单元的首达 CDF 误差界。仅用于界定多时间尺度方法的已有背景。

3. **Jérôme Feret, Thomas Henzinger, Heinz Koeppl, Tatjana Petrov, Lumpability Abstractions of Rule-based Systems, arXiv:1011.0496v1（2010）。**
   原文：https://arxiv.org/abs/1011.0496v1 。实际读取 §4.1、Definition 22、Theorem 2 及其后讨论。它区分对所有初始分布成立的强可聚合性与特定初始分布条件。其 WLTS 速率矩阵约定与保守生成矩阵不同，不能混用对角线和自环条件。本单元的精确判定从普通有限生成矩阵的方程直接推出。

4. **Wenming Hong and Ke Zhou, arXiv:1302.5987v1（2013-02-25）。**
   固定版本：https://arxiv.org/abs/1302.5987v1 ，本地 PDF 标题为 *Hitting Time Distribution for finite states Markov Chains*。实际读取 §3 的首跳分解及线性方程。未锁版本网页展示较晚修订，其标题、页数和定理编号与 v1 不同；本单元只引用锁定的 v1，不把不同版本混为同一次读取。这里的生存函数与矩公式均在教程中直接推导，不依赖摘录的排版公式。

5. **Frank Ball and Geoffrey F. Yeo（1993），Lumpability and marginalisability for continuous-time Markov chains, Journal of Applied Probability 30(3), 518–528；Peter Buchholz（1994），Exact and ordinary lumpability in finite Markov chains, 同刊 31(1), 59–75。**
   出版方页面：
   - https://www.cambridge.org/core/journals/journal-of-applied-probability/article/lumpability-and-marginalisability-for-continuoustime-markov-chains/52418B77E531D0733B6792C967E1BB6E
   - https://www.cambridge.org/core/journals/journal-of-applied-probability/article/exact-and-ordinary-lumpability-in-finite-markov-chains/2DC748F09D80BEEB03CCF18036E149D7
   实际读取出版方摘要和书目信息，未取得这两篇全文。它们确认聚合及近似聚合已有长期先例；不将未读正文当作本单元证明的依据。页面的 2016 年在线日期不是论文首次发表年份。

6. **G. Franceschinis and R. R. Muntz（1994），Bounds for quasi-lumpable Markov chains, Performance Evaluation 20, 223–243。**
   导航：https://www.sciencedirect.com/science/article/pii/0166531694900159 。出版方正文/PDF 打开失败；没有读到可核验的完整误差界，因此不据此比较常数优劣，也不声称超过它。

## 选择与排除

- 选择一个小型、齐次、有限状态、到目标即停止的模型，研究首达时间的绝对 CDF 误差。它可以用精确矩阵计算，没有蒙特卡洛抽样噪声，也不需要有限种群灭绝概率的既有偏差结论。
- 可聚合性提供零误差检查；Poisson 方程提供可计算修正；次随机矩阵的收缩性提供可解释的充分界。它们都是已知工具，本单元是组合与教学实现。
- 没有进行系统性新颖性检索或与所有既有最优界比较。**新颖性未建立。**
