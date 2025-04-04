from PIL import Image
from typing import Tuple, List
from sklearn.cluster import KMeans
import numpy as np
import os
from PIL import ImageDraw

def save_dominant_color_square(image_path: str, size: int = 256) -> str:
    """
    Creates and saves a solid-color square image using the dominant color of the input image.

    Parameters:
    - image_path: str: Path to the original image.
    - size: int: Width and height of the output square image.

    Returns:
    - str: Path to the saved solid-color image.
    """
    dominant_color = get_dominant_color(image_path)

    solid_img = Image.new("RGB", (size, size), dominant_color)

    base, _ = os.path.splitext(image_path)
    output_path = f"{base}_dominant.jpg"
    solid_img.save(output_path, format="JPEG", quality=95, optimize=True)

    return output_path

def save_top4_color_grid(image_path: str, size: int = 256) -> str:
    """
    Creates and saves a 2x2 grid image showing the top 4 dominant colors of the input image.

    Parameters:
    - image_path: str: Path to the original image.
    - size: int: Width and height of the output grid image.

    Returns:
    - str: Path to the saved 2x2 grid image.
    """

    colors = get_top_colors(image_path, n_colors=4)
    block_size = size // 2

    # Create new blank image
    img = Image.new("RGB", (size, size))

    # Define positions
    positions = [
        (0, 0),                      # top-left
        (block_size, 0),             # top-right
        (0, block_size),             # bottom-left
        (block_size, block_size),    # bottom-right
    ]

    # Draw rectangles
    for color, pos in zip(colors, positions):
        square = Image.new("RGB", (block_size, block_size), color)
        img.paste(square, pos)

    base, _ = os.path.splitext(image_path)
    output_path = f"{base}_top4.jpg"
    img.save(output_path, format="JPEG", quality=95, optimize=True)

    return output_path


def get_top_colors(image_path: str, n_colors: int = 3, resize: int = 50) -> List[Tuple[int, int, int]]:
    """
    Uses KMeans clustering to extract the top N most dominant colors from an image.

    Parameters:
    - image_path: str: Path to the input image.
    - n_colors: int: Number of dominant colors to return.
    - resize: int: Resize dimension to reduce pixel noise and speed up clustering.

    Returns:
    - List[Tuple[int, int, int]]: List of dominant RGB colors sorted by dominance.
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize((resize, resize))
    pixels = np.array(img).reshape(-1, 3)

    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init='auto')
    kmeans.fit(pixels)
    cluster_centers = kmeans.cluster_centers_
    labels = kmeans.labels_

    # Count how many pixels fall into each cluster
    counts = np.bincount(labels)

    # Sort clusters by frequency
    sorted_indices = np.argsort(-counts)
    sorted_colors = [tuple(map(int, cluster_centers[i])) for i in sorted_indices]

    return sorted_colors

def get_dominant_color(image_path: str, resize: int = 50) -> Tuple[int, int, int]:
    """
    Returns the single most dominant RGB color from an image using KMeans.

    Parameters:
    - image_path: str: Path to the image.
    - resize: int: Resize dimension for clustering.

    Returns:
    - Tuple[int, int, int]: Dominant RGB color.
    """
    return get_top_colors(image_path, n_colors=1, resize=resize)[0]
