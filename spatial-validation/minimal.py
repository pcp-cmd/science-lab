"""最小实验：只需 NumPy。手动运行 python minimal.py；不联网，不自动重启。"""
import numpy as np


def run(ell, ell_index):
    n, w, repeats = 200, 40, 8192
    x = np.arange(n)
    K = np.eye(n) if ell == 0 else np.exp(-abs(x[:, None] - x) / ell)
    rng = np.random.default_rng([2026101502, ell_index])
    field = rng.standard_normal((repeats, n))
    if ell > 0:  # 每行是一条独立的场；相邻列彼此相关。
        a, s = np.exp(-1 / ell), np.sqrt(-np.expm1(-2 / ell))
        for j in range(1, n):
            field[:, j] = a * field[:, j - 1] + s * field[:, j]

    def score(test, rows=None):
        train = np.setdiff1d(x, test)
        assert len(train) == 160 and not np.intersect1d(train, test).size
        cross = K[np.ix_(train, test)]
        W = np.linalg.solve(K[np.ix_(train, train)], cross).T
        variance = 1 - np.sum(W * cross.T, axis=1)
        error = field[:, test] - field[:, train] @ W.T
        if rows is not None:  # 未评分的缺失点依然不能放回训练。
            variance, error = variance[rows], error[:, rows]
        return float(variance.mean()), (error ** 2).mean(axis=1)

    blocks = [score(np.arange(j * w, (j + 1) * w)) for j in range(5)]
    random_scores = []
    for p in range(20):
        order = np.random.default_rng(2026101501 + p).permutation(n)
        random_scores += [score(np.sort(test)) for test in np.split(order, 5)]
    groups = {"random_cv": random_scores, "blocked_cv": blocks,
              "interior_cv": blocks[1:4], "edge_cv": [blocks[0], blocks[4]]}
    print(f"ell={ell}; 误差条针对仿真均值，不是单次预测")
    exact = {}
    for name, scores in groups.items():
        truth = float(np.mean([s[0] for s in scores]))
        loss = np.mean([s[1] for s in scores], axis=0)
        se = loss.std(ddof=1) / np.sqrt(repeats)  # 独立单位是整行。
        exact[name] = truth
        print(f"{name:12s} exact={truth:.8f} MC={loss.mean():.8f} +/- {1.96*se:.8f}")
    assert np.isclose(exact["blocked_cv"],
                      .6 * exact["interior_cv"] + .4 * exact["edge_cv"])
    if ell == 0:
        assert all(np.isclose(v, 1) for v in exact.values())
    else:  # 不使用矩阵求解的两端公式，再检查一次。
        d = np.arange(1, w + 1)
        bridge = ((-np.expm1(-2*d/ell)) * (-np.expm1(-2*(w+1-d)/ell))
                  / (-np.expm1(-2*(w+1)/ell)))
        assert np.isclose(bridge.mean(), exact["interior_cv"])
    inside = score(np.arange(73, 113), np.arange(20))[0]
    edge = score(np.arange(40), np.arange(20, 40))[0]
    print(f"同为最近距离1..20：内部={inside:.8f} 边缘={edge:.8f}")


if __name__ == "__main__":
    run(0.0, 0)   # 无相关负对照
    run(40.0, 4)  # 主案例；索引4与完整方案一致
