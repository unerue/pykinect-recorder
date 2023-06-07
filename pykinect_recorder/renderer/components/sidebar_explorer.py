import os
from glob import glob
from pathlib import Path

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QScrollArea, 
    QPushButton, QHBoxLayout, QFileDialog
)
from ..common_widgets import Label, PushButton
from ..signals import all_signals


class ExplorerSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: #252526;")
        
        self.layout_main = QVBoxLayout()
        self.layout_title = QHBoxLayout()
        self.base_path = os.path.join(Path.home(), "Videos/")
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
        self.setMaximumHeight(1080)
        self.setFixedWidth(300)
        self.setLayout(self.layout_main)
        self.set_scrollarea(self.base_path)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(
            self, 
            "Open Data Files", 
            ".",
            QFileDialog.ShowDirsOnly
        )
        print(_dirNames)
        self.base_path = _dirNames
        self.label_dirpath.setText(_dirNames)
        self.set_scrollarea(_dirNames)

    def set_scrollarea(self, filedirs: str) -> None:
        self._widget = QWidget()
        layout_file = QVBoxLayout()
        layout_file.setAlignment(Qt.AlignmentFlag.AlignTop)

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
        tmp = os.path.join(self.base_path, filename)
        all_signals.playback_filepath.emit(tmp)
        

class _FileInfo(QPushButton):
    Filename = Signal(str)
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(240,100)
        self.setObjectName("FileInfo")
        self.setStyleSheet("""
            QPushButton#FileInfo {
                border-color: white;
            }
            QPushButton#FileInfo:hover {
                border-color: red;
            }
        """)

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
    