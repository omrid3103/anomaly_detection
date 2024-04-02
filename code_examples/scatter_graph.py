import numpy as np
import matplotlib.pyplot as plt
from kmc_files.kmeans_clustering import kmc
from kmc_files.kmeans_proj import main

points_coordinates = main()
print(points_coordinates)
random_indices = np.random.choice(points_coordinates.shape[0], size=5, replace=False)
centers_coordinates = points_coordinates[random_indices]
print(centers_coordinates)
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