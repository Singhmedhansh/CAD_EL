from typing import Tuple
from PIL import Image
import numpy as np

WOOD_HUE_RANGE = (15, 45)  # approx brown/orange hues in HSV (0-180 scale if using OpenCV), here we'll compute simplistic hue-like
METAL_HUE_RANGE = (180, 240)  # gray/silver/metallic hues


def load_image(path: str) -> Image.Image:
    """Load an image (PNG or JPEG) and convert to RGB."""
    img = Image.open(path)
    if img.format not in ("PNG", "JPEG", "JPG"):
        raise ValueError("Input image must be PNG or JPEG format")
    return img.convert("RGB")


def average_color(img: Image.Image) -> Tuple[float, float, float]:
    arr = np.array(img)
    # Downsample for speed
    if arr.shape[0] * arr.shape[1] > 1_000_000:
        img_small = img.resize((800, int(800 * img.height / img.width)))
        arr = np.array(img_small)
    # Compute mean RGB
    mean_rgb = arr.reshape(-1, 3).mean(axis=0)
    return tuple(mean_rgb.tolist())


def rgb_to_hsv(rgb: Tuple[float, float, float]) -> Tuple[float, float, float]:
    r, g, b = [x / 255.0 for x in rgb]
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx - mn

    # Hue
    if df == 0:
        h = 0.0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    else:
        h = (60 * ((r - g) / df) + 240) % 360

    # Saturation
    s = 0.0 if mx == 0 else df / mx
    # Value
    v = mx
    return h, s, v


def looks_wood_like(img: Image.Image) -> bool:
    mean_rgb = average_color(img)
    h, s, v = rgb_to_hsv(mean_rgb)
    # Map to rough brown range: ~15-45 degrees on 0-360 hue
    return 15 <= h <= 45 and s >= 0.2 and v >= 0.2


def looks_metallic(img: Image.Image) -> bool:
    """Detect if image looks metallic/mechanical (gray, silver tones with low saturation)."""
    mean_rgb = average_color(img)
    h, s, v = rgb_to_hsv(mean_rgb)
    # Metallic: low saturation (grayish) and moderate to high value
    return s <= 0.3 and v >= 0.3


def detect_component_type(img: Image.Image) -> str:
    """Detect whether image shows wood, metal/mechanical, or other component."""
    if looks_metallic(img):
        return "mechanical"
    elif looks_wood_like(img):
        return "wood"
    else:
        return "unknown"
