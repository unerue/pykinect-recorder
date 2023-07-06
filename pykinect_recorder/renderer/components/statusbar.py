from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizeGrip

class StatusBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(" background-color: #4888d6; ")

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_size_grip = QFrame()
        self.frame_size_grip.setObjectName("frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 10))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)
        self.main_layout.addWidget(self.frame_size_grip)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 30px; height: 30px; margin 0px; padding: 0px;")
        self.setLayout(self.main_layout)