from pathlib import Path
import numpy as np
import torch
from torchvision.models import resnet18
import polars as pl
import glob
import os
from PIL import Image
from torchvision import transforms
import torch.nn as nn
from sklearn.neighbors import NearestNeighbors


def load_image(image_path: Path) -> Image.Image:
    image = Image.open(image_path)
    image = image.convert("RGB")
    return image


def load_images(image_paths: list[Path]) -> list[Image.Image]:
    return [load_image(image_path) for image_path in image_paths]


def get_training_image_paths() -> list[Path]:
    image_files = glob.glob(os.path.join("data/training", "*"))
    return [Path(image_file) for image_file in image_files]

def get_abnormal_test_image_paths() -> list[Path]:
    image_files = glob.glob(os.path.join("data/test/abnormal", "*"))
    return [Path(image_file) for image_file in image_files]

def get_normal_test_image_paths() -> list[Path]:
    image_files = glob.glob(os.path.join("data/test/normal", "*"))
    return [Path(image_file) for image_file in image_files]

def load_training_images() -> list[Image.Image]:
    return load_images(get_training_image_paths())

def load_abnormal_test_images() -> list[Image.Image]:
    return load_images(get_abnormal_test_image_paths())


def load_normal_test_images() -> list[Image.Image]:
    return load_images(get_normal_test_image_paths())

def extract_penultimate_features(image: Image.Image) -> np.ndarray:
    preprocessor = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    model = resnet18()
    model = nn.Sequential(*list(model.children())[:-1])

    processed_image = preprocessor(image).unsqueeze(0)
    with torch.no_grad():
        features = model(processed_image)
    features = features.squeeze().numpy()
    return features

def get_anomaly_score(image: Image.Image, nn_model: NearestNeighbors) -> float:
    image_features = extract_penultimate_features(image)
    distances, _ = nn_model.kneighbors(X=image_features.reshape(1, -1), return_distance=True)
    anomaly_score = np.mean(distances)
    return anomaly_score



if __name__ == "__main__":
    ### Data Loading ###
    training_images = load_training_images()
    abnormal_test_images = load_abnormal_test_images()
    normal_test_images = load_normal_test_images()
    print(f"Loaded {len(training_images)} training images")
    print(f"Loaded {len(abnormal_test_images)} abnormal test images")
    print(f"Loaded {len(normal_test_images)} normal test images")

    ### Feature Extraction ###
    training_features = np.array([extract_penultimate_features(image) for image in training_images])
    abnormal_test_features = np.array([extract_penultimate_features(image) for image in abnormal_test_images])
    normal_test_features = np.array([extract_penultimate_features(image) for image in normal_test_images])

    nn_model = NearestNeighbors(n_neighbors=5, algorithm='auto').fit(training_features)
    abnormal_scores = np.array([get_anomaly_score(image, nn_model) for image in abnormal_test_images])
    normal_scores = np.array([get_anomaly_score(image, nn_model) for image in normal_test_images])
    print(f"Abnormal scores: {abnormal_scores}")
    print(f"Mean abnormal score: {np.mean(abnormal_scores)}")
    print(f"Normal scores: {normal_scores}")
    print(f"Mean normal score: {np.mean(normal_scores)}")