import matplotlib.pyplot as plt
import numpy as np
import random

N = 10000
lst = [random.randint(0,9) for i in range(N)]
bins = np.arange(0,11) - 0.5
plt.hist(lst, bins = bins, align = 'mid', rwidth = 0.5)
plt.gca().set_xticks(range(10))
plt.gca().set_ylim(ymin=900)
plt.xlabel("Digit")
plt.ylabel("Frequency")
plt.savefig("histogram.pdf")
