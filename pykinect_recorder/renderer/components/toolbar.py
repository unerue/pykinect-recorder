import os
from pathlib import Path

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame, QWidget, QPushButton,
    QVBoxLayout, QScrollArea, QFileDialog
)
from ..common_widgets import PushButton, Label


class Toolbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(1900, 50)
        self.base_path = f"C:\\Users\\{os.getenv('USERNAME')}\\Videos\\"
        self.setObjectName("Toolbar")
        self.setStyleSheet("""
            QFrame#Toolbar {
                background-color: #3e4d59; padding: 0px; margin: 0px;
            }
        """)

        self.btn_finddir = PushButton("경로 지정", "Arial", 10)
        self.btn_finddir.setFixedWidth(300)
        self.btn_finddir.clicked.connect(self.search_file)
        self.label_dirpath = Label(f"{self.base_path}", orientation=Qt.AlignmentFlag.AlignLeft)

        btn_option = PushButton("옵션", "Arial", 10)
        btn_option.clicked.connect(self.option)

        layout_main = QHBoxLayout()
        layout_option = QHBoxLayout()
        layout_option.addWidget(btn_option)
        layout_option.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout_main.addWidget(self.btn_finddir)
        layout_main.addWidget(self.label_dirpath)
        layout_main.addLayout(layout_option)
        self.setLayout(layout_main)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(
            self, 
            "Open Data Files", 
            self.base_path,
            QFileDialog.ShowDirsOnly
        )
        self.label_dirpath.setText(_dirNames)
        self.base_path = _dirNames
        
    def option(self) -> None:
        pass