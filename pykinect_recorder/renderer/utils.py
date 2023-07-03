from typing import Optional, Tuple
import cv2
import numpy as np
from numpy.typing import NDArray


def colorize(
    image: NDArray,
    clipping_range: Optional[tuple[int, int]] = (None, None),
    colormap: int = cv2.COLORMAP_HSV,
) -> NDArray:
    """Colorize image with OpenCV colormap.
    Args:
        image (NDArray): Image to colorize.
        clipping_range (Optional[tuple[int, int]], optional): Clipping range for image. Defaults to (None, None).
        colormap (int, optional): OpenCV colormap. Defaults to cv2.COLORMAP_HSV.
    Returns:
        NDArray: Colorized image.
    """
    if clipping_range[0] or clipping_range[1]:
        image = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
    else:
        image = image.copy()
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    image = cv2.applyColorMap(image, colormap)
    return image
