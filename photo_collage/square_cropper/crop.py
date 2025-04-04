from PIL import Image
import os

def crop_center_square(image_path, output_size=None):
    """
    Crop the largest centered square from a JPEG image and optionally resize it.
    
    Parameters:
    - image_path: str, path to the input JPEG file
    - output_size: int or None, if None, it will resize to the original square dimension (min of width/height)
    
    Returns:
    - output_path: str, path to the saved cropped JPEG image
    """
    img = Image.open(image_path)
    width, height = img.size
    min_dim = min(width, height)

    # Calculate crop box (centered)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    img_cropped = img.crop((left, top, right, bottom))

    # Resize (always)
    target_size = output_size if output_size is not None else min_dim
    img_cropped = img_cropped.resize((target_size, target_size), Image.LANCZOS)

    # Create output filename
    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_square.jpg"

    # Save with high quality
    img_cropped.save(output_path, format="JPEG", quality=95, optimize=True)
    print(f"Saved cropped image to: {output_path}")
    return output_path

