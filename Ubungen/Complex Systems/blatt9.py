import numpy as np
from math import comb


def binomial_entropy(n, p):
    ans = 0
    for k in range(n+1):
        Pk = comb(n,k) * (p**k) * ((1-p)**(n-k))
        ans -= Pk * np.log2(Pk)
    return ans

print(binomial_entropy(1,0.5))
print(binomial_entropy(2,0.5))
print(binomial_entropy(4,0.5))
print(binomial_entropy(8,0.5))
