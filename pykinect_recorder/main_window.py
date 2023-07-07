import os

from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QIcon, QScreen
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget,
    QSizePolicy, QApplication
)

from .renderer.components.topbar import Topbar
from .renderer.components.sidebar_menu import SidebarMenus
from .renderer.components.sidebar_control import StackedSidebar
from .renderer.components.viewer_control import StackedViewer
from .renderer.components.statusbar import StatusBar
from .renderer.signals import all_signals
from .pyk4a.utils import get_root


class MainWindow(QMainWindow):
    def __init__(self, width, height) -> None:
        super().__init__()
        self.setWindowTitle("pykinect recorder")
        self.setWindowIcon(QIcon(os.path.join(get_root(), "renderer/public/kinect-sensor.ico")))
        self.initial_window()

    def initial_window(self) -> None:
        self.setMinimumSize(QSize(1280, 740))
        self.setMaximumSize(QSize(1550, 1080))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.is_maximize = False

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignmentFlag.AlignLeft)

        self.topbar = Topbar()
        main_layout.addWidget(self.topbar)

        main_sub_layout = QHBoxLayout()
        # main_sub_layout.setSpacing(0)
        # main_sub_layout.setContentsMargins(0, 0, 0, 0)
        main_sub_layout.setAlignment(Qt.AlignLeft)

        self.sidebar_menus = SidebarMenus()
        self.stacked_sidebar = StackedSidebar()
        # self.stacked_sidebar.setStyleSheet("border: 1px solid blue;")

        content_layout = QHBoxLayout()
        self.stacked_viewer = StackedViewer()
        # self.stacked_viewer.setStyleSheet("border: 1px solid red;")
        content_layout.addWidget(self.stacked_viewer, Qt.AlignmentFlag.AlignLeft)
        content_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        main_sub_layout.addWidget(self.sidebar_menus)
        main_sub_layout.addWidget(self.stacked_sidebar)
        main_sub_layout.addLayout(content_layout)
        main_layout.addLayout(main_sub_layout)
       
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)
        self.setCentralWidget(main_widget)

        self.topbar.mouseMoveEvent = self.moveWindow
        all_signals.window_control.connect(self.window_control)

    @Slot(str)
    def window_control(self, value):
        if value == "minimize":
            self.showMinimized()
        elif value == "maximize":
            if self.is_maximize is False:
                self.showFullScreen()
                self.is_maximize = True
            else:
                self.resize(QSize(1280, 740))
                center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
                geo = self.frameGeometry()
                geo.moveCenter(center)
                self.move(geo.topLeft())
                self.is_maximize = False
        else:
            self.close()

    def mousePressEvent(self, event) -> None:
        self.dragPos = event.globalPos()

    def moveWindow(self, event) -> None:
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
