import os
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QFrame, QPushButton
)

import qtawesome as qta
from ..signals import all_signals

class SidebarMenus(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet("background-color: #333333;")
        _root_path = os.path.abspath("./renderer/public/")

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.recorder_option = self._make_icons(
            qta.icon("mdi.file-multiple-outline"),
            "Recording Viewer",
        )
        self.explorer_option = self._make_icons(
            qta.icon("mdi6.file-find-outline"),
            "Explorer & Playback",
        )
        self.deeplearning_option = self._make_icons( 
            qta.icon("ph.gear"), 
            "Deep Learning Solution",
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
            icon: qta,
            tooltip: str,
        ) -> QPushButton:

        _btn = QPushButton(icon, "")
        _btn.setFixedSize(45, 55)
        _btn.setIconSize(QSize(45, 45))
        _btn.setToolTip(f'<b>{tooltip}<b>')
        _btn.setStyleSheet("""
            QPushButton:hover {
                border-color: white;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)

        # print(root_path)
        # print(os.path.join(root_path, file_path))
        # tmp = QPixmap(os.path.join(root_path, file_path))
        # tmp = QPixmap(os.path.join(os.path.split(__file__)[0], file_path))
        # _icon = QIcon(tmp)
        # _btn.setIcon(QIcon(os.path.join(root_path, file_path)))
        # _btn.setIcon(file_path)

        # print(os.path.abspath("./renderer/components/sidebarBtn.stylesheet"))
        # print(os.path.split(__file__))
        # if stylesheet is not None:
        #     with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
        #     # with open(os.path.abspath("./pykinect_recorder/renderer/components/sidebbarBtn.stylesheet"), "r", encoding="utf-8") as f:
        #         stylesheet = f.read()
        #     _btn.setStyleSheet(str(stylesheet))

        return _btn
    
    def clicked_recorder(self):
        all_signals.stacked_sidebar_status.emit("recorder")

    def clicked_explorer(self):
        all_signals.stacked_sidebar_status.emit("explorer")

    def clicked_solution(self):
        all_signals.stacked_sidebar_status.emit("solution")
