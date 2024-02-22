import numpy as np
import matplotlib.pyplot as plt
from kmeans_clustering import kmc

points_coordinates = np.random.uniform(1, 20, (150, 2))
centers_coordinates = np.random.uniform(1, 20, (5, 2))

grouping_list = []

ITERATIONS = 5

for _ in range(ITERATIONS):
    centers_coordinates, grouping_list = kmc(points_coordinates, centers_coordinates, 5)

    print(centers_coordinates)
    print(grouping_list)

    plt.figure(figsize=(6, 6))

    for j, (center, cluster) in enumerate(zip(centers_coordinates, grouping_list)):
        plt.scatter(points_coordinates[cluster][:, 0], points_coordinates[cluster][:, 1], label=str(j))
        plt.scatter(center[0], center[1], s=90, c='black', label=f"{j} center")

    plt.legend()
    plt.show()