import random
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt

x = [[4.0, 10.0], [4.1, 11.0], [3.8, 9.0], [3.9, 9.8], [4.0, 10.5], [5.0, 3.0], [4.8, 5.0], [5.2, 4.0], [5.1, 2.0],
     [4.9, 3.0]]


# center_list = [random.randrange(1, 10), random.randrange(1, 10), random.randrange(1, 10)]
# # second_center = [random.randrange(1, 10), random.randrange(1, 10), random.randrange(1, 10)]
# counter = 10
# list_first = []
# list_second = []
# while counter != 0:
#     for point in x:
#         dist_first = math.dist(point, first_center)
#         dist_second = math.dist(point, second_center)
#         if dist_first > dist_second:
#             list_second.append(point)
#         else:
#             list_first.append(point)
#
#     first_center = [np.array(list_first)[:, 0].mean(), np.array(list_first)[:, 1].mean(), np.array(list_first)[:, 1].mean()]
#     second_center = [np.array(list_second)[:, 0].mean(), np.array(list_second)[:, 1].mean(), np.array(list_second)[:, 1].mean()]
#     counter -= 1
#
# print(len(list_first))
# print(len(list_second))
# print(first_center)
# print(second_center)
# print(str(list_first) + "\n\n\n\n\n\n")
# print(str(list_second))


def point_distance(point: list[float], centers_list: list[list[float]]):
    """dictionary that keeps a tuple of two points (the arg point and the current center from the arg centers_list)"""
    dist_dict: dict[tuple[tuple[float], tuple[float]], float] = {}

    """adds to the latter dictionary a cell of: key - the tuple of the point and current center (c), value -the wanted distance between 
            the current center and point"""
    for c in centers_list:
        dist_dict[(tuple(point), tuple(c))] = math.dist(point, c)

    """keeps in a variable the minimal distance between the point and the right center"""
    min_dist = min(dist_dict.values())

    """return the index of the min-distance center in the dictionary"""
    index = 0
    for c in centers_list:
        if min_dist == dist_dict[(tuple(point), tuple(c))]:
            return index
        index += 1


def kmc(x: list[list[float]], n: int):
    centers_list: list[list[float]] = []
    index_dict: dict[int, list[list[float]]] = {}
    for i in range(n):
        center_var: list[float] = [random.randrange(1, 10), random.randrange(1, 10)]
        centers_list.append(center_var)
        index_dict[i] = []
    # for i in range(10):
    for p in x:
        index_dict[point_distance(p, centers_list)].append(p)
        # for l in range(len(centers_list)):
        #     centers_list[l] = [random.randrange(1, 10), random.randrange(1, 10)]
    return index_dict, centers_list