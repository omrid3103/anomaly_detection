import random
import numpy as np
import math
import statistics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from db_and_pdf_demo import kmc_controller


def distance_calc(point_coordinates_arr: np.ndarray, center_coordinates_arr: np.ndarray) -> float:
    sum_differences: int = 0
    for i in range(len(point_coordinates_arr)):
        sum_differences += math.pow(point_coordinates_arr[i] - center_coordinates_arr[i], 2)
    return math.sqrt(sum_differences)


def cluster_index_of_point(specific_point_arr: np.ndarray, centers_array: np.array):
    """dictionary that keeps a tuple of two points (the arg point and the current center from the arg centers_list)"""
    distance_arr = np.zeros([len(centers_array), len(specific_point_arr) + 1], dtype=float)

    """adds to the latter dictionary a cell of: key - the tuple of the point and current center (c), value -the wanted distance between 
            the current center and point"""
    i = 0
    for c in centers_array:
        row_list = []
        for j in range(len(specific_point_arr)):
            row_list.append(specific_point_arr[j])
        row_list.append(distance_calc(specific_point_arr, c))
        row_array = np.array(row_list)
        distance_arr[i, :] = row_array
        i += 1

    """keeps in a variable the minimal distance between the point and the right center"""
    min_dist, min_dist_index = distance_arr[:, len(specific_point_arr)].min(), distance_arr[:, len(specific_point_arr)].argmin()
    return min_dist_index


def clusters_groups_division(points_array: np.ndarray, centers_array: np.ndarray, n_clusters: int) -> list[list[int]]:
    grouping_list: list[list[int]] = [[] for _ in range(n_clusters)]
    for i, p in enumerate(points_array):
        cluster_i = cluster_index_of_point(p, centers_array)
        grouping_list[cluster_i].append(i)
    return grouping_list


def new_centers(points_array: np.array, grouping_list: list[list[int]]) -> np.ndarray:
    centers = np.zeros((len(grouping_list), len(points_array[0])))
    for cluster_i, cluster_points_i in enumerate(grouping_list):
        if len(grouping_list[cluster_i]) != 0:
            for j in range(len(points_array[0])):
                centers[cluster_i][j] = points_array[cluster_points_i][:, j].mean()
        else:
            continue
    return centers


def kmc(
        points_array: np.ndarray,
        centers_array: np.ndarray,
        n_clusters: int,
        iterations: int = 1
) -> tuple[np.ndarray, list[list[int]]]:
    grouping_list = clusters_groups_division(points_array, centers_array, n_clusters)
    # for i, p in enumerate(points_array):
    #     print(i, p)
    # print("Test run #1")
    # print(centers_array)
    # print(grouping_list)
    # print("\n")
    for i in range(iterations):
        # print("Test run #" + str(i + 2))
        centers_array = new_centers(points_array, grouping_list)
        # print(new_centers_arr)
        grouping_list = clusters_groups_division(points_array, centers_array, n_clusters)
        # print(grouping_list)
        # print("\n")
    return centers_array, grouping_list


def scatter_graph_3d(
        points_coordinates: np.ndarray,
        iterations: int = 10
) -> plt:

    random_indices = np.random.choice(points_coordinates.shape[0], size=6, replace=False)
    centers_coordinates = points_coordinates[random_indices]

    grouping_list = []
    # Generate random initial cluster centers out of the points array

    # plt.scatter(points_coordinates_4d[cluster][:, 0], points_coordinates_4d[cluster][:, 1], points_coordinates_4d[cluster][:, 1], label=str(j))
    # plt.scatter(center[0], center[1], s=90, c='black', label=f"{j} center")

    COLORS = ['gold', 'teal', 'black', 'red', 'blue', 'green', 'orange', 'pink', 'cyan']

    for _ in range(iterations):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')
        ax.set_title('3D Scatter Plot')

        centers_coordinates, grouping_list = kmc(points_coordinates, centers_coordinates, 6)

        print(centers_coordinates)
        print(grouping_list)

        for j, (center, cluster) in enumerate(zip(centers_coordinates, grouping_list)):
            # plt.figure(figsize=(6, 6))
            x_cluster_points = points_coordinates[cluster][:, 0]
            y_cluster_points = points_coordinates[cluster][:, 1]
            z_cluster_points = points_coordinates[cluster][:, 2]
            x_center = center[0]
            y_center = center[1]
            z_center = center[2]

            for index, (x, y, z) in enumerate(zip(x_cluster_points, y_cluster_points, z_cluster_points)):
                if points_coordinates[cluster][index][3] == 1.0:
                    ax.scatter(x, y, z, c=COLORS[j], marker='*', label=str(j))
                else:
                    ax.scatter(x, y, z, c=COLORS[j], label=str(j), marker='s')
            ax.scatter(x_center, y_center, z_center, s=90, c=COLORS[j], label=f"{j} center")

        # ax.legend()
        plt.show()


def main():
    points_coordinates: np.ndarray = kmc_controller.kmc_controller_main()
    scatter_graph_3d(points_coordinates)


if __name__ == "__main__":
    main()