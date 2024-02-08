import random
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt

x = [[4.0, 10.0], [4.1, 11.0], [3.8, 9.0], [3.9, 9.8], [4.0, 10.5], [5.0, 3.0], [4.8, 5.0], [5.2, 4.0], [5.1, 2.0],
     [4.9, 3.0]]

npa = np.array(x)


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

def distance_calc(x_point: float, y_point: float, x_center: float, y_center: float) -> float:
    return math.sqrt(math.pow(x_point - x_center, 2) + math.pow(y_point - y_center, 2))


def point_distance(x_point: float, y_point: float, centers_array: np.array):
    #centers_list: list[list[float]]
    """dictionary that keeps a tuple of two points (the arg point and the current center from the arg centers_list)"""
    # dist_dict: dict[tuple[tuple[float], tuple[float]], float] = {}
    distance_arr = np.zeros([len(centers_array), 3], dtype=float)

    """adds to the latter dictionary a cell of: key - the tuple of the point and current center (c), value -the wanted distance between 
            the current center and point"""
    i = 0
    for c in centers_array:
        row_list: list[float, float, float] = [x_point, y_point, distance_calc(x_point, y_point, c[0], c[1])]
        row_array = np.array(row_list)
        distance_arr[i, :] = row_array
        i += 1
        # dist_dict[(tuple(point), tuple(c))] = math.dist(point, c)

    """keeps in a variable the minimal distance between the point and the right center"""
    min_dist, min_dist_index = distance_arr[:, 2].min(), distance_arr[:, 2].argmin()
    return min_dist_index
    # """return the index of the min-distance center in the dictionary"""
    # index = 0
    # for c in centers_list:
    #     if min_dist == dist_dict[(tuple(point), tuple(c))]:
    #         return index
    #     index += 1


def kmc(points_array: np.array, n: int):
    centers_array: np.array = np.zeros([n, 2], dtype=float)
    index_dict: dict[int, list[list[float]]] = {}
    grouping_array = np.zeros([len(points_array), 3])
    for i in range(n):
        specific_center_arr: np.array = np.array([random.randrange(1, 10), random.randrange(1, 10)])
        centers_array[i, :] = specific_center_arr
        index_dict[i] = []
    # for i in range(10):
    i = 0
    for p in points_array:
        # index_dict[point_distance(p, centers_list)].append(p)
        grouping_array[i, :] = np.array([point_distance(p[0], p[1], centers_array), p[0], p[1]])
        i += 1
        # for l in range(len(centers_list)):
        #     centers_list[l] = [random.randrange(1, 10), random.randrange(1, 10)]
    return grouping_array, centers_array


def main():
    g_a, c_a = kmc(npa, 4)
    print(g_a)
    print(c_a)

if __name__ == "__main__":
    main()
