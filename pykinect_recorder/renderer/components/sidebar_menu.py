import os
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QVBoxLayout, QFrame, QPushButton

import qtawesome as qta
from ..signals import all_signals


class SidebarMenus(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(55)
        self.setStyleSheet("background-color: #333333;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignLeft)
        menu_layout = QVBoxLayout()
        menu_layout.setSpacing(0)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        btn_recorder_menu = self.make_icons(qta.icon("fa.video-camera"),"Recording Viewer")
        btn_explorer_menu = self.make_icons(qta.icon("ph.monitor-play-fill"),"Explorer & Playback")
        btn_deeplearning_menu = self.make_icons(qta.icon("fa.crosshairs"),"Deep Learning Solution")

        menu_layout.addWidget(btn_recorder_menu)
        menu_layout.addWidget(btn_explorer_menu)
        menu_layout.addWidget(btn_deeplearning_menu)
        main_layout.addLayout(menu_layout)

        option_layout = QVBoxLayout()         
        btn_option = self.make_icons(qta.icon("fa.gear"),"Pykinect Recorder Option")
        option_layout.addWidget(btn_option)
        main_layout.addLayout(option_layout)

        self.setLayout(main_layout)

        btn_recorder_menu.clicked.connect(self.clicked_recorder)
        btn_explorer_menu.clicked.connect(self.clicked_explorer)
        btn_deeplearning_menu.clicked.connect(self.clicked_solution)
        btn_option.clicked.connect(self.clicked_option)

    def make_icons(
        self,
        icon: qta,
        tooltip: str,
        scale: float = 0.8
    ) -> QPushButton:
        w, h = int(45 * scale), int(45 * scale)
        _btn = QPushButton(icon, "")
        _btn.setFixedSize(55, 55)
        _btn.setIconSize(QSize(w, h))
        _btn.setToolTip(f"<b>{tooltip}<b>")
        _btn.setStyleSheet(
            """
            QPushButton {
                border: 0px solid #ffffff;
            }
            QPushButton:hover {
                background-color: #252526;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """
        )

        return _btn

    def clicked_recorder(self):
        all_signals.stacked_sidebar_status.emit("recorder")

    def clicked_explorer(self):
        all_signals.stacked_sidebar_status.emit("explorer")

    def clicked_solution(self):
        all_signals.stacked_sidebar_status.emit("solution")

    def clicked_option(self):
        pass