import matplotlib.pyplot as plt
import numpy as np
import random

N = 10000
X1 = np.array([random.randint(0,9) for i in range(N)])
X2 = np.array([random.randint(0,9) for i in range(N)])
X3 = X1 + X2
bins = np.arange(0,20) - 0.5
plt.hist(X3, bins = bins, align = 'mid', rwidth = 0.5)
plt.gca().set_xticks(range(19))
plt.xlabel(r"Sum $X_1+X_2$")
plt.ylabel("Frequency")
#plt.show()
plt.savefig("histogram_sum.pdf")
