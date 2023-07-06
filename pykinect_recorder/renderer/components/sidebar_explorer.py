import os
from pathlib import Path

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QFileDialog
)

from ..common_widgets import Label, PushButton
from ..signals import all_signals


class ExplorerSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: #252526;")

        self.main_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.base_path = os.path.join(Path.home(), "Videos/")

        self.label_dirpath = Label("")
        self.label_dirpath.setFixedSize(180, 50)
        self.btn_search = PushButton("search\npath")

        self.btn_search.setFixedSize(70, 50)
        self.title_layout.addWidget(self.label_dirpath)
        self.title_layout.addWidget(self.btn_search)
        self.btn_search.clicked.connect(self.search_file)

        self.layout_scroll = QScrollArea()
        self.layout_scroll.setWidgetResizable(True)

        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.layout_scroll)
        self.setMaximumHeight(1080)
        self.setFixedWidth(300)
        self.setLayout(self.main_layout)
        self.set_scrollarea(self.base_path)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(self, "Open Data Files", ".", QFileDialog.ShowDirsOnly)
        self.base_path = _dirNames
        self.label_dirpath.setText(_dirNames)  # /etc/ssh/, /etc/ssh/config.txt
        self.set_scrollarea(_dirNames)

    def set_scrollarea(self, filedirs: str) -> None:
        self._widget = QWidget()
        layout_file = QVBoxLayout()
        layout_file.setAlignment(Qt.AlignmentFlag.AlignTop)

        for filedir in Path(filedirs).iterdir():
            _filename = str(filedir).split("\\")[-1]
            if _filename[-4:] == ".mkv":
                fileinfo = _FileInfo()
                fileinfo.label_name.setText(_filename)
                fsize = os.path.getsize(filedir) / (2**30)  # byte -> GB
                fileinfo.label_store.setText("File volume : %.2fGB" % (fsize))
                layout_file.addWidget(fileinfo)
                fileinfo.Filename.connect(self.emit_file_path)

        self._widget.setLayout(layout_file)
        self.layout_scroll.setWidget(self._widget)

    @Slot(str)
    def emit_file_path(self, filename) -> None:
        tmp = os.path.join(self.base_path, filename)
        all_signals.playback_signals.playback_filepath.emit(tmp)


class _FileInfo(QPushButton):
    Filename = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(240, 100)
        self.setObjectName("FileInfo")
        self.setStyleSheet(
            """
            QPushButton#FileInfo {
                border-color: white;
            }
            QPushButton#FileInfo:hover {
                border-color: red;
            }
        """
        )

        layout_main = QVBoxLayout()
        # playback = Playback(filepath)
        # playback

        self.label_name = Label("File name: ", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        self.label_store = Label("Total Volume: ", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        self.label_name.setWordWrap(True)

        layout_main.addWidget(self.label_name)
        layout_main.addWidget(self.label_store)
        self.setLayout(layout_main)
        self.clicked.connect(self.emitName)

    def emitName(self) -> None:
        self.Filename.emit(self.label_name.text())
