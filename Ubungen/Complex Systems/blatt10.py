import numpy as np

p1 = 1/2
p2 = 1/2
psi1 = np.array([1,1]) / np.sqrt(2)
psi2 = np.array([0,1])

rho = p1 * np.outer(psi1, psi1) + p2 * np.outer(psi2, psi2)

print(rho)

eigvals, eigvecs = np.linalg.eigh(rho)

print(eigvals)
print(eigvecs)
