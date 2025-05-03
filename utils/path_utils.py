from pathlib import Path
import numpy as np
import torch
from torchvision.models import resnet18
import polars as pl
import glob
import os
from PIL import Image

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

def get_case_study_image_paths() -> list[Path]:
    image_files = glob.glob(os.path.join("case_study_data", "*"))
    return [Path(image_file) for image_file in image_files]

def load_training_images() -> list[Image.Image]:
    return load_images(get_training_image_paths())

def load_abnormal_test_images() -> list[Image.Image]:
    return load_images(get_abnormal_test_image_paths())


def load_normal_test_images() -> list[Image.Image]:
    return load_images(get_normal_test_image_paths())


def load_case_study_images() -> list[Image.Image]:
    return load_images(get_case_study_image_paths())