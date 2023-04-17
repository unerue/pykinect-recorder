import os

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QImage
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget
)

from .renderer.components.sidebar_menu import SidebarMenus
from .renderer.components.toolbar import Toolbar
from .renderer.components.sidebar_tab import Sidebar
from .renderer.components.asidebar import Asidebar
from .renderer.components.viewer_sensors import SensorViewer


class AllSignals:
    def __init__(self):
        # Thread Signals
        self.captured_rgb = Signal(QImage)
        self.captured_depth = Signal(QImage)
        self.captured_ir = Signal(QImage)
        self.captured_time = Signal(float)
        self.captured_acc_data = Signal(list)
        self.captured_yyro_data = Signal(list)
        self.captured_fps = Signal(float)

        # Remain Signals
        self.playback_filepath = Signal(str)



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Azure Kinect Camera DK")
        self.setWindowIcon(QIcon(os.path.abspath("./renderer/public/kinect-sensor.ico")))
        self.initial_window()

    def initial_window(self) -> None:
        self.setFixedSize(1920, 1080)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.toolbar = Toolbar()
        main_layout.addWidget(self.toolbar)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        main_sub_layout = QHBoxLayout()
        main_sub_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.tab_sidebar = Sidebar()
        self.sensor_viewer = SensorViewer()
        self.asidebar = Asidebar()
        self.tab_sidebar.ToggleSign.connect(self.asidebar.toggle_hide)
        self.tab_sidebar.sidebar_explorer.Filepath.connect(self.sensor_viewer.playback)

        main_sub_layout.addWidget(SidebarMenus())
        main_sub_layout.addWidget(self.tab_sidebar)
        main_sub_layout.addWidget(self.sensor_viewer)
        main_sub_layout.addWidget(self.asidebar)


        main_layout.addLayout(main_sub_layout)
        self.setCentralWidget(main_widget)
