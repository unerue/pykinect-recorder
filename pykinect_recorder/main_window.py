from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QSizePolicy, QFrame, QSizeGrip

from .renderer.components.toolbar import Toolbar
from .renderer.components.sidebar_menu import SidebarMenus
from .renderer.components.sidebar_control import StackedSidebar
from .renderer.components.viewer_control import StackedViewer
from .renderer.signals import all_signals


class MainWindow(QMainWindow):
    def __init__(self, width, height) -> None:
        super().__init__()
        self.setWindowTitle("pykinect recorder")
        self.setWindowIcon(QIcon("pykinect_recorder/renderer/public/kinect-sensor.ico"))
        self.initial_window()

    def initial_window(self) -> None:
        self.setMinimumSize(QSize(1280, 720))
        self.setMaximumSize(QSize(1980, 1080))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop)

        self.toolbar = Toolbar()
        main_layout.addWidget(self.toolbar)

        main_sub_layout = QHBoxLayout()
        main_sub_layout.setSpacing(0)
        main_sub_layout.setContentsMargins(0, 0, 0, 0)
        main_sub_layout.setAlignment(Qt.AlignRight)

        self.sidebar_menus = SidebarMenus()
        self.stacked_sidebar = StackedSidebar()
        self.stacked_viewer = StackedViewer()

        self.frame_layout = QHBoxLayout()
        self.frame_size_grip = QFrame()
        self.frame_size_grip.setObjectName("frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 10))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)
        self.frame_layout.addWidget(self.frame_size_grip)
        self.frame_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        main_sub_layout.addWidget(self.sidebar_menus)
        main_sub_layout.addWidget(self.stacked_sidebar)
        main_sub_layout.addWidget(self.stacked_viewer)

        main_layout.addLayout(main_sub_layout)
        main_layout.addLayout(self.frame_layout)
        self.setCentralWidget(main_widget)

        all_signals.save_filepath.connect(self.stacked_viewer.main_viewer.setBasePath)
        all_signals.sidebar_toggle.connect(self.stacked_viewer.main_viewer.set_config)
        all_signals.stacked_sidebar_status.connect(self.stacked_sidebar.set_current_widget)
        all_signals.stacked_sidebar_status.connect(self.stacked_viewer.set_current_widget)
        all_signals.playback_filepath.connect(self.stacked_viewer.main_explorer.start_playback)
