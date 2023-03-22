import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, 
    QWidget, QTabWidget, QToolBar
)

from .components.toolbar import Toolbar, SaveDirLoader
from .components.viewer_sidebar import ViewerSidebar
from .components.sensor_viewer import SensorViewer
from .components.dl_sidebar import DLSidebar
from .components.custom_widgets import Label


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

        # toolbar
        self.toolbar = Toolbar()

        # frame Layout
        layout_frame = QHBoxLayout()
        self.tab_sidebar = QTabWidget()        
        self.sidebar_viewer = ViewerSidebar()
        self.sidebar_dl = DLSidebar()
        self.tab_sidebar.addTab(self.sidebar_viewer, "Viewer")
        self.tab_sidebar.addTab(self.sidebar_dl, "Deep Learning")
        self.tab_sidebar.setMovable(True)

        layout_frame.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.toolbar.btn_ml.clicked.connect(self.sidebar_viewer.vision_solution_panel.hide_panel)

        self.sensor_viewer = SensorViewer()
        self.asidebar = SaveDirLoader()
        self.toolbar.PATH.connect(self.asidebar.set_scrollArea)        

        layout_frame.addWidget(self.tab_sidebar)
        layout_frame.addWidget(self.sensor_viewer)
        layout_frame.addWidget(self.asidebar)

        layout_main = QVBoxLayout()
        layout_main.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # layout_main.addWidget(self.toolbar_sample)
        layout_main.addWidget(self.toolbar)
        layout_main.addLayout(layout_frame)

        widget_main = QWidget(self)
        widget_main.setLayout(layout_main)
        self.setCentralWidget(widget_main)