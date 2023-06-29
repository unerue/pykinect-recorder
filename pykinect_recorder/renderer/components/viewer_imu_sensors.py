from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout

from ..common_widgets import Label


class ImuSensors(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumWidth(320)
        self.setMaximumHeight(480)
        self.setObjectName("IMUSensor")

        self.main_layout = QVBoxLayout()
        self.label_title = Label("IMU Sensor", orientation=Qt.AlignmentFlag.AlignCenter)
        self.label_title.setFixedHeight(60)

        self.speed_layout = QHBoxLayout()
        self.label_time = Label("Time(s) : --- ")
        self.label_time.setFixedHeight(30)
        self.label_fps = Label("FPS : ")
        self.label_fps.setFixedHeight(30)
        self.speed_layout.addWidget(self.label_time)
        self.speed_layout.addWidget(self.label_fps)

        self.acc_layout = QVBoxLayout()
        self.label_acc_title = Label("Accelerometer")
        self.label_acc_x = Label("X : ")
        self.label_acc_y = Label("Y : ")
        self.label_acc_z = Label("Z : ")

        self.gyro_layout = QVBoxLayout()
        self.label_gyro_title = Label("Gyroscope")
        self.label_gyro_x = Label("X : ")
        self.label_gyro_y = Label("Y : ")
        self.label_gyro_z = Label("Z : ")

        self.acc_layout.addWidget(self.label_acc_title)
        self.acc_layout.addWidget(self.label_acc_x)
        self.acc_layout.addWidget(self.label_acc_y)
        self.acc_layout.addWidget(self.label_acc_z)

        self.gyro_layout.addWidget(self.label_gyro_title)
        self.gyro_layout.addWidget(self.label_gyro_x)
        self.gyro_layout.addWidget(self.label_gyro_y)
        self.gyro_layout.addWidget(self.label_gyro_z)

        self.main_layout.addWidget(self.label_title)
        self.main_layout.addLayout(self.speed_layout)
        self.main_layout.addWidget(self.label_time)
        self.main_layout.addLayout(self.acc_layout)
        self.main_layout.addLayout(self.gyro_layout)

        self.setLayout(self.main_layout)
