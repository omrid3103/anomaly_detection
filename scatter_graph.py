import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from dataclasses import dataclass

# x = np.array()
# plt.scatter(x[ : , 0], x[ :, 1], s = 100, c = 'b')
# plt.show()

@dataclass(slots=True, frozen=False)
class Point():
    x: int
    y: int


points = list()
for i in range(14):
    x = i
    y = pow(i, 2)
    p = Point(x, y)
    points.append(p)

# The question starts here.
# The best I could come up with so far:
x = np.fromiter((p.x for p in points), int)
y = np.fromiter((p.y for p in points), int)
arr = np.vstack((x, y)).transpose()
print(arr)
plt.scatter(arr[ : , 0], arr[ :, 1], s = 13, c = 'g')
plt.show()