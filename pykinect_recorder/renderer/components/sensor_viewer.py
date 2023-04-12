import os
import sys
import time
import datetime
import numpy as np
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QPointF
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QVBoxLayout, 
    QFrame, QDialog, QGridLayout
)

from .custom_widgets import Label, Frame
from .viewer_sidebar import _config_sidebar
from .pyk4a_thread import Pyk4aThread
from .playback import PlayBackThread
from .imu_viewer import IMUSensor
from .audio_viewer import AudioSensor
from pykinect_recorder.main.logger import logger
from pykinect_recorder.main._pyk4a.k4a._k4a import k4a_device_set_color_control
from pykinect_recorder.main._pyk4a.k4a.configuration import Configuration
from pykinect_recorder.main._pyk4a.pykinect import start_device, initialize_libraries, start_playback


SAMPLE_COUNT = 10000
RESOLUTION = 4


class SensorViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(1200, 1000)
        self.setStyleSheet("background-color: black;") 
        self.device = None
        self.config = None
        self.color_control = None

        self.layout_grid = QGridLayout()
        self.frame_rgb = Frame("RGB Sensor")
        self.frame_depth = Frame("Depth Sensor")
        self.frame_ir = Frame("IR Sensor")
        
        self.layout_subdata = QHBoxLayout() # TODO => 네이밍 다시 하기
        self.imu_senser = IMUSensor()
        self.audio_sensor = AudioSensor()
        self.layout_subdata.addWidget(self.imu_senser)
        self.layout_subdata.addWidget(self.audio_sensor)
        self.frame_subdata = Frame("subdata", layout=self.layout_subdata)

        layout_btn = QHBoxLayout()
        self.btn_open = QPushButton("Device open")
        self.btn_viewer = QPushButton("▶")
        self.btn_record = QPushButton("●")

        self.btn_viewer.setStyleSheet("""
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            QPushButton {
                background-color: red;
            }
            """
        )
        self.btn_record.setStyleSheet("""
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            """
        )

        self.btn_viewer.setToolTip("<b>Streaming Button</b>")
        self.btn_record.setToolTip("<b>Recording Button</b>")
        
        layout_btn.addWidget(self.btn_open)
        layout_btn.addWidget(self.btn_viewer)
        layout_btn.addWidget(self.btn_record)
        
        self.buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.th = Pyk4aThread(device=self.device)
        self.th.RGBUpdateFrame.connect(self.setRGBImage)
        self.th.DepthUpdateFrame.connect(self.setDepthImage)
        self.th.IRUpdateFrame.connect(self.setIRImage)
        self.th.Time.connect(self.setTime)
        self.th.AccData.connect(self.setAccData)
        self.th.GyroData.connect(self.setGyroData)
        self.th.Fps.connect(self.setFps)
        self.th.Audio.connect(self.setAudioData)
            
        self.is_device = True
        self.is_viewer = True
        self.is_record = True
        self.btn_open.clicked.connect(self.open_device)
        self.btn_viewer.clicked.connect(self.streaming)
        self.btn_record.clicked.connect(self.recording)
        
        self.target = None
        self.layout_grid.addWidget(self.frame_rgb, 0, 0)
        self.layout_grid.addWidget(self.frame_depth, 0, 1)
        self.layout_grid.addWidget(self.frame_ir, 1, 0)
        self.layout_grid.addWidget(self.frame_subdata, 1, 1)
        self.layout_grid.addLayout(layout_btn, 2, 0, 1, 2)

        self.setAcceptDrops(True)
        self.setLayout(self.layout_grid)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(watched, event)
    
    def get_index(self, pos):
        for i in range(self.layout_grid.count()):
            if self.layout_grid.itemAt(i).geometry().contains(pos) and i != self.target:
                return i

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.target = self.get_index(event.windowPos().toPoint())
        else:
            self.target = None

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.target is not None:
            drag = QDrag(self.layout_grid.itemAt(self.target).widget())
            pix = self.layout_grid.itemAt(self.target).widget().grab()
            mimedata = QMimeData()
            mimedata.setImageData(pix)
            drag.setMimeData(mimedata)
            drag.setPixmap(pix)
            drag.exec(Qt.DropAction.CopyAction | Qt.DropAction.MoveAction)

    def mouseReleaseEvent(self, event):
        self.target = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        if not event.source().geometry().contains(event.pos()):
            source = self.get_index(event.pos())
            if source is None:
                return

            i, j = max(self.target, source), min(self.target, source)
            p1, p2 = self.layout_grid.getItemPosition(i), self.layout_grid.getItemPosition(j)

            self.layout_grid.addItem(self.layout_grid.takeAt(i), *p2)
            self.layout_grid.addItem(self.layout_grid.takeAt(j), *p1)

            event.accept()
        
    def check_device(self) -> bool:
        try:
            self.config = Configuration()

            for k, v in _config_sidebar.items():
                setattr(self.config, k, v)

            initialize_libraries()
            _device = start_device(config=self.config)
            logger.debug(
                "카메라 연결에 문제에 이상이 없습니다."
            )
            _device.close()
        except:
            modal = QDialog()
            layout_modal = QVBoxLayout()
            e_message = Label(
                "<b>카메라 연결에 문제가 있습니다. <br> 연결을 재시도해주세요.</b>", 
                "Arial", 20, Qt.AlignmentFlag.AlignCenter
            )
            logger.error(
                "카메라 연결에 문제가 있습니다. 연결을 재시도해주세요"
            )

            layout_modal.addWidget(e_message)
            modal.setLayout(layout_modal)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()
            sys.exit(0)

    def open_device(self) -> None:
        if self.is_device is True:
            self.check_device()
            self.is_device = False
            self.btn_open.setText("Device close")
        else:
            self.frame_rgb.frame.setText("RGB Frame")
            self.frame_depth.frame.setText("Depth Frame")
            self.frame_ir.frame.setText("IR Frame")
            self.is_device = True
            self.btn_open.setText("Device open")
            self.device = None
    
    # TODO Streaming 이랑 Recording 겹치는 코드가 많음.
    def streaming(self) -> None:
        if self.is_viewer:
            self.set_filename()
            self.device = start_device(config=self.config, record=False)
            self.th.device = self.device
            self.th.audio_file = self.filename_audio

            self.btn_record.setEnabled(False)
            self.th.is_run = True
            self.btn_viewer.setText("■")
            self.is_viewer = False
            self.th.start()
        else:
            self.btn_record.setEnabled(True)
            self.th.is_run = False
            self.btn_viewer.setText("▶")
            self.is_viewer = True
            self.device.close()
            self.th.quit()
            time.sleep(1)   
        
    def recording(self) -> None:
        if self.is_record:
            self.set_filename()
            self.device = start_device(
                config=self.config, 
                record=True, 
                record_filepath=self.filename_video
            )
            self.th.device = self.device
            self.th.audio_record = True
            self.th.audio_file = self.filename_audio

            self.btn_viewer.setEnabled(False)
            self.th.is_run = True
            self.btn_record.setText("■")
            self.is_record = False
            self.th.start()
        else:
            self.btn_viewer.setEnabled(True)
            self.th.is_run = False
            self.btn_record.setText("▶")
            self.is_record = True
            self.device.close()
            self.th.quit()
            time.sleep(1)

    @Slot(str)
    def playback(self, filepath) -> None:
        # playback
        print(filepath)
        initialize_libraries()
        playback = start_playback(filepath)
        playback_config = playback.get_record_configuration()

        # Connect
        self.th = PlayBackThread(playback=playback)
        self.th.RGBUpdateFrame.connect(self.setRGBImage)
        self.th.DepthUpdateFrame.connect(self.setDepthImage)
        self.th.IRUpdateFrame.connect(self.setIRImage)
        self.th.Time.connect(self.setTime)
        self.th.Fps.connect(self.setFps)

        # set option
        self.th.is_run = True
        self.btn_record.setEnabled(False)
        self.btn_viewer.setEnabled(False)
        self.btn_open.setEnabled(False)
        self.th.start()

    def set_filename(self) -> None:
        base_path = os.path.join(Path.home(), "Videos")

        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")

        self.filename_video = os.path.join(base_path, f"{filename}.mkv")
        self.filename_audio = os.path.join(base_path, f"{filename}.mp3")
        if sys.flags.debug:
            print(base_path, self.filename_video)
        
    @Slot(QImage)
    def setRGBImage(self, image: QImage) -> None:
        self.frame_rgb.frame.setPixmap(QPixmap.fromImage(image))
    
    @Slot(QImage)
    def setDepthImage(self, image: QImage) -> None:
        self.frame_depth.frame.setPixmap(QPixmap.fromImage(image))
        
    @Slot(QImage)
    def setIRImage(self, image: QImage) -> None:
        self.frame_ir.frame.setPixmap(QPixmap.fromImage(image))

    @Slot(float)
    def setTime(self, time) -> None:
        self.imu_senser.label_time.setText("Time(s) : %.3f" %time)

    @Slot(float)
    def setFps(self, value) -> None:
        self.imu_senser.label_fps.setText("FPS : %.2f" %value)

    @Slot(list)
    def setAccData(self, values) -> None:
        self.imu_senser.acc_x.setText("X : %.5f" %values[0])
        self.imu_senser.acc_y.setText("Y : %.5f" %values[1])
        self.imu_senser.acc_z.setText("Z : %.5f" %values[2])

    @Slot(float)
    def setGyroData(self, values) -> None:
        self.imu_senser.gyro_x.setText("X : %.5f" %values[0])
        self.imu_senser.gyro_y.setText("Y : %.5f" %values[1])
        self.imu_senser.gyro_z.setText("Z : %.5f" %values[2])

    @Slot(list)
    def setAudioData(self, values) -> None:
        start = 0
        if (values[1] < SAMPLE_COUNT):
            start = SAMPLE_COUNT - values[1]
            for s in range(start):
                self.buffer[s].setY(self.buffer[s + values[1]].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(values[0][data_index]) - 128) / 128
            self.buffer[s].setY(value)
            data_index = data_index + RESOLUTION
        
        self.audio_sensor.series.replace(self.buffer)

        
    def initial_check(self) -> bool:
        # TODO: pykinect_recorder 폴더에서 유틸로 처리
        # self.logger
        initial_flag = True
        logger.debug("---------------녹화 시작 전 테스트를 진행합니다.---------------")
        logger.debug(
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
