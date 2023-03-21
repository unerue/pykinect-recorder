import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget,
)

# from main.logger import logger
from .components.toolbar import Toolbar, SaveDirLoader
from .components.sidebar import Sidebar
from .components.sensor_viewer import SensorViewer


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Azure Kinect Camera DK")
        self.setWindowIcon(QIcon(os.path.abspath("./renderer/public/kinect-sensor.ico")))
        # fileHandler = logging.FileHandler("tools/pyk4a/example/outputs/log.txt")
        # formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] (%(filename)s:%(lineno)d) > %(message)s')
        # fileHandler.setFormatter(formatter)
        # self.logger.addHandler(fileHandler)

        self.initial_window()

    def initial_window(self) -> None:
        
        self.setFixedSize(1920, 1080)

        # toolbar Layout
        self.toolbar = Toolbar()
        
        # frame Layout
        layout_frame = QHBoxLayout()        
        self.sidebar = Sidebar()
        layout_frame.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.toolbar.btn_ml.clicked.connect(self.sidebar.vision_solution_panel.hide_panel)

        self.sensor_viewer = SensorViewer()
        # self.asidebar = SaveDirLoader()
        # self.toolbar.btn_finddir.connect(self.)        

        layout_frame.addWidget(self.sidebar)
        layout_frame.addWidget(self.sensor_viewer)
        # layout_frame.addWidget(self.asidebar)

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        layout_main.addWidget(self.toolbar)
        layout_main.addLayout(layout_frame)

        widget_main = QWidget(self)
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)