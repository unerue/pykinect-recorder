from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy

from ..common_widgets import Label


class ImuSensors(QFrame):
    def __init__(self, min_size: tuple[int, int], max_size: tuple[int, int]) -> None:
        super().__init__()
        self.setMinimumSize(QSize(min_size[0], min_size[1]))
        self.setMaximumSize(QSize(max_size[0], max_size[1]))
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("IMUSensor")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.label_title = Label("IMU Sensor", orientation=Qt.AlignCenter)
        self.label_title.setMinimumHeight(30)
        self.label_title.setMaximumHeight(50)

        self.grid_layout = QGridLayout()
        self.speed_layout = QHBoxLayout()
        self.speed_layout.setSpacing(5)
        self.speed_layout.setContentsMargins(0, 0, 0, 0)

        self.label_time = Label("Time(s) : ")
        self.label_time.setMinimumHeight(30)
        self.label_time.setMaximumHeight(50)

        self.label_fps = Label("FPS : ")
        self.label_fps.setMinimumHeight(30)
        self.label_fps.setMaximumHeight(50)

        self.speed_layout.addWidget(self.label_time)
        self.speed_layout.addWidget(self.label_fps)

        self.acc_layout = QVBoxLayout()
        self.acc_layout.setSpacing(5)
        self.acc_layout.setContentsMargins(0, 0, 0, 0)

        self.label_acc_title = Label("Accelerometer")
        self.label_acc_x = Label("X : ")
        self.label_acc_y = Label("Y : ")
        self.label_acc_z = Label("Z : ")

        self.gyro_layout = QVBoxLayout()
        self.gyro_layout.setSpacing(5)
        self.gyro_layout.setContentsMargins(0, 0, 0, 0)

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
        self.main_layout.addWidget(Label())
        self.main_layout.addLayout(self.gyro_layout)

        self.setLayout(self.main_layout)
