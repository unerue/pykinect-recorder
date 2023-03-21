import os
from pathlib import Path

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame, QWidget,
    QVBoxLayout, QScrollArea, QFileDialog
)
from .custom_buttons import PushButton, Label


class Toolbar(QFrame):
    PATH = Signal(str)
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
        self.PATH.emit(self.base_path)
        
    def option(self) -> None:
        pass


class SaveDirLoader(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: black;
        """)
        self.setFixedWidth(380)
        self.layout_main = QVBoxLayout()
        self.layout_scroll = QScrollArea()
        
    @Slot(str)
    def set_scrollArea(self, filedirs: str) -> None:
        layout_file = QVBoxLayout()
        for filedir in Path(filedirs).iterdir():
            fileinfo = _FileInfo()
            filename = str(filedir).split("\\")[-1]
            fileinfo.label_name.setText(filename)
            fileinfo.label_stor.setText(str(os.path.getsize(filedir)))

            layout_file.addWidget(fileinfo)
        
        self.layout_scroll.setLayout(layout_file)
        self.layout_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_main.addWidget(self.layout_scroll)
        self.setLayout(self.layout_main)


class _FileInfo(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(
            "border-color: white;" "color: white;"
        )
        layout_main = QHBoxLayout()
        self.label_name = Label("파일 이름", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        self.label_stor = Label("총 용량", "Arial", 10, Qt.AlignmentFlag.AlignCenter)

        layout_main.addWidget(self.label_name)
        layout_main.addWidget(self.label_stor)

        self.setFixedSize(340,100)
        self.setLayout(layout_main)
