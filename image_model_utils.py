from torchvision import transforms
import numpy as np
from torchvision.models import resnet18
from PIL import Image
import torch.nn as nn
from sklearn.neighbors import NearestNeighbors
import torch

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