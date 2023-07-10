import os

from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame, QPushButton,
    QMenuBar, QMenu, QApplication, QToolBar
)
import qtawesome as qta

from ..signals import all_signals
from ..common_widgets import Label
from ...pyk4a.utils import get_root


class Topbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(40)
        self.setMaximumWidth(4000)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)

        self.setObjectName("Topbar")
        self.setStyleSheet("""
            QFrame#Topbar {
                background-color: #323233; 
                padding: 0px; margin: 0px; 
                border-radius: 0px;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignLeft)

        self.label_icon = Label()
        self.label_icon.setStyleSheet("margin-left: 6px;")
        self.label_icon.setFixedSize(40, 40)
        self.icon = QIcon(os.path.join(get_root(), "renderer/public/kinect-sensor.ico"))
        self.pixmap = self.icon.pixmap(25, 25)
        self.label_icon.setPixmap(self.pixmap)
        main_layout.addWidget(self.label_icon)    

        self.menubar = QMenuBar()
        self.menubar.setFixedWidth(100)
        self.menubar.setContentsMargins(0, 0, 0, 0)
        self.menubar.setStyleSheet("""
            QMenuBar {
                font-size: 15px; 
                background-color: #323233; 
                border: none;                              
            }
            QMenuBar:item:selected {
                border-color: white;
                border-radius: 0px;                      
            }
        """)

        self.file_menu = QMenu("File")
        self.help_menu = QMenu("Help")
        self.file_menu.setContentsMargins(0, 0, 0, 0)
        self.help_menu.setContentsMargins(0, 0, 0, 0)
        
        self.exit_action = QAction("Exit")
        self.info_action = QAction("Info")

        self.file_menu.addAction(self.exit_action)
        self.help_menu.addAction(self.info_action)
        self.menubar.addMenu(self.file_menu)
        self.menubar.addMenu(self.help_menu)
        main_layout.addWidget(self.menubar)

        self.title_layout = QHBoxLayout()
        self.title_layout.setAlignment(Qt.AlignCenter)
        self.label_title = Label("pykinect-recorder", font="Arial", fontsize=12, orientation=Qt.AlignCenter)
        self.title_layout.addWidget(self.label_title)
        main_layout.addLayout(self.title_layout)

        self.right_btn_layout = QHBoxLayout()
        self.right_btn_layout.setSpacing(0)
        self.right_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = self.make_icons(qta.icon("msc.chrome-minimize"), "minimize")
        self.btn_maximize = self.make_icons(qta.icon("msc.chrome-maximize"), "maximize")
        self.btn_close = self.make_icons(qta.icon("msc.chrome-close"), "close")
        self.right_btn_layout.addWidget(self.btn_minimize)
        self.right_btn_layout.addWidget(self.btn_maximize)
        self.right_btn_layout.addWidget(self.btn_close)
        main_layout.addLayout(self.right_btn_layout)
        self.setLayout(main_layout)

        self.exit_action.triggered.connect(self.quit_window)
        self.info_action.triggered.connect(self.get_window_info)
        self.btn_minimize.clicked.connect(self.right_btn_clicked)
        self.btn_maximize.clicked.connect(self.right_btn_clicked)
        self.btn_close.clicked.connect(self.right_btn_clicked)
    
    def make_icons(self, icon: qta, tooltip: str, scale: float = 0.8) -> QPushButton:
        w, h = int(35 * scale), int(35 * scale)
        btn = QPushButton(icon, "")
        btn.setObjectName(tooltip)
        btn.setFixedSize(38, 38)
        btn.setIconSize(QSize(w, h))
        btn.setToolTip(f"<b>{tooltip}<b>")
        btn.setStyleSheet("""
            QPushButton {
                border: none; border-radius: 0px;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }             
        """)
        return btn
    
    def right_btn_clicked(self):
        all_signals.window_control.emit(self.sender().objectName())

    def quit_window(self):
        QApplication.instance().quit()

    def get_window_info(self):
        print("pass")