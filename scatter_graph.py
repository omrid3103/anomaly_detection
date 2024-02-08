import numpy as np
import matplotlib.pyplot as plt
from kmeans_clustering import kmc
from dataclasses import dataclass
from datetime import datetime


# x = np.array()
# plt.scatter(x[ : , 0], x[ :, 1], s = 100, c = 'b')
# plt.show()
class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y


# points = [Point(4.0, 10.0), Point(4.1, 11.0), Point(3.8, 9.0), Point(3.9, 9.8), Point(4.0, 10.5), Point(5.0, 3.0), Point(4.8, 5.0), Point(5.2, 4.0), Point(5.1, 2.0), Point(4.9, 3.0)]
# points = [[4.0, 10.0, 8.0], [4.1, 11.0, 7.0], [3.8, 9.0, 9.0], [3.9, 9.8, 8.0], [4.0, 10.5, 7.9], [5.0, 3.0, 4.0], [4.8, 5.0, 5.0], [5.2, 4.0, 4.5], [5.1, 2.0, 4.2], [4.9, 3.0, 3.7]]
points = [
    [4.0, 10.0],
    [4.1, 11.0],
    [3.8, 9.0],
    [3.9, 9.8],
    [4.0, 10.5],
    [5.0, 3.0],
    [4.8, 5.0],
    [5.2, 4.0],
    [5.1, 2.0],
    [4.9, 3.0],
    [4.4, 7.9],
    [5.1, 10.5],
    [4.8, 10.1],
    [5.2, 8.5],
    [4.1, 5.6],
    [4.4, 7.6],
    [3.9, 4.9]
]
npa = np.array(points)

# before = datetime.now()
grouping_arr, centers_arr = kmc(npa, 4)
print(grouping_arr)
# after = datetime.now()
# print(after-before)



# list1 = dict1[0]
# print(list1)
# list2 = dict1[1]
# print(list2)
# list3 = dict1[2]
# print(list3)
# list4 = dict1[3]
# print(list4)
#
#
#
#
#
# # The question starts here.
# # The best I could come up with so far:
#
# x = np.fromiter((l1[0] for l1 in list1), float)
# y = np.fromiter((l1[1] for l1 in list1), float)
# arr1 = np.vstack((x, y)).transpose()
# x = np.fromiter((l2[0] for l2 in list2), float)
# y = np.fromiter((l2[1] for l2 in list2), float)
# arr2 = np.vstack((x, y)).transpose()
# x = np.fromiter((l3[0] for l3 in list3), float)
# y = np.fromiter((l3[1] for l3 in list3), float)
# arr3 = np.vstack((x, y)).transpose()
# x = np.fromiter((l4[0] for l4 in list4), float)
# y = np.fromiter((l4[1] for l4 in list4), float)
# arr4 = np.vstack((x, y)).transpose()
# x = np.fromiter((l5[0] for l5 in centers), float)
# y = np.fromiter((l5[1] for l5 in centers), float)
# arr5 = np.vstack((x, y)).transpose()
# plt.scatter(arr1[:, 0], arr1[:, 1], s=13, c='g')
# plt.scatter(arr2[:, 0], arr2[:, 1], s=13, c='r')
# plt.scatter(arr3[:, 0], arr3[:, 1], s=13, c='b')
# plt.scatter(arr4[:, 0], arr4[:, 1], s=13, c='y')
# plt.scatter(arr5[:, 0], arr5[:, 1], s=25, c='black')
# plt.show()