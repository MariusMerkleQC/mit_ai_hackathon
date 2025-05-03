import numpy as np
from sklearn.neighbors import NearestNeighbors
from utils.coordinate_utils import get_gps_data
from generate_random_coordinates import generate_random_coordinates
from optimization_problem import maximize_utility_with_distance_constraint
from utils.path_utils import get_case_study_image_paths, load_case_study_images
from geopy.distance import geodesic
from utils.image_model_utils import extract_penultimate_features, get_anomaly_score
from plot_solution import plot_path_on_map


### Parameters ###
MAXIMUM_TRAVEL_DISTANCE: float = 100 # in km


if __name__ == "__main__":
    case_study_images = load_case_study_images()
    print(f"Loaded {len(case_study_images)} case study images")

    ### Coordinate Extraction ###
    coords = [get_gps_data(str(image_path)) for image_path in get_case_study_image_paths()]
    features = np.array([extract_penultimate_features(image) for image in case_study_images])

    ### Scoring ###
    training_features = np.load("training_features.npy")
    nn_model = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(training_features)
    scores = np.array([get_anomaly_score(image, nn_model) for image in case_study_images])

    ### Optimization Data Collection ###
    base_coordinates = generate_random_coordinates()
    coordinates = [base_coordinates] + coords
    distance_matrix = [
        [geodesic(coord1, coord2).km for coord2 in coordinates]
        for coord1 in coordinates
    ]
    scores = [0] + scores

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
