import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from kmc_files.kmeans_clustering import kmc
from kmc_files.kmeans_proj import kmeans_proj_main

points_coordinates = kmeans_proj_main()
print(points_coordinates)
points_coordinates_3d = points_coordinates[:, :3]
random_indices = np.random.choice(points_coordinates.shape[0], size=4, replace=False)
centers_coordinates = points_coordinates[random_indices]
print(centers_coordinates)
centers_coordinates_3d = centers_coordinates[:, :3]
grouping_list = []
# Generate random data

# plt.scatter(points_coordinates_4d[cluster][:, 0], points_coordinates_4d[cluster][:, 1], points_coordinates_4d[cluster][:, 1], label=str(j))
# plt.scatter(center[0], center[1], s=90, c='black', label=f"{j} center")

ITERATIONS = 5
COLORS = ['teal', 'cyan', 'black', 'red', 'blue', 'green', 'orange', 'pink', 'gold']

for _ in range(ITERATIONS):
    centers_coordinates, grouping_list = kmc(points_coordinates, centers_coordinates, 4)

    print(centers_coordinates)
    print(grouping_list)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title('3D Scatter Plot')

    for j, (center, cluster) in enumerate(zip(centers_coordinates, grouping_list)):
        plt.figure(figsize=(6, 6))
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
                ax.scatter(x, y, z, c=COLORS[j], label=str(j))
        ax.scatter(x_center, y_center, z_center, s=90, c=COLORS[j], label=f"{j} center")

    # ax.legend()
    plt.show()





