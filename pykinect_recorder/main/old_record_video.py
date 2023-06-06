import datetime
import logging
import os
import queue
import sys
import time
from typing import Optional, Tuple

import cv2
import numpy as np

import sounddevice as sd
import soundfile as sf

assert np  # avoid "imported but unused" message (W0611)

import pyk4a
from pydub import AudioSegment
from pyk4a import Config, ImageFormat, PyK4A, PyK4ARecord

from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


CONFIG = Config(
    color_format=ImageFormat.COLOR_BGRA32,
    depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
    color_resolution=pyk4a.ColorResolution.RES_720P,
    synchronized_images_only=True,
)

# make output dir
# if not os.path.exists('./tools/outputs/'):
#     os.mkdir('./tools/outputs')


class RecordRGBD:
    pass


class Thread(QThread):
    rgb_updated_frame = Signal(QImage)
    depth_updated_frame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.set_filename()

    def set_filename(self) -> None:
        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")
        # base_path = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\tools\\outputs'
        base_path = "C:\\Users\\qhdrm\\Videos"

        self.filename_video = f"{base_path}\\{filename}.mkv"
        self.filename_audio = f"{base_path}\\{filename}.wav"
        print(filename)

    def colorize(
        self,
        image: np.ndarray,
        clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
        colormap: int = cv2.COLORMAP_HSV,
    ) -> np.ndarray:
        if clipping_range[0] or clipping_range[1]:
            img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
        else:
            img = image.copy()
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img = cv2.applyColorMap(img, colormap)
        return img

    def run(self):
        config = CONFIG
        azure_device = PyK4A(config=config, device_id=0)
        azure_device.start()
        record = PyK4ARecord(device=azure_device, config=config, path=self.filename_video)
        record.create()
        print(self.status)
        while self.status:
            current_frame = azure_device.get_capture()
            record.write_capture(current_frame)

            if np.any(current_frame.color):
                color_frame = current_frame.color[:, :, :3].copy()
                color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

                h, w, ch = color_frame.shape
                img = QImage(color_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
                self.rgb_updated_frame.emit(scaled_img)

            if np.any(current_frame.depth):
                depth_frame = self.colorize(current_frame.depth, (None, 5000), cv2.COLORMAP_HSV)
                h, w, ch = depth_frame.shape

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(640, 480, Qt.KeepAspectRatio)
                self.depth_updated_frame.emit(scaled_depth_frame)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler("tools/pyk4a/example/outputs/log.txt")
        formatter = logging.Formatter("[%(levelname)s] [%(asctime)s] (%(filename)s:%(lineno)d) > %(message)s")
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)

        self.config = CONFIG
        self.azure_device = PyK4A(config=self.config, device_id=0)
        self.record_flag = True

        # check record env
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

        # initailize main window ui
        self.initial_window()

    def initial_check(self) -> bool:
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
        # Title and dimensions
        self.setWindowTitle("영유아 녹화 프로그램")
        self.setGeometry(0, 0, 1400, 600)

        # image layout
        images_layout = QHBoxLayout()
        self.time_label = QLabel(self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont("Arial", 15))

        self.rgb_label = QLabel(self)
        self.rgb_label.setFixedSize(640, 480)
        self.depth_label = QLabel(self)
        self.depth_label.setFixedSize(640, 480)
        images_layout.addWidget(self.rgb_label)
        images_layout.addWidget(self.depth_label)

        # Thread in charge of updating the image
        self.th = Thread(self)
        # self.th.finished.connect(self.close)
        self.th.rgb_updated_frame.connect(self.setRGBImage)
        self.th.depth_updated_frame.connect(self.setDepthImage)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("녹화 시작")
        self.button2 = QPushButton("녹화 종료")
        self.button1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button1)
        buttons_layout.addWidget(self.button2)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addLayout(images_layout)
        layout.addLayout(buttons_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
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


if __name__ == "__main__":
    app = QApplication()
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

    # main(args)
