"""只需 NumPy：参数设错时，两端预测未必优于单端预测。
手动运行 python minimal_boundary.py；不联网，无后台或自动重启。
"""
import numpy as np


def point_risks(true_length, model_length):
    d = np.arange(1, 21, dtype=float)

    def correlation(distance, length):
        return np.zeros_like(distance) if length == 0 else np.exp(-distance / length)

    # A、B是模型相信的相关；u、v、r是真实相关。
    A = correlation(d, model_length)
    B = correlation(41 - d, model_length)
    denominator = 1 - A*A*B*B
    p = A * (1 - B*B) / denominator
    q = B * (1 - A*A) / denominator
    u = correlation(d, true_length)
    v = correlation(41 - d, true_length)
    r = correlation(np.full_like(d, 41), true_length)
    one = 1 + A*A - 2*A*u
    both = 1 + p*p + q*q + 2*p*q*r - 2*p*u - 2*q*v
    return one, both, A, p, q


def simulate(true_length, model_length, case_index):
    one, both, A, p, q = point_risks(true_length, model_length)
    reported_one, reported_both, *_ = point_risks(model_length, model_length)
    x = np.arange(42)
    K = (np.eye(42) if true_length == 0 else
         np.exp(-abs(x[:, None] - x[None, :]) / true_length))
    rng = np.random.default_rng([2026101507, case_index])
    fields = rng.standard_normal((2048, 42)) @ np.linalg.cholesky(K).T
    # 同一组目标和左端点，比较两种预测，降低差值的随机噪声。
    target = fields[:, 1:21]
    pred_one = fields[:, [0]] * A
    pred_both = fields[:, [0]] * p + fields[:, [41]] * q
    loss_one = ((target - pred_one)**2).mean(axis=1)
    loss_both = ((target - pred_both)**2).mean(axis=1)
    difference = loss_one - loss_both  # 每行是一条独立场的配对差。
    se = difference.std(ddof=1) / np.sqrt(len(difference))
    print(f"真实长度={true_length}, 假定长度={model_length}")
    print(f"  真实MSE: 单端={one.mean():.9f}, 两端={both.mean():.9f}")
    print(f"  报告方差: 单端={reported_one.mean():.9f}, 两端={reported_both.mean():.9f}")
    print(f"  单端减两端: 精确={(one-both).mean():.9f}, "
          f"MC={difference.mean():.9f}, 95%区间="
          f"[{difference.mean()-1.96*se:.9f}, {difference.mean()+1.96*se:.9f}]")
    if true_length == model_length == 0:
        assert np.all(difference == 0)


if __name__ == "__main__":
    for index, (truth, model) in enumerate([(0, 10), (2, 10), (40, 40), (0, 0)]):
        simulate(truth, model, index)
    # 一次括区二分，只报告一个过零点，不证明唯一性。
    lo, hi = .5, 20.0
    for _ in range(50):
        mid = (lo + hi) / 2
        one, both, *_ = point_risks(mid, 10)
        if (one - both).mean() < 0:
            lo = mid
        else:
            hi = mid
    print(f"假定长度10时，本括区过零点约为{(lo+hi)/2:.9f}")
