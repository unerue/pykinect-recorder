# TODO 왕택
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from .custom_widgets import Label


class AudioSensor(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(270)
        self.setStyleSheet(
            "border-color: white;"
        )
        
        self.layout_main = QVBoxLayout()
        self.title = Label("Audio Sensor", orientation=Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(60)
        self.title.setStyleSheet(
            "border-color: white;"
        )

        self._widget = QWidget()

        self.layout_main.addWidget(self.title)
        self.layout_main.addWidget(self._widget)
        self.setLayout(self.layout_main)
