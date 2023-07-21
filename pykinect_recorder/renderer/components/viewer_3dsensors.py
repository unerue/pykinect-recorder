from PySide6.QtCore import QSize
from PySide6.QtWidgets import QFrame, QHBoxLayout, QRadioButton, QLabel
from ..common_widgets import Frame


class Viewer3DSensors(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(1190, 1030))
        self.setStyleSheet("background-color: black;")

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel("Sibal")

        # self.frame_sensor = QFrame()
        # self.frame_sensor.setFixedHeight()
        self.main_layout.addWidget(self.label)
        



        # self.btn_frame = QFrame()
        # self.btn_rgb = QRadioButton("RGB")
        # self.btn_depth = QRadioButton("Depth")

        self.setLayout(self.main_layout)



