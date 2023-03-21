import os
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame, QGridLayout,
    QVBoxLayout, QScrollArea, QFileDialog
)
from .custom_buttons import PushButton, Label


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
        self.btn_ml = PushButton("ML Solution", "Arial", 10)
        btn_option.clicked.connect(self.option)

        layout_main = QHBoxLayout()
        layout_option = QHBoxLayout()
        layout_option.addWidget(btn_option)
        layout_option.addWidget(self.btn_ml)
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


class SaveDirLoader(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: black;
        """)
        self.setFixedWidth(380)

        layout_main = QVBoxLayout()
        layout_title = QGridLayout()
        
        self.label_name = Label("파일 경로", orientation=Qt.AlignmentFlag.AlignCenter)
        self.label_name.setFixedSize(180, 50)
        self.label_name.setStyleSheet("""
            border-color: white;
        """)
        self.label_filepath = Label("asdasd")
        self.label_filepath.setFixedSize(180, 50)
        self.label_filepath.setStyleSheet("""
            border-color: white;
        """)
        layout_title.addWidget(self.label_name, 0, 0)
        layout_title.addWidget(self.label_filepath, 0, 1)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout_scroll = QScrollArea()
        self.layout_file = QVBoxLayout()
        self.layout_scroll.setLayout(self.layout_file)
        
        self.layout_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout_main.addLayout(layout_title)
        layout_main.addWidget(self.layout_scroll)

        self.setLayout(layout_main)
