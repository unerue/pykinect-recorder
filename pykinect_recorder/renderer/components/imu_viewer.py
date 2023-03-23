from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout

from .custom_widgets import Label


class IMUSensor(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(270)
        self.setObjectName("IMUSensor")
        self.setStyleSheet(
            " QFrame#IMUSensor { border-color: white; }"
        )

        self.layout_main = QVBoxLayout()
        self.title = Label("IMU Sensor", orientation=Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet(
            "border-color: white;"
        )
        self.title.setFixedHeight(60)

        self.layout_speed = QHBoxLayout()
        self.label_time = Label("Time(s) : --- ")
        self.label_time.setFixedHeight(30)
        self.label_fps = Label("FPS : ")
        self.label_fps.setFixedHeight(30)
        self.layout_speed.addWidget(self.label_time)
        self.layout_speed.addWidget(self.label_fps)

        self.layout_acc = QVBoxLayout()
        self.acc_title = Label("Accelerometer")
        self.acc_x = Label("X : ")
        self.acc_y = Label("Y : ")
        self.acc_z = Label("Z : ")

        self.layout_gyro = QVBoxLayout() 
        self.gyro_title = Label("Gyroscope")
        self.gyro_x = Label("X : ")
        self.gyro_y = Label("Y : ")
        self.gyro_z = Label("Z : ")

        self.layout_acc.addWidget(self.acc_title)
        self.layout_acc.addWidget(self.acc_x)
        self.layout_acc.addWidget(self.acc_y)
        self.layout_acc.addWidget(self.acc_z)

        self.layout_gyro.addWidget(self.gyro_title)
        self.layout_gyro.addWidget(self.gyro_x)
        self.layout_gyro.addWidget(self.gyro_y)
        self.layout_gyro.addWidget(self.gyro_z)

        self.layout_main.addWidget(self.title)
        self.layout_main.addLayout(self.layout_speed)
        self.layout_main.addWidget(self.label_time)
        self.layout_main.addLayout(self.layout_acc)
        self.layout_main.addLayout(self.layout_gyro)

        self.setLayout(self.layout_main)


