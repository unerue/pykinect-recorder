import os
import platform

from PySide6.QtCore import QSize, Qt, Slot
from PySide6.QtWidgets import QFrame, QHBoxLayout, QSizeGrip

from ..common_widgets import Label
from ..signals import all_signals

class StatusBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(30)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(" background-color: #007acc; border-radius: 0px;")

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.user_name = os.getenv("USERNAME")
        if platform.system().startswith("Windows"):
            self.base_path = os.path.join("C", "Users", self.user_name, "Videos")
        else:
            self.base_path = os.path.join("home", self.user_name, "Videos")

        self.sub_data_layout = QHBoxLayout()
        self.label_save_path = Label(f"Save dir: {self.base_path}", fontsize=12)
        self.sub_data_layout.addWidget(self.label_save_path)
        self.sub_data_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.addLayout(self.sub_data_layout)

        self.frame_size_layout = QHBoxLayout()
        self.frame_size_grip = QFrame()
        self.frame_size_grip.setFixedWidth(30)
        self.frame_size_grip.setObjectName("frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(30, 10))
        self.frame_size_grip.setMaximumSize(QSize(30, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)
        self.frame_size_layout.addWidget(self.frame_size_grip)
        self.frame_size_layout.setAlignment(Qt.AlignRight)

        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 30px; height: 30px; margin 0px; padding: 0px;")
        self.main_layout.addLayout(self.frame_size_layout)
        self.setLayout(self.main_layout)

        all_signals.option_signals.save_filepath.connect(self.set_save_path)

    @Slot(str)
    def set_save_path(self, value):
        self.label_save_path.setText("save path: " + value)