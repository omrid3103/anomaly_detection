import random
import numpy as np
import math
import statistics

x = [[4, 10, 8], [4.1, 11, 7], [3.8, 9, 9], [3.9, 9.8, 8], [4, 10.5, 7.9], [5, 3, 4], [4.8, 5, 5], [5.2, 4, 4.5], [5.1, 2, 4.2], [4.9, 3, 3.7]]
first_center = [random.randrange(1, 10), random.randrange(1, 10), random.randrange(1, 10)]
second_center = [random.randrange(1, 10), random.randrange(1, 10), random.randrange(1, 10)]
counter = 100
list_first = []
list_second = []
while counter != 0:
    for point in x:
        dist_first = math.dist(point, first_center)
        dist_second = math.dist(point, second_center)
        if dist_first > dist_second:
            list_second.append(point)
        else:
            list_first.append(point)

    first_center = [np.array(list_first)[:, 0].mean(), np.array(list_first)[:, 1].mean(), np.array(list_first)[:, 1].mean()]
    second_center = [np.array(list_second)[:, 0].mean(), np.array(list_second)[:, 1].mean(), np.array(list_second)[:, 1].mean()]
    counter -= 1

print(len(list_first))
print(len(list_second))
print(first_center)
print(second_center)
print(str(list_first) + "\n\n\n\n\n\n")
print(str(list_second))