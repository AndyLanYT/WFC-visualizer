import matplotlib.pyplot as plt
import numpy as np


x = np.array([21, 5, 40])
y = np.array([25, 100, 225, 400])

X, Y = np.meshgrid(x, y)

Z = np.array([
    [ 1.009, 11.753, 52.799, 151.634 ],
    [ 0.472,  2.407,  6.126,  13.463 ],
    [ 5.077, 40.307, 173.05, 515.473 ]
]).T


print(X)
print()
print(Y)
print()
print(Z)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(X, Y, Z, cmap='turbo_r')
ax.set_xlabel('input size')
ax.set_ylabel('output size')
ax.set_zlabel('seconds')

plt.show()

