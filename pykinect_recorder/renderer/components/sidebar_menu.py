import os
from PySide6.QtCore import Signal, QSize, Qt, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QFrame, QPushButton
)


from ..common_widgets import all_signals

class SidebarMenus(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet("background-color: #2d2d2d;")
        _root_path = "..\\pykinect-recorder\\pykinect_recorder\\renderer\\public\\"

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.recorder_option = self._make_icons(
            _root_path, 
            "files-icon.svg", 
            "Recording Viewer",
            "stylesheet\\sidebarBtn.stylesheet",
        )
        self.explorer_option = self._make_icons(
            _root_path, 
            "search-line-icon.svg", 
            "Explorer & Playback",
            "stylesheet\\sidebarBtn.stylesheet",
        )
        self.deeplearning_option = self._make_icons(
            _root_path, 
            "artificial-intelligence-ai-chip-icon.svg", 
            "Deep Learning Solution",
            "stylesheet\\sidebarBtn.stylesheet",
        )

        main_layout.addWidget(self.recorder_option)
        main_layout.addWidget(self.explorer_option)
        main_layout.addWidget(self.deeplearning_option)
        self.setLayout(main_layout)

        self.recorder_option.clicked.connect(self.clicked_recorder)
        self.explorer_option.clicked.connect(self.clicked_explorer)
        self.deeplearning_option.clicked.connect(self.clicked_solution)

    def _make_icons(
            self, 
            root_path: os.PathLike, 
            file_path: str,
            tooltip: str,
            stylesheet=None
        ) -> QPushButton:

        _btn = QPushButton()
        _btn.setFixedSize(45, 55)
        _btn.setIcon(QIcon(root_path + file_path))
        _btn.setIconSize(QSize(45, 45))
        _btn.setToolTip(f'<b>{tooltip}<b>')

        if stylesheet is not None:
            with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
                stylesheet = f.read()
            _btn.setStyleSheet(str(stylesheet))

        return _btn
    
    def clicked_recorder(self):
        all_signals.stacked_sidebar_status.emit("recorder")

    def clicked_explorer(self):
        all_signals.stacked_sidebar_status.emit("explorer")

    def clicked_solution(self):
        all_signals.stacked_sidebar_status.emit("solution")