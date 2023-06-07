import os
import sys
import time
import ctypes
import datetime
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QPointF
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QFrame, QDialog, QGridLayout

from ..common_widgets import Label, Frame
from .record_sensors import RecordSensors
from .playback_sensors import PlaybackSensors
from .viewer_imu_sensors import ImuSensors
from .viewer_audio import AudioSensor
from pykinect_recorder.main._pyk4a.k4a._k4a import k4a_device_set_color_control
from pykinect_recorder.main._pyk4a.k4a._k4atypes import color_command_dict, K4A_COLOR_CONTROL_MODE_MANUAL
from pykinect_recorder.main._pyk4a.k4a.configuration import Configuration
from pykinect_recorder.main._pyk4a.pykinect import start_device, initialize_libraries, start_playback
from .sidebar_record_control import _config_sidebar
from ..signals import all_signals


SAMPLE_COUNT = 10000
RESOLUTION = 4


class SensorViewer(QFrame):
    def __init__(self, size: tuple[int, int] = (1200, 1000)) -> None:
        super().__init__()

        self.setStyleSheet("background-color: #1e1e1e;")
        self.device = None
        self.config = None
        self.color_control = None
        self.base_path = None
        self.emit_configs = _config_sidebar

        self.grid_layout = QGridLayout()
        self.frame_rgb = Frame("RGB Sensor")
        self.frame_depth = Frame("Depth Sensor")
        self.frame_ir = Frame("IR Sensor")

        self.layout_subdata = QHBoxLayout()  # TODO => 네이밍 다시 하기
        self.imu_senser = ImuSensors()
        self.audio_sensor = AudioSensor()
        self.layout_subdata.addWidget(self.imu_senser)
        self.layout_subdata.addWidget(self.audio_sensor)
        self.frame_subdata = Frame("subdata", layout=self.layout_subdata)

        layout_btn = QHBoxLayout()
        layout_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_open = QPushButton("Device open")
        self.btn_open.setFixedSize(200, 40)
        self.btn_viewer = QPushButton("▶")
        self.btn_viewer.setFixedSize(200, 40)
        self.btn_record = QPushButton("●")
        self.btn_record.setFixedSize(200, 40)

        self.btn_open.setStyleSheet(
            """
            QPushButton:hover {
                border-color: "white";
            }
        """
        )
        self.btn_viewer.setStyleSheet(
            """
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            QPushButton:hover {
                border-color: "white";
            }
            """
        )
        self.btn_record.setStyleSheet(
            """
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            QPushButton {
                background-color: red;
            }
            QPushButton:hover {
                border-color: "white";
            }
            """
        )

        self.btn_viewer.setToolTip("<b>Streaming Button</b>")
        self.btn_record.setToolTip("<b>Recording Button</b>")

        layout_btn.addStretch()
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_open)
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_viewer)
        layout_btn.addStretch()
        layout_btn.addWidget(self.btn_record)
        layout_btn.addStretch()
        layout_btn.addStretch()

        self.buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.th = RecordSensors(device=self.device)
        all_signals.captured_rgb.connect(self.setRGBImage)
        all_signals.captured_depth.connect(self.setDepthImage)
        all_signals.captured_ir.connect(self.setIRImage)
        all_signals.captured_time.connect(self.setTime)
        all_signals.captured_acc_data.connect(self.setAccData)
        all_signals.captured_gyro_data.connect(self.setGyroData)
        all_signals.captured_fps.connect(self.setFps)
        all_signals.captured_audio.connect(self.setAudioData)

        self.is_device = True
        self.is_viewer = True
        self.is_record = True
        self.btn_open.clicked.connect(self.open_device)
        self.btn_viewer.clicked.connect(self.streaming)
        self.btn_record.clicked.connect(self.recording)
        self.btn_viewer.setEnabled(False)

        self.target = None
        self.grid_layout.addLayout(layout_btn, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.frame_rgb, 1, 0)
        self.grid_layout.addWidget(self.frame_depth, 1, 1)
        self.grid_layout.addWidget(self.frame_ir, 2, 0)
        self.grid_layout.addWidget(self.frame_subdata, 2, 1)

        self.setAcceptDrops(True)
        self.setLayout(self.grid_layout)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(watched, event)

    def get_index(self, pos):
        for i in range(self.grid_layout.count()):
            if self.grid_layout.itemAt(i).geometry().contains(pos) and i != self.target:
                return i

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.target = self.get_index(event.windowPos().toPoint())
        else:
            self.target = None

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.target is not None:
            drag = QDrag(self.grid_layout.itemAt(self.target).widget())
            pix = self.grid_layout.itemAt(self.target).widget().grab()
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
            p1, p2 = self.grid_layout.getItemPosition(i), self.grid_layout.getItemPosition(j)

            self.grid_layout.addItem(self.grid_layout.takeAt(i), *p2)
            self.grid_layout.addItem(self.grid_layout.takeAt(j), *p1)

            event.accept()

    def check_device(self) -> bool:
        try:
            self.config = Configuration()
            initialize_libraries()
            _device = start_device(config=self.config)
            _device.close()
        except:
            modal = QDialog()
            layout_modal = QVBoxLayout()
            e_message = Label("<b>카메라 연결에 문제가 있습니다. <br> 연결을 재시도해주세요.</b>", "Arial", 20, Qt.AlignmentFlag.AlignCenter)
            layout_modal.addWidget(e_message)
            modal.setLayout(layout_modal)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()
            return False

    def open_device(self) -> None:
        if self.is_device is True:
            if self.check_device() is False:
                return
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

            for k, v in self.emit_configs["color"].items():
                setattr(self.config, k, v)
            setattr(self.config, "depth_mode", self.emit_configs["depth_mode"])
            self.device = start_device(config=self.config, record=False)

            for k, v in self.emit_configs["color_option"].items():
                k4a_device_set_color_control(
                    self.device._handle, color_command_dict[k], K4A_COLOR_CONTROL_MODE_MANUAL, ctypes.c_int32(int(v))
                )

            self.th.device = self.device
            self.th.audio_file = self.filename_audio

            self.btn_record.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.btn_viewer.setText("■")
            self.th.is_run = True
            self.is_viewer = False
            self.th.start()
        else:
            self.btn_record.setEnabled(True)
            self.btn_open.setEnabled(True)
            self.btn_viewer.setText("▶")
            self.th.is_run = False
            self.is_viewer = True
            self.device.close()
            self.th.quit()
            time.sleep(1)

    def recording(self) -> None:
        if self.is_record:
            self.set_filename()

            for k, v in self.emit_configs["color"].items():
                setattr(self.config, k, v)
            setattr(self.config, "depth_mode", self.emit_configs["depth_mode"])
            self.device = start_device(config=self.config, record_filepath=self.filename_video, record=True)

            for k, v in self.emit_configs["color_option"].items():
                k4a_device_set_color_control(
                    self.device._handle, color_command_dict[k], K4A_COLOR_CONTROL_MODE_MANUAL, ctypes.c_int32(int(v))
                )

            self.th.device = self.device
            self.th.audio_record = True
            self.th.audio_file = self.filename_audio

            # self.btn_viewer.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.btn_record.setText("■")
            self.th.is_run = True
            self.is_record = False
            self.th.start()
        else:
            # self.btn_viewer.setEnabled(True)
            self.btn_open.setEnabled(True)
            self.btn_record.setText("▶")
            self.th.is_run = False
            self.is_record = True
            self.device.close()
            self.th.quit()
            time.sleep(1)

    def set_filename(self) -> None:
        if self.base_path is None:
            self.base_path = os.path.join(Path.home(), "Videos")

        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")

        self.filename_video = os.path.join(self.base_path, f"{filename}.mkv")
        self.filename_audio = os.path.join(self.base_path, f"{filename}.mp3")
        if sys.flags.debug:
            print(self.base_path, self.filename_video)

    @Slot(dict)
    def setConfig(self, value: dict) -> None:
        self.emit_configs = value

    @Slot(str)
    def setBasePath(self, value: str) -> None:
        self.base_path = value

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
        self.imu_senser.label_time.setText("Time(s) : %.3f" % time)

    @Slot(float)
    def setFps(self, value) -> None:
        self.imu_senser.label_fps.setText("FPS : %.2f" % value)

    @Slot(list)
    def setAccData(self, values) -> None:
        self.imu_senser.acc_x.setText("X : %.5f" % values[0])
        self.imu_senser.acc_y.setText("Y : %.5f" % values[1])
        self.imu_senser.acc_z.setText("Z : %.5f" % values[2])

    @Slot(float)
    def setGyroData(self, values) -> None:
        self.imu_senser.gyro_x.setText("X : %.5f" % values[0])
        self.imu_senser.gyro_y.setText("Y : %.5f" % values[1])
        self.imu_senser.gyro_z.setText("Z : %.5f" % values[2])

    @Slot(list)
    def setAudioData(self, values) -> None:
        start = 0
        if values[1] < SAMPLE_COUNT:
            start = SAMPLE_COUNT - values[1]
            for s in range(start):
                self.buffer[s].setY(self.buffer[s + values[1]].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(values[0][data_index]) - 128) / 128
            self.buffer[s].setY(value)
            data_index = data_index + RESOLUTION

        self.audio_sensor.series.replace(self.buffer)
