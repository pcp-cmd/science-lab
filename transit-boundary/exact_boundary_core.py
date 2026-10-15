"""Independent exact certificate for the alpha=2 near-contact teaching case.

Standard library only. No circle-overlap formula, quadrature, or prior files.
Every decision uses Fraction; decimals are only outward displays.
"""
from fractions import Fraction as Q

def outward(q,places=12,upper=False):
    q=Q(q);scale=10**places;n=q.numerator*scale;d=q.denominator
    value=-((-n)//d) if upper else n//d
    sign='-' if value<0 else '';value=abs(value)
    return f"{sign}{value//scale}.{value%scale:0{places}d}"

def exact_boundary_certificate(k,z,c,J):
    k,z,c,J=map(Q,(k,z,c,J));epsilon=z+k-1
    if not (0<k<=1 and z>=0 and 0<=c<=1 and 0<=epsilon<Q(1,10)):
        raise ValueError('Requires a planet near or at internal contact')
    if 1-c*(1+epsilon)**2<0:
        raise ValueError('This exterior polynomial bound requires nonnegative intensity')
    d=1-c/2
    full=10**6*k*k*(1-c*(z*z+k*k/2)-J)/d
    omitted_area_factor=(1+epsilon)**2-1
    width=10**6*omitted_area_factor*max(abs(J),abs(1-J))/d
    lower,upper=full-width,full+width
    status='SAFE' if -1<=lower<=upper<=1 else 'UNSAFE' if lower>1 or upper< -1 else 'UNRESOLVED'
    return lower,upper,status

def main():
    k=Q(1,100);epsilon=Q(1,2**120);z=Q(99,100)+epsilon;c=Q(7,10)
    # Preserve the exact binary64 J selected by the frozen new boundary case.
    J=Q.from_float(float(1-c*z*z))
    denominator=(z+k)**2-1;scale=2**96
    dlo=denominator.numerator*scale//denominator.denominator
    dhi=-((-denominator.numerator*scale)//denominator.denominator)
    assert denominator>0 and (dlo,dhi)==(0,1)
    lower,upper,status=exact_boundary_certificate(k,z,c,J)
    assert status=='SAFE' and upper-lower<Q(4,10**30)
    print('positive denominator at 96 bits: [0, 1/2**96]')
    print('exact independent certificate: '+status+', ['+outward(lower)+', '+outward(upper,upper=True)+'] ppm')
    print('exact certificate width is below 4e-30 ppm')
    print('PASS: Fraction decisions; no numerical integration or external files.')

if __name__=='__main__':main()
