import os
import cv2
import datetime
from pathlib import Path

import qtawesome as qta
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QScrollArea, 
    QPushButton, QHBoxLayout, QFileDialog
)

from ..common_widgets import Label
from ..signals import all_signals
from ...pyk4a.pykinect import start_playback, initialize_libraries


class ExplorerSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        initialize_libraries()
        self.setStyleSheet(" background-color: #252526; border-radius: 0px; ")

        self.main_layout = QVBoxLayout()
        self.title_layout = QHBoxLayout()
        self.base_path = os.path.join(Path.home(), "Videos")

        self.label_dirpath = Label(self.base_path)
        self.label_dirpath.setFixedSize(180, 50)
        
        self.btn_reload = self.make_icons(qta.icon("mdi6.reload"), "Reload", scale=0.7)
        self.btn_search = self.make_icons(qta.icon("ri.search-line"), "Search directory", scale=0.7)

        self.title_layout.addWidget(self.label_dirpath)
        self.title_layout.addWidget(self.btn_reload)
        self.title_layout.addWidget(self.btn_search)

        self.layout_scroll = QScrollArea()
        self.layout_scroll.setWidgetResizable(True)
        self.layout_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.layout_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.main_layout.addLayout(self.title_layout)
        self.main_layout.addWidget(self.layout_scroll)
        self.setMaximumHeight(1080)
        self.setFixedWidth(300)
        self.setLayout(self.main_layout)
        self.set_scrollarea(self.base_path)

        self.btn_reload.clicked.connect(self.reload_dir)
        self.btn_search.clicked.connect(self.search_dir)

    def reload_dir(self) -> None:
        self.set_scrollarea(self.base_path)

    def search_dir(self) -> None:
        self.base_path = QFileDialog.getExistingDirectory(self, "Open Data Files", ".", QFileDialog.ShowDirsOnly)
        self.label_dirpath.setText(self.base_path)  # /etc/ssh/ or /etc/ssh/config.txt
        self.set_scrollarea(self.base_path)

    def set_scrollarea(self, filedirs: str) -> None:
        self._widget = QWidget()
        layout_file = QVBoxLayout()
        layout_file.setAlignment(Qt.AlignmentFlag.AlignTop)

        for filedir in Path(filedirs).iterdir():
            _filename = str(filedir).split("\\")[-1]
            if _filename[-4:] == ".mkv":
                try:
                    fileinfo = _FileInfo()
                    playback = start_playback(str(filedir))
                    handle = playback.get_record_configuration()._handle
                    start_time = handle.start_timestamp_offset_usec

                    # Thumbnail
                    # playback.seek_timestamp(start_time)
                    # _, current_frame = playback.update()
                    # rgb_frame = current_frame.get_color_image()
                    # thumbnail = cv2.cvtColor(rgb_frame[1], cv2.COLOR_BGR2RGB)
                    # thumbnail = QImage(thumbnail, 30, 30, 30*3, QImage.Format_RGB888)
                    # fileinfo.label_thumbnail.setPixmap(QPixmap.fromImage(thumbnail))
                    
                    record_length = (playback.get_recording_length()-start_time) // 1e6
                    fsize = os.path.getsize(filedir) / (2**30)
                    record_time = str(datetime.timedelta(seconds=record_length))
                    playback.close()
                    
                    font_metrics = fileinfo.label_file_name.fontMetrics()
                    elided_text = font_metrics.elidedText(_filename, Qt.ElideRight, fileinfo.label_file_name.width())
                    fileinfo.label_file_name.setText(elided_text)
                    fileinfo.label_metadata.setText(f"{record_time} ({fsize:.2f}GB)")
                    layout_file.addWidget(fileinfo)
                    fileinfo.Filename.connect(self.emit_file_path)
                except:
                    pass

        self._widget.setLayout(layout_file)
        self.layout_scroll.setWidget(self._widget)
    
    def make_icons(self, icon: qta, tooltip: str, scale: float = 0.8) -> QPushButton:
        w, h = int(35 * scale), int(35 * scale)
        btn = QPushButton(icon, "")
        btn.setObjectName(tooltip)
        btn.setFixedSize(40, 40)
        btn.setIconSize(QSize(w, h))
        btn.setToolTip(f"<b>{tooltip}<b>")
        btn.setStyleSheet("""
            QPushButton {
                border-radius: 0px;
            }
            QPushButton:hover {
                border-color: white;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)
        return btn

    @Slot(str)
    def emit_file_path(self, filename) -> None:
        tmp = os.path.join(self.base_path, filename)
        all_signals.playback_signals.playback_filepath.emit(tmp)


class _FileInfo(QPushButton):
    Filename = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(240, 60)
        self.setObjectName("FileInfo")
        self.setStyleSheet(
            """
            QPushButton#FileInfo {
                border-color: white;
                border-radius: 0px;
            }
            QPushButton#FileInfo:hover {
                border-color: red;
            }
        """
        )

        main_layout = QVBoxLayout()
        self.thumbnail_layout = QHBoxLayout()
        # self.label_thumbnail = Label()
        self.label_file_name = Label("File name: ", "Arial", 10, Qt.AlignLeft)
        self.label_file_name.setWordWrap(True)
        # self.label_file_name.setFixedWidth(240)
        # self.thumbnail_layout.addWidget(self.label_thumbnail)
        self.thumbnail_layout.addWidget(self.label_file_name)
        main_layout.addLayout(self.thumbnail_layout)

        self.metadata_layout = QHBoxLayout()
        self.label_metadata = Label("", "Arial", 10, Qt.AlignLeft)
        self.metadata_layout.addWidget(self.label_metadata)
        main_layout.addLayout(self.metadata_layout)
        self.setLayout(main_layout)

        self.clicked.connect(self.emitName)

    def emitName(self) -> None:
        self.Filename.emit(self.label_file_name.text())
