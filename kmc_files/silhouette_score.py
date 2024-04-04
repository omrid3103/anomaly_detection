import numpy as np
from kmc_files.kmeans_clustering import *
from kmc_files.kmeans_proj import kmeans_proj_main


def silhouette_score(points_array: np.ndarray, centers_array: np.ndarray, grouping_list: list[list[int]]) -> float:
    """
    Calculate silhouette score for the clustering.

    Parameters:
        points_array (np.ndarray): Input data points.
        centers_array (np.ndarray): Array of cluster centers.
        grouping_list (list[list[int]]): List of clusters where each cluster is a list of point indices.

    Returns:
        float: Silhouette score for the clustering.
    """
    num_points = len(points_array)
    silhouette_values = []

    # Calculate a for each point
    for i, point in enumerate(points_array):
        cluster_index = cluster_index_of_point(point, centers_array)
        cluster_points = points_array[grouping_list[cluster_index]]
        a = np.mean([distance_calc(point, p) for p in cluster_points if not np.array_equal(point, p)])

        # Calculate b for each point
        b_values = []
        for j, cluster in enumerate(grouping_list):
            if j != cluster_index:
                other_cluster_points = points_array[cluster]
                b_values.append(np.mean([distance_calc(point, p) for p in other_cluster_points]))

        b = min(b_values) if b_values else 0

        # Calculate silhouette value for the point
        silhouette_value = (b - a) / max(a, b)
        silhouette_values.append(silhouette_value)

    # Calculate overall silhouette score
    silhouette_i_score = np.mean(silhouette_values)
    return silhouette_i_score


def most_efficient_n_of_clusters(points_coordinates: np.ndarray, max_clusters_to_check: int) -> int:
    silhouette_scores_list = []
    random_indices = np.random.choice(points_coordinates.shape[0], size=max_clusters_to_check, replace=False)
    centers_coordinates = points_coordinates[random_indices]
    for i in range(2, max_clusters_to_check + 1):
        updated_centers, grouping_list = kmc(points_coordinates, centers_coordinates[:i, :], i, 30)
        silhouette_scores_list.append(silhouette_score(points_coordinates, updated_centers, grouping_list))
        print(i, silhouette_score(points_coordinates, updated_centers, grouping_list))
    silhouette_scores_array = np.array(silhouette_scores_list)
    return silhouette_scores_array.argmax() + 2


def main():
    points_coordinates = kmeans_proj_main()
    print(most_efficient_n_of_clusters(points_coordinates, 8))


if __name__ == "__main__":
    main()
