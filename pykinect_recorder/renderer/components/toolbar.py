import os
import cv2
import platform

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QHBoxLayout, QFrame, QFileDialog

from ..common_widgets import PushButton, Label
from ..signals import all_signals


class Toolbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumWidth(1980)
        self.setMaximumHeight(50)
        self.setContentsMargins(0, 0, 0, 0)
        self.user_name = os.getenv('USERNAME')
        
        # check execution environment.
        if platform.system().startswith("Windows"):
            self.base_path = os.path.join("C", "Users", self.user_name, "Videos\\")
        else:
            self.base_path = os.path.join("home", self.user_name, "Videos\\")

        self.setObjectName("Toolbar")
        self.setStyleSheet("""
            QFrame#Toolbar {
                background-color: #323233; padding: 0px; margin: 0px;
            }
        """)

        self.label_device_status = Label("Azure Kinect Camera", orientation=Qt.AlignCenter)
        self.label_device_status.setStyleSheet(" border-color: #3f4042; ")
        self.label_device_status.setFixedWidth(170)

        self.label_user_name = Label(" ".join(["User name:", self.user_name]), orientation=Qt.AlignCenter)
        self.label_user_name.setStyleSheet(" border-color: #3f4042; ")
        self.label_user_name.setFixedWidth(170)

        self.btn_finddir = PushButton("Select save path", "Arial", 10)
        self.btn_finddir.setFixedWidth(170)
        self.btn_finddir.clicked.connect(self.search_file)
        self.label_dirpath = Label(f"Save path: {self.base_path}", orientation=Qt.AlignLeft)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label_device_status)
        main_layout.addWidget(self.label_user_name)
        main_layout.addWidget(self.btn_finddir)
        main_layout.addWidget(self.label_dirpath)
        self.setLayout(main_layout)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(
            self, 
            "Open Data Files", 
            self.base_path, 
            QFileDialog.ShowDirsOnly
        )
        self.label_dirpath.setText(_dirNames)
        self.base_path = _dirNames
        all_signals.save_filepath.emit(self.base_path)