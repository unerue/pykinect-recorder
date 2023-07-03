import os
import platform

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QFrame, QFileDialog

from ..signals import all_signals
from ..common_widgets import PushButton, Label, VLine


class Toolbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(50)
        self.setMaximumWidth(4000)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.user_name = os.getenv("USERNAME")

        # check execution environment.
        if platform.system().startswith("Windows"):
            self.base_path = os.path.join("C", "Users", self.user_name, "Videos\\")
        else:
            self.base_path = os.path.join("home", self.user_name, "Videos\\")

        self.setObjectName("Toolbar")
        self.setStyleSheet(
            """
            QFrame#Toolbar {
                background-color: #323233; padding: 0px; margin: 0px;
            }
        """
        )

        self.label_device_status = Label("Azure Kinect Camera", orientation=Qt.AlignCenter)
        self.label_device_status.setFixedSize(170, 50)
        self.btn_finddir = PushButton("select save path", "Arial", 10)
        self.btn_finddir.setFixedSize(170, 50)
        self.label_dirpath = Label(f"  save path: {self.base_path}", orientation=Qt.AlignVCenter)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.label_device_status)
        main_layout.addWidget(VLine())
        main_layout.addWidget(self.btn_finddir)
        main_layout.addWidget(VLine())
        main_layout.addWidget(self.label_dirpath)
        self.setLayout(main_layout)

        self.btn_finddir.clicked.connect(self.search_file)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(self, "Open Data Files", self.base_path, QFileDialog.ShowDirsOnly)
        self.label_dirpath.setText(_dirNames)
        self.base_path = _dirNames
        all_signals.save_filepath.emit(self.base_path)
