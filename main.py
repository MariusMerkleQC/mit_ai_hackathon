import numpy as np
from sklearn.neighbors import NearestNeighbors
from coordinate_utils import _convert_to_degress, get_gps_data
from generate_random_coordinates import generate_random_coordinates
from optimization_problem import maximize_utility_with_distance_constraint
from path_utils import get_abnormal_test_image_paths, get_normal_test_image_paths, load_abnormal_test_images, load_normal_test_images, load_training_images, get_training_image_paths
from geopy.distance import geodesic
from image_model_utils import extract_penultimate_features, get_anomaly_score
from plot_solution import plot_path_on_map


### Parameters ###
MAXIMUM_TRAVEL_DISTANCE: float = 100 # in km


if __name__ == "__main__":
    ### Data Loading ###
    training_images = load_training_images()
    abnormal_test_images = load_abnormal_test_images()
    normal_test_images = load_normal_test_images()
    print(f"Loaded {len(training_images)} training images")
    print(f"Loaded {len(abnormal_test_images)} abnormal test images")
    print(f"Loaded {len(normal_test_images)} normal test images")

    ### Coordinate Extraction ###
    training_coords = [get_gps_data(str(image_path)) for image_path in get_training_image_paths()]
    abnormal_test_coords = [get_gps_data(str(image_path)) for image_path in get_abnormal_test_image_paths()]
    normal_test_coords = [get_gps_data(str(image_path)) for image_path in get_normal_test_image_paths()]

    ### Feature Extraction ###
    training_features = np.array([extract_penultimate_features(image) for image in training_images])
    abnormal_test_features = np.array([extract_penultimate_features(image) for image in abnormal_test_images])
    normal_test_features = np.array([extract_penultimate_features(image) for image in normal_test_images])


    ### Scoring ###
    nn_model = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(training_features)
    abnormal_scores = np.array([get_anomaly_score(image, nn_model) for image in abnormal_test_images])
    normal_scores = np.array([get_anomaly_score(image, nn_model) for image in normal_test_images])
    print(f"Abnormal scores: {abnormal_scores}")
    print(f"Mean abnormal score: {np.mean(abnormal_scores)}")
    print(f"Normal scores: {normal_scores}")
    print(f"Mean normal score: {np.mean(normal_scores)}")

    ### Optimization Data Collection ###
    base_coordinates = generate_random_coordinates()
    coordinates = [base_coordinates] + abnormal_test_coords + normal_test_coords
    distance_matrix = [
        [geodesic(coord1, coord2).km for coord2 in coordinates]
        for coord1 in coordinates
    ]
    scores = [0] + list(abnormal_scores) + list(normal_scores)

    optimal_predicted_path = maximize_utility_with_distance_constraint(
        utilities=scores,
        distance_matrix=distance_matrix,
        D_max=MAXIMUM_TRAVEL_DISTANCE,
        start_node=0
    )

    print(f"Optimal predicted path: {optimal_predicted_path.tour}")

    plot_path_on_map(
        locations=coordinates,
        path_order=optimal_predicted_path.visited,
        save_path="optimal_path_map.png"
    )
