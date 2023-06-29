from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from .renderer.components.toolbar import Toolbar
from .renderer.components.sidebar_menu import SidebarMenus
from .renderer.components.sidebar_control import StackedSidebar
from .renderer.components.viewer_control import StackedViewer
from .renderer.signals import all_signals


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("pykinect recorder")
        self.setWindowIcon(QIcon("pykinect_recorder/renderer/public/kinect-sensor.ico"))
        self.initial_window()

    def initial_window(self) -> None:
        self.setFixedSize(1280, 720)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.toolbar = Toolbar()
        main_layout.addWidget(self.toolbar)

        main_sub_layout = QHBoxLayout()
        main_sub_layout.setSpacing(0)
        main_sub_layout.setContentsMargins(0, 0, 0, 0)
        main_sub_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.sidebar_menus = SidebarMenus()
        self.stacked_sidebar = StackedSidebar()
        self.stacked_viewer = StackedViewer()

        all_signals.save_filepath.connect(self.stacked_viewer.main_viewer.setBasePath)
        all_signals.config_viewer.connect(self.stacked_viewer.main_viewer.setConfig)
        all_signals.stacked_sidebar_status.connect(self.stacked_sidebar.setCurrentWidget)
        all_signals.stacked_sidebar_status.connect(self.stacked_viewer.setCurrentWidget)
        all_signals.playback_filepath.connect(self.stacked_viewer.main_explorer.start_playback)

        main_sub_layout.addWidget(self.sidebar_menus)
        main_sub_layout.addWidget(self.stacked_sidebar)
        main_sub_layout.addWidget(self.stacked_viewer)

        main_layout.addLayout(main_sub_layout)
        self.setCentralWidget(main_widget)
