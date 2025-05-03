import numpy as np
from path_utils import load_training_images
from image_model_utils import extract_penultimate_features

if __name__ == "__main__":
    ### Data Loading ###
    training_images = load_training_images()
    print(f"Loaded {len(training_images)} training images")

    ### Feature Extraction ###
    training_features = np.array([extract_penultimate_features(image) for image in training_images])

    ### Serialization ###
    np.save("training_features.npy", training_features)