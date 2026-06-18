import numpy as np
from math import comb
import matplotlib.pyplot as plt
import pandas as pd


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


xmin = 1
xmax = 50
xvals_sim = np.arange(xmin, xmax)
xvals_fit = np.linspace(xmin, xmax, 1000)
sim = np.array([binomial_entropy(x, 0.5) for x in xvals_sim])
fitted = np.array([np.log2(x*np.pi*np.e / 2)/2 for x in xvals_fit])

plt.scatter(xvals_sim, sim)
plt.plot(xvals_fit, fitted)
plt.show()

data_sim = {"xvals":xvals_sim, "data":sim}
data_fitted = {"xvals":xvals_fit, "data":fitted}

df = pd.DataFrame(data=data_sim)
df.to_csv("blatt9_sim.csv", index=None)
df = pd.DataFrame(data=data_fitted)
df.to_csv("blatt9_fit.csv", index=None)
