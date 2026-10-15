"""E02自包含严格根存在实验，仅需Python标准库。
运行：python -B minimal_e02.py
模型固定N=8、n0=4、两向环境速率1/10。输出区间认证存在，不认证全局唯一性。
"""
from fractions import Fraction as F
from math import ceil, lcm


def probability_bounds(t, averaged=False, K=400):
    t = F(t)
    deaths = (F(1),) if averaged else (F(1, 2), F(3, 2))
    environments = len(deaths)
    dead = 8 * environments
    rules = []
    for e, mu in enumerate(deaths):
        for n in range(1, 9):
            events = []
            if n < 8:
                events.append((e * 8 + n, F(n * (8 - n), 4)))
            events.append((dead if n == 1 else e * 8 + n - 2, mu * n))
            if not averaged:
                events.append(((1 - e) * 8 + n - 1, F(1, 10)))
            rules.append(events)
    D = lcm(*(rate.denominator for row in rules for _, rate in row))
    lam = ceil(max(sum(rate for _, rate in row) for row in rules))
    base = lam * D
    x = lam * t
    if t < 0 or K + 2 <= x:
        raise ValueError("时间非法或K不足")
    weights = []
    for state, row in enumerate(rules):
        events = [(target, int(rate * D)) for target, rate in row]
        events.append((state, base - sum(weight for _, weight in events)))
        assert all(weight >= 0 for _, weight in events)
        weights.append(events)
    weights.append([(dead, base)])
    counts = [0] * (dead + 1)
    for e in range(environments):
        counts[e * 8 + 3] = 1  # n0=4的索引
    coefficient = F(1, environments)
    numerator, a, total = F(0), F(1), F(1)
    mass = environments
    for k in range(1, K + 1):
        updated = [0] * len(counts)
        for state, count in enumerate(counts):
            for target, weight in weights[state]:
                updated[target] += count * weight
        counts = updated
        mass *= base
        assert sum(counts) == mass
        coefficient *= t / (D * k)
        numerator += coefficient * counts[dead]
        a *= x / k
        total += a
    tail = a * x / (K + 1) / (1 - x / (K + 2))
    return numerator / (total + tail), min(F(1), (numerator + tail) / total)


def delta_bounds(t):
    switch = probability_bounds(t)
    average = probability_bounds(t, averaged=True)
    return switch[0] - average[1], switch[1] - average[0]


if __name__ == "__main__":
    left, right = F(5), F(10)
    assert delta_bounds(left)[0] > 0
    assert delta_bounds(right)[1] < 0
    steps = 0
    while right - left > F(1, 1000):
        if steps >= 16:
            raise RuntimeError("达到冻结迭代上限")
        middle = (left + right) / 2
        low, high = delta_bounds(middle)
        if low > 0:
            left = middle
        elif high < 0:
            right = middle
        else:
            raise RuntimeError("区间含零，不能凭浮点猜符号")
        steps += 1
    assert 0 < left < right and right - left <= F(1, 100)
    assert delta_bounds(left)[0] > 0 and delta_bounds(right)[1] < 0
    print("严格根区间（有理端点）：", left, right)
    print("端点十进制：", float(left), float(right))
    print("宽度：", right - left, "=", float(right - left))
    print("二分步数：", steps)
    print("连续性+严格异号证明至少一个非零根；此最小程序不证明唯一性。")
