"""只用 Python 标准库：python3 -B mean_minimal.py。所有数学计算用有理数。"""
from fractions import Fraction as F


def M(rows):
    return [[F(x) for x in row] for row in rows]


def mul(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def solve(a, b):
    # 精确消元：每列找非零主元，再把其他行这一列消掉。
    n = len(a)
    rows = [ar[:] + br[:] for ar, br in zip(a, b)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if rows[i][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        divisor = rows[col][col]
        rows[col] = [x/divisor for x in rows[col]]
        for i in range(n):
            if i != col:
                factor = rows[i][col]
                rows[i] = [x-factor*y for x, y in zip(rows[i], rows[col])]
    return [row[n:] for row in rows]


K = M([[-1,1,0,0], [2,-2,0,0], [0,0,-1,1], [0,0,2,-2]])
L = M([[-2,0,1,0], [0,-5,0,3], [2,0,-3,0], [0,1,0,-4]])
J = M([[1,0], [1,0], [0,1], [0,1]])
P = M([['2/3','1/3',0,0], [0,0,'2/3','1/3']])
A = mul(mul(P, L), J)
ma = solve([[-x for x in row] for row in A], M([[1], [1]]))
LJ, JA = mul(L, J), mul(J, A)
D = [[x-y for x, y in zip(ar, br)] for ar, br in zip(LJ, JA)]
# 本例每块 K 的非零特征值为 -3，中心化向量上 H=D/3。
H = [[x/3 for x in row] for row in D]
assert mul(K, H) == [[-x for x in row] for row in D]
assert all(x == 0 for row in mul(P, H) for x in row)
z = [row[0] for row in mul(J, ma)]
c = [row[0] for row in mul(H, ma)]
r = [row[0] for row in mul(L, [[x] for x in c])]
cstar = max(abs(ci)/zi for ci, zi in zip(c, z))
rstar = max(abs(x) for x in r)
threshold = rstar + 100*(cstar + rstar)  # 1% 相对均值误差的充分阈值
nu = F(300)
v = [zi+ci/nu for zi, ci in zip(z, c)]
g = [1-ri/nu for ri in r]
Q = [[nu*x+y for x, y in zip(kr, lr)] for kr, lr in zip(K, L)]
assert mul(Q, [[x] for x in v]) == [[-x] for x in g]
if min(v) <= 0 or min(g) <= 0:
    raise ValueError('本证书未认证；不能据此说真实均值无穷。')
lower = [x/max(g) for x in v]
upper = [x/min(g) for x in v]
mean = [row[0] for row in solve([[-x for x in row] for row in Q], M([[1]]*4))]
assert all(lo <= x <= hi for lo, x, hi in zip(lower, mean, upper))
error_bound = max(max(abs(lo-zi), abs(hi-zi))/zi for lo, hi, zi in zip(lower, upper, z))
beta = min(g)/max(v)
print('平均链均值：', [str(row[0]) for row in ma])
print('1% 充分阈值：', threshold, '≈', float(threshold))
print('nu=300 相对均值误差上界：', error_bound, '≈', float(error_bound))
print('生存尾部指数 beta：', beta)
for i, (lo, x, hi) in enumerate(zip(lower, mean, upper)):
    print(i, str(lo), '<=', str(x), '<=', str(hi))
