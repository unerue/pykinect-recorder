import os
import sys
import cv2
<<<<<<< HEAD
import time
import queue
import datetime
import logging
from typing import Optional, Tuple
=======
import queue
import datetime
import logging
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43

import sounddevice as sd
import soundfile as sf
import numpy as np
assert np  # avoid "imported but unused" message (W0611)
<<<<<<< HEAD
=======
from typing import Optional, Tuple
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43

from pydub import AudioSegment
from pyk4a import Config, ImageFormat, PyK4A, PyK4ARecord
import pyk4a

from PySide6.QtCore import Qt, QThread, Signal, Slot
<<<<<<< HEAD
from PySide6.QtGui import QImage, QPixmap, QFont
=======
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap, QFont
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43
from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget, QDialog, 
)

<<<<<<< HEAD

CONFIG = Config(
    color_format=ImageFormat.COLOR_BGRA32, 
    depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
    color_resolution=pyk4a.ColorResolution.RES_720P,
    synchronized_images_only=True
)

# make output dir
# if not os.path.exists('./tools/outputs/'):
#     os.mkdir('./tools/outputs')
=======
# make output dir
if not os.path.exists('./tools/pyk4a/example/outputs/'):
    os.mkdir('./tools/pyk4a/example/outputs')

>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43

class RecordRGBD:
    pass


<<<<<<< HEAD
class Thread(QThread):
    RGBUpdateFrame = Signal(QImage)
    DepthUpdateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.set_filename()

    def set_filename(self) -> None:
        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")
        # base_path = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\tools\\outputs'
        base_path = "C:\\Users\\qhdrm\\Videos"
        
        self.filename_video = f'{base_path}\\{filename}.mkv'
        self.filename_audio = f'{base_path}\\{filename}.wav'
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
        record = PyK4ARecord(
            device=azure_device, 
            config=config, 
            path=self.filename_video
        )
        record.create()
        print(self.status)
        while self.status:
            cur_frame = azure_device.get_capture()
            record.write_capture(cur_frame)

            if np.any(cur_frame.color):
                color_frame = cur_frame.color[:, :, :3].copy()
                color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

                h, w, ch = color_frame.shape
                img = QImage(color_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
                self.RGBUpdateFrame.emit(scaled_img)

            if np.any(cur_frame.depth):
                depth_frame = self.colorize(cur_frame.depth, (None, 5000), cv2.COLORMAP_HSV)
                h, w, ch = depth_frame.shape

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(640, 480, Qt.KeepAspectRatio)
                self.DepthUpdateFrame.emit(scaled_depth_frame)


=======
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43
class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler("tools/pyk4a/example/outputs/log.txt")
        formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] (%(filename)s:%(lineno)d) > %(message)s')
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)

<<<<<<< HEAD
        self.config = CONFIG
=======
        self.config = Config(
            color_format=ImageFormat.COLOR_BGRA32, 
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            color_resolution=pyk4a.ColorResolution.RES_720P,
            camera_fps= pyk4a.FPS.FPS_30,
            synchronized_images_only=True
        )
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43
        self.azure_device = PyK4A(config=self.config, device_id=0)
        self.record_flag = True

        # check record env
        if not self.initial_check():
            modal = QDialog()
            modal_layout = QVBoxLayout()

            e_message = QLabel("카메라에 문제가 있습니다. 재연결을 시도해주세요.")
            e_message.setAlignment(Qt.AlignCenter)
            e_message.setFont(QFont('Arial', 15))
            
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
        self.time_label.setFont(QFont('Arial', 15))
        
        self.rgb_label = QLabel(self)
        self.rgb_label.setFixedSize(640, 480)
        self.depth_label = QLabel(self)
        self.depth_label.setFixedSize(640, 480)
        images_layout.addWidget(self.rgb_label)
        images_layout.addWidget(self.depth_label)

<<<<<<< HEAD
        # Thread in charge of updating the image
        self.th = Thread(self)
        # self.th.finished.connect(self.close)
        self.th.RGBUpdateFrame.connect(self.setRGBImage)
        self.th.DepthUpdateFrame.connect(self.setDepthImage)

=======
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43
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

<<<<<<< HEAD
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
=======
    def set_filename(self) -> None:
        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")
        base_path = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\tools\\outputs'
        
        self.filename_video = f'{base_path}\\{filename}.mkv'
        self.filename_audio = f'{base_path}\\{filename}.wav'
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

    def start(self):
        print("녹화를 시작합니다.")
        self.logger.debug("녹화를 시작합니다.")
        self.set_filename()
        self.azure_device.start()
        record = PyK4ARecord(  
            device=self.azure_device, 
            config=self.config, 
            path=self.filename_video
        )
        record.create()
        self.button1.setEnabled(False)
        self.button2.setEnabled(True)

        while self.record_flag:
            frame = self.azure_device.get_capture()
            record.write_capture(frame)
            
            if np.any(frame.color):
                color_frame = frame.color[:, :, :3].copy()
                color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.color[:, :, :3].shape

                color_img = QImage(color_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = color_img.scaled(640, 480, Qt.KeepAspectRatio)
                self.setColorImage(scaled_img)

            if np.any(frame.depth):
                depth_img = self.colorize(frame.depth, (None, 5000), cv2.COLORMAP_HSV)
                h, w, ch = depth_img.shape

                depth_img = QImage(depth_img, w, h,  QImage.Format_RGB888)
                scaled_depth_img = depth_img.scaled(640, 480, Qt.KeepAspectRatio)
                self.setDepthImage(scaled_depth_img)

            self.time_label.setText("{%.2f}초" %(record.captures_count/30))

        record.flush()
        record.close()
        self.logger.debug(f"{record.captures_count/1800}분 동안 촬영되었습니다.")
        self.azure_device.close()

    def stop(self):
        print("녹화를 종료합니다.")
        self.button1.setEnabled(True)
        self.button2.setEnabled(False)
        self.record_flag = False
        
    def setColorImage(self, image):
        self.rgb_label.setPixmap(QPixmap.fromImage(image))

    def setDepthImage(self, image):
        self.depth_label.setPixmap(QPixmap.fromImage(image))    
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43


if __name__ == '__main__':
    app = QApplication()
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

    # main(args)
<<<<<<< HEAD
=======

    

    

    

    
>>>>>>> 17e2c2abf735c8502eafd0093806426722ea9b43