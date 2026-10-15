# 空间验证：误差对应哪一种预测任务？

[中文](README.md) | [English](README.en.md)

这是合成高斯场上的可复现方法演示与探索性条件边界分析，**没有建立新颖性**，也没有逐项复现引用论文的真实数据实验。

## 问题与结果

同样观测160点、预测40点，随机缺失、连续内部缺口与边缘缺口是不同任务。在200点等距一维、零均值单位方差、无噪声指数协方差且已知正确相关长度40的模型中：

- 随机五折的精确MSE为0.029373，内部连续缺口为0.327692：相对目标低估91.04%。
- 包含边缘块的连续五折为0.427970：相对内部目标高估30.60%。
- 将最近观测距离都配平到1–20后，单侧与双侧观测的风险仍相差17.05%（以双侧为分母）。
- 参数设错可以改变方向：真实长度2、假定10时，双侧风险1.103229高于单侧1.100060；模型报告方差也不等于真实MSE。

因此，应先定义部署任务与可用信息，再设计验证划分。上述数字不能直接推广到未知超参数、非平稳、带噪声、二维或现实地图；误设分析是主结果之后的探索性工作。

## 阅读与运行

从[完整中文教程](TUTORIAL.zh-CN.md)开始：背景、逐步代数、完整代码、文献、负对照、失败实例、误设边界及练习均保留。两张图：[验证几何](figures/research_unit.png)、[误设边界](figures/misspecification_boundary.png)。

使用已安装NumPy的Python，在本目录运行：

```sh
OPENBLAS_NUM_THREADS=1 python -B minimal.py
OPENBLAS_NUM_THREADS=1 python -B minimal_boundary.py
OPENBLAS_NUM_THREADS=1 python -B check_evidence.py
```

脚本不联网，不下载数据。前两项会生成小规模教学模拟，最后一项仅用解析公式检查选定表格。最小代码不重建完整原始实验。

## 证据与核验范围

- [主实验36行汇总](evidence/summary.csv)：六种长度、六种评分方案，含MSE、标准误与区间。
- [全部45组误设结果](evidence/extension_grid.csv)与[9行次要比较](evidence/extension_secondary.csv)，不只选取支持结论的行。
- [探索性机制结果](evidence/mechanism_summary.json)，包括未支持真实效应的iid区间实例。
- [主实验参数](evidence/protocol.json)与[误设参数](evidence/extension_config.json)：保留科学设置和种子。
- original_verification.json及original_extension_verification.json是原始实验校验记录；算法独立由同一研究者完成，非外部盲审。

2026-10-15整理本版时，先核对原包83个清单条目的SHA-256，再审阅并实际运行两份最小脚本和本版check_evidence.py。运行环境为Python 3.12.14、NumPy 2.3.5，无新增安装。[主案例输出](validation/minimal-output.txt)、[边界输出](validation/boundary-output.txt)和[解析检查结果](validation/evidence-check.json)记录本版实际验证。

本版重新核对全部45格端点真实风险/报告方差、六种长度的部署风险和混合恒等式；没有重新核对原始大型权重、逐场数组或从原始样本重算全部标准误。完整实验运行器与大型原始数组未收录，避免把历史校验记录误当成本版的重新验证。原始完整实验还使用SciPy 1.17.0与Matplotlib 3.10.8。引用文献沿用原教程，本次整理未重新做文献检索。
