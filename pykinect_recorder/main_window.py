import logging
import sys
import time

import numpy as np

from pyk4a import PyK4A
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .record_video import RecordVideo


class MainWindow(QMainWindow):
    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # fileHandler = logging.FileHandler("tools/pyk4a/example/outputs/log.txt")
        # formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] (%(filename)s:%(lineno)d) > %(message)s')
        # fileHandler.setFormatter(formatter)
        # self.logger.addHandler(fileHandler)
        self.azure_device = PyK4A(config=self.config, device_id=0)
        self.record_flag = True

        # TODO: initial_check 함수 안에 집어넣기
        if not self.initial_check():
            modal = QDialog()
            modal_layout = QVBoxLayout()

            e_message = QLabel("카메라에 문제가 있습니다. 재연결을 시도해주세요.")
            e_message.setAlignment(Qt.AlignCenter)
            e_message.setFont(QFont("Arial", 15))

            modal_layout.addWidget(e_message)
            modal.setLayout(modal_layout)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()
            sys.exit(0)

        self.initial_window()

    def initial_check(self) -> bool:
        # TODO: pykinect_recorder 폴더에서 유틸로 처리
        # self.logger
        initial_flag = True
        self.logger.debug("---------------녹화 시작 전 테스트를 진행합니다.---------------")
        self.logger.debug(
            f"\n \
            FPS : {str(self.azure_device._config.camera_fps)}\n \
            color_format: {str(self.azure_device._config.color_format)}\n \
            color_resolution: {str(self.azure_device._config.color_resolution)}\n \
            depth_mode: {str(self.azure_device._config.depth_mode)}"
        )
        self.logger.debug("\n---------------영상 테스트를 시작합니다.---------------")

        try:
            self.azure_device.start()
            num_frames = 0

            while num_frames < 10:
                frame = self.azure_device.get_capture()
                if frame.color.shape[2] != 4:
                    self.logger.debug("RGBD 영상의 차원이 올바르지 않습니다.")
                    initial_flag = False
                if not np.any(frame.depth):
                    self.logger.debug("Depth 영상을 찾을 수 없습니다.")
                    initial_flag = False

                num_frames += 1
            self.azure_device.close()

        except Exception as e:
            self.logger.debug(e)

        finally:
            self.logger.debug("카메라 연결 테스트를 종료합니다.")
            return initial_flag

    def initial_window(self) -> None:
        self.setWindowTitle("영유아 녹화 프로그램")
        width = 180 + 1280
        self.setFixedSize(width, 720)

        self.time_label = QLabel(
            "You and me 내 맘이 보이지? 한참을 쳐다봐, 가까이 다가가 you see (ey-yeah) You see, ey, ey, ey, ey",
            self,
        )
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont("Arial", 15))
        self.time_label.setFixedHeight(50)

        self.rgb_label = QLabel("RGB 영상", self)
        self.rgb_label.setStyleSheet("background-color: black;")
        self.rgb_label.setFixedSize(640, 480)

        self.depth_label = QLabel("깊이 영상", self)
        self.depth_label.setStyleSheet("background-color: black;")
        self.depth_label.setFixedSize(400, 360)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.rgb_label)
        images_layout.addWidget(self.depth_label)

        self.th = RecordVideo(self.config, self)
        # self.th.finished.connect(self.close)
        self.th.RGBUpdateFrame.connect(self.setRGBImage)
        self.th.DepthUpdateFrame.connect(self.setDepthImage)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("녹화 시작")
        self.button2 = QPushButton("녹화 종료")
        self.button1.setFixedSize(120, 80)
        self.button2.setFixedSize(120, 80)
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button2)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Main layout
        main_layout = QHBoxLayout()
        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.time_label)
        preview_layout.addLayout(images_layout)
        preview_layout.addLayout(buttons_layout)
        main_layout.addLayout(preview_layout)

        file_list = QVBoxLayout()
        widget_name = QLabel("녹화된 영상 목록")
        widget_name.setFixedHeight(30)
        file_list.addWidget(widget_name)
        file_widget = QWidget()
        file_widget.setFixedWidth(360)
        file_widget.setStyleSheet("background-color: black;")
        file_list.addWidget(file_widget)

        button3 = QPushButton("파일 업로드")
        button3.setFixedSize(360, 50)
        file_list.addWidget(button3)

        main_layout.addLayout(file_list)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Connections
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.stop)
        self.button1.setEnabled(True)
        self.button2.setEnabled(False)

    @Slot()
    def stop(self) -> None:
        print("Finishing...")
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        # cv2.destroyAllWindows()
        self.th.status = False
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self) -> None:
        print("Starting...")
        self.button2.setEnabled(True)
        self.button1.setEnabled(False)
        self.th.set_filename()
        self.th.status = True
        self.th.start()

    @Slot(QImage)
    def setRGBImage(self, image: QImage) -> None:
        self.rgb_label.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def setDepthImage(self, image: QImage):
        self.depth_label.setPixmap(QPixmap.fromImage(image))
