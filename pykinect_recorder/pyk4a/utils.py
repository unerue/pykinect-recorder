import sys
import platform
from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from numpy.typing import NDArray
import open3d as o3d


def colorize(
    image: NDArray,
    clipping_range: Optional[tuple[int, int]] = (None, None),
    colormap: int = cv2.COLORMAP_HSV,
) -> NDArray:
    """Colorize image with OpenCV colormap.
    Args:
        image (NDArray[H,W]): Image to colorize.
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

def get_root() -> Path:
    """Get root path for load assets.
    Args:
        None.
    Returns:
        Path: Root Directory.
    """
    return Path(__file__).parent.parent

class Open3dVisualizer:
    def __init__(self):
        self.point_cloud = o3d.geometry.PointCloud()
        self.o3d_started = False

        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()

    def __call__(self, points_3d, rgb_image=None):
        self.update(points_3d, rgb_image)

    def update(self, points_3d, rgb_image=None):
        # Add values to vectors
        self.point_cloud.points = o3d.utility.Vector3dVector(points_3d)
        if rgb_image is not None:
            colors = cv2.cvtColor(rgb_image, cv2.COLOR_BGRA2RGB).reshape(-1, 3) / 255
            self.point_cloud.colors = o3d.utility.Vector3dVector(colors)

        self.point_cloud.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

        # Add geometries if it is the first time
        if not self.o3d_started:
            self.vis.add_geometry(self.point_cloud)
            self.o3d_started = True

        else:
            self.vis.update_geometry(self.point_cloud)

        self.vis.poll_events()
        self.vis.update_renderer()


def smooth_depth_image(depth_image, max_hole_size=10):
    """Smoothes depth image by filling the holes using inpainting method

    Parameters:
    depth_image(Image): Original depth image
    max_hole_size(int): Maximum size of hole to fill

    Returns:
    Image: Smoothed depth image

    Remarks:
    Bigger maximum hole size will try to fill bigger holes but requires longer time
    """
    mask = np.zeros(depth_image.shape, dtype=np.uint8)
    mask[depth_image == 0] = 1

    # Do not include in the mask the holes bigger than the maximum hole size
    kernel = np.ones((max_hole_size, max_hole_size), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    mask = mask - erosion

    smoothed_depth_image = cv2.inpaint(depth_image.astype(np.uint16), mask, max_hole_size, cv2.INPAINT_NS)

    return smoothed_depth_image


def get_k4a_module_path():
    # Check if running in Jetson Nano or similar ARM chips
    if platform.machine().lower() == "aarch64":
        return r"/usr/lib/aarch64-linux-gnu/libk4a.so"

    # For non-Arm chips, first check if it is running linux
    if platform.system().lower() == "linux":
        return r"/usr/lib/x86_64-linux-gnu/libk4a.so"

    # In Windows check the architecture
    if platform.machine().lower() == "amd64":
        return "C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\amd64\\release\\bin\\k4a.dll"

    # Otherwise return the x86 Windows version
    return "C:\\Program Files\\Azure Kinect SDK v1.4.1\\sdk\\windows-desktop\\x86\\release\\bin\\k4a.dll"


def get_k4abt_module_path():
    # Check if running in Jetson Nano or similar ARM chips
    if platform.machine().lower() == "aarch64":
        print(
            "Kinect Body Tracking is not implemented yet in ARM. Check https://feedback.azure.com/forums/920053 for more info."
        )
        sys.exit(1)

    # For non-Arm chips, first check if it is running linux
    if platform.system().lower() == "linux":
        return "libk4abt.so"

    # Otherwise return the Windows version
    return "C:\\Program Files\\Azure Kinect Body Tracking SDK\\sdk\\windows-desktop\\amd64\\release\\bin\\k4abt.dll"


def get_k4arecord_module_path(modulePath):
    return modulePath.replace("k4a", "k4arecord")


def get_k4abt_lite_model_path():
    # Check if it is a Linux system
    if platform.system().lower() == "linux":
        return None

    # Return the Windows version
    return "C:/Program Files/Azure Kinect Body Tracking SDK/sdk/windows-desktop/amd64/release/bin/dnn_model_2_0_lite_op11.onnx".encode(
        "utf-8"
    )


def get_dict(struct):
    result = {}
    for field, _ in struct._fields_:
        value = getattr(struct, field)
        # if the type is not a primitive and it evaluates to False ...
        if (type(value) not in [int, float, bool]) and not bool(value):
            # it's a null pointer
            value = None
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # Probably an array
            value = np.array(list(value))
        elif hasattr(value, "_fields_"):
            # Probably another struct
            value = get_dict(value)
        result[field] = value
    return result
