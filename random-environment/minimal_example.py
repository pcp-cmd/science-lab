"""自包含最小例子。运行：python -B minimal_example.py
需要已安装的 NumPy、SciPy；矩阵指数计算是浮点近似。
"""
import numpy as np
from scipy.linalg import expm


def extinction_probability(N, n0, nu, time, averaged=False):
    if N < 1 or not 0 <= n0 <= N or nu < 0 or time < 0:
        raise ValueError("参数超出模型范围")
    environments = [0] if averaged else [0, 1]
    states = [(n, e) for n in range(1, N + 1) for e in environments]
    index = {state: i for i, state in enumerate(states)}
    dead = len(states)
    G = np.zeros((dead + 1, dead + 1))
    for (n, e), i in index.items():
        birth = 2 * n * (1 - n / N)
        mortality = 1 if averaged else [0.5, 1.5][e]
        if n < N:
            G[i, index[n + 1, e]] += birth
        target = dead if n == 1 else index[n - 1, e]
        G[i, target] += mortality * n
        if not averaged:
            G[i, index[n, 1 - e]] += nu
        G[i, i] = -G[i].sum()
    # 最后一行全零：灭绝后保持灭绝。
    assert np.max(np.abs(G.sum(axis=1))) < 1e-12
    initial = np.zeros(dead + 1)
    if n0 == 0:
        initial[dead] = 1
    else:
        for e in environments:
            initial[index[n0, e]] = 1 / len(environments)
    final = initial @ expm(time * G)
    assert abs(final.sum() - 1) < 1e-12
    return float(final[dead])


if __name__ == "__main__":
    switching = extinction_probability(16, 8, 0.1, 10)
    average = extinction_probability(16, 8, 0.1, 10, averaged=True)
    print(f"随机环境灭绝概率：{switching:.12f}")
    print(f"平均环境灭绝概率：{average:.12f}")
    print(f"差：{switching - average:.12f}")
    assert abs(switching - 0.4332814342438991) < 1e-11
    assert abs(average - 0.2151040422159595) < 1e-11
    assert extinction_probability(16, 0, 0.1, 10) == 1
    assert extinction_probability(16, 8, 0.1, 0) == 0
