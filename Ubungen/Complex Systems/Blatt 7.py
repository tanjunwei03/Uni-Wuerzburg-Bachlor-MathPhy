import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
x = 1
y = 1
z = 1
max_iter = 20
alpha = 0.2
alphay = 2*np.e/(np.exp(2) - 1)
alphaz = 1
xlst = [x]
ylst = [y]
zlst = [z]
for i in range(max_iter):
    x -= alpha*np.sinh(x)
    xlst.append(x)
    y -= alphay*np.sinh(y)
    ylst.append(y)
    z -= alphaz*np.sinh(z)
    zlst.append(z)

plt.scatter(range(len(xlst)), xlst)
plt.scatter(range(len(xlst)), ylst)
plt.scatter(range(len(xlst)), zlst)

df = pd.DataFrame(data={"xvals":range(len(xlst)), "0.2":xlst, "1":zlst, "optimal":ylst})
df.to_csv("blatt7_data.csv", index = False)
plt.show()
