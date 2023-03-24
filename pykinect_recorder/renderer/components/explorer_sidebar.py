import os
from pathlib import Path

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QScrollArea, 
    QPushButton, QHBoxLayout, QFileDialog
)
from .custom_widgets import Label, PushButton


class ExplorerSidebar(QFrame):
    Filepath = Signal(str)
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: #242c33;")
        
        self.layout_main = QVBoxLayout()
        self.layout_title = QHBoxLayout()
        self.base_path = None
        # title
        self.label_dirpath = Label("")
        self.label_dirpath.setFixedSize(200, 50)
        self.btn_search = PushButton("경로\n탐색")
        self.btn_search.setFixedSize(50, 50)
        self.layout_title.addWidget(self.label_dirpath)
        self.layout_title.addWidget(self.btn_search)
        self.btn_search.clicked.connect(self.search_file)
        
        # scroll area
        self.layout_scroll = QScrollArea()
        self.layout_scroll.setWidgetResizable(True)

        self.layout_main.addLayout(self.layout_title)
        self.layout_main.addWidget(self.layout_scroll)
        self.setMaximumHeight(970)
        self.setFixedWidth(300)
        self.setLayout(self.layout_main)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(
            self, 
            "Open Data Files", 
            ".",
            QFileDialog.ShowDirsOnly
        )
        self.base_path = _dirNames
        self.label_dirpath.setText(_dirNames)
        self.set_scrollArea(_dirNames)

    def set_scrollArea(self, filedirs: str) -> None:
        self._widget = QWidget()
        layout_file = QVBoxLayout()

        for filedir in Path(filedirs).iterdir():
            _filename = str(filedir).split("\\")[-1]
            if _filename[-4:] == '.mkv':
                fileinfo = _FileInfo()
                fileinfo.label_name.setText(_filename)
                fsize = os.path.getsize(filedir) / (2**30)  # byte -> GB
                fileinfo.label_stor.setText("파일 크기 : %.2fGB" %(fsize))
                layout_file.addWidget(fileinfo)
                fileinfo.Filename.connect(self.emit_file_path)

        self._widget.setLayout(layout_file)
        self.layout_scroll.setWidget(self._widget)

    @Slot(str)
    def emit_file_path(self, filename) -> None:
        tmp = f"{self.base_path}/{filename}"
        tmp = tmp.replace('\\', '/')
        self.Filepath.emit(tmp)
        

class _FileInfo(QPushButton):
    Filename = Signal(str)
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(240,100)
        self.setStyleSheet(
            "border-color: white;"
        )

        layout_main = QVBoxLayout()
        self.label_name = Label("파일 이름", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        self.label_stor = Label("총 용량", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        self.label_name.setWordWrap(True)

        layout_main.addWidget(self.label_name)
        layout_main.addWidget(self.label_stor)
        self.setLayout(layout_main)
        self.clicked.connect(self.emitName)
    
    def emitName(self) -> None:
        self.Filename.emit(self.label_name.text())
    