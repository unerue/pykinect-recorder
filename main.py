import sys

import pyk4a
import qdarktheme
from renderer.main_window import MainWindow
from PySide6.QtWidgets import QApplication


CONFIG = pyk4a.Config(
    color_format=pyk4a.ImageFormat.COLOR_BGRA32,
    depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
    color_resolution=pyk4a.ColorResolution.RES_720P,
    synchronized_images_only=True,
)


if __name__ == "__main__":
    app = QApplication()
    qdarktheme.setup_theme()
    main_window = MainWindow(CONFIG)
    main_window.show()
    app.exec()
