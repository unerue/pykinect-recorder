import os
import sys
import time
import ctypes
import datetime
from pathlib import Path

from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QPointF, QSize
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QGridLayout

from .record_sensors import RecordSensors
from .viewer_imu_sensors import ImuSensors
from .viewer_audio import AudioSensor
from .sidebar_record_control import config_sidebar
from ..signals import all_signals
from ..common_widgets import Frame, VLine, CustomProgressBarDialog
from ...pyk4a.k4a._k4a import k4a_device_set_color_control, k4a_image_set_exposure_time_usec
from ...pyk4a.k4a._k4atypes import color_command_dict, K4A_COLOR_CONTROL_MODE_MANUAL
from ...pyk4a.k4a.configuration import Configuration
from ...pyk4a.pykinect import start_device


SAMPLE_COUNT = 10000
RESOLUTION = 4


class SensorViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(1190, 1030))
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #1e1e1e; border-radius: 0px;")

        self.device = None
        self.config = Configuration()
        self.color_control = None
        self.base_path = None
        self.emit_configs = config_sidebar

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.frame_rgb = Frame("RGB Sensor", min_size=(460, 330), max_size=(595, 510))
        self.frame_depth = Frame("Depth Sensor", min_size=(460, 330), max_size=(595, 510))
        self.frame_ir = Frame("IR Sensor", min_size=(460, 330), max_size=(595, 510))

        self.sensor_data_layout = QHBoxLayout()
        self.sensor_data_layout.setSpacing(0)
        self.sensor_data_layout.setContentsMargins(0, 0, 0, 0)
        self.imu_senser = ImuSensors(min_size=(225, 300), max_size=(440, 480))
        self.audio_sensor = AudioSensor(min_size=(225, 300), max_size=(440, 480))

        self.v_line = QVBoxLayout()
        self.v_line.setSpacing(0)
        self.v_line.setContentsMargins(0, 0, 0, 0)
        self.v_line.addWidget(VLine())
        
        self.sensor_data_layout.addWidget(self.imu_senser)
        self.sensor_data_layout.addLayout(self.v_line)
        self.sensor_data_layout.addWidget(self.audio_sensor)
        self.frame_subdata = Frame(
            "IMU & Audio Sensor", 
            layout=self.sensor_data_layout, 
            min_size=(460, 330), 
            max_size=(595, 510)
        )

        self.buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.main_layout.addWidget(self.frame_ir, 0, 0)
        self.main_layout.addWidget(self.frame_depth, 0, 1)
        self.main_layout.addWidget(self.frame_rgb, 1, 0)
        self.main_layout.addWidget(self.frame_subdata, 1, 1)

        self.setAcceptDrops(True)
        self.setLayout(self.main_layout)

        self.is_play = True
        self.is_record = True
        self.setLayout(self.main_layout)

        # UI option signals 
        all_signals.option_signals.save_filepath.connect(self.set_base_path)
        all_signals.option_signals.sidebar_toggle.connect(self.set_config)
        all_signals.option_signals.device_option.connect(self.select_option)
        all_signals.option_signals.camera_option.connect(self.set_config)
        all_signals.option_signals.clear_frame.connect(self.clear_frame)
        
        # Recording signals
        all_signals.record_signals.rgb_image.connect(self.set_rgb_image)
        all_signals.record_signals.depth_image.connect(self.set_depth_image)
        all_signals.record_signals.ir_image.connect(self.set_ir_image)
        all_signals.record_signals.record_time.connect(self.set_time)
        all_signals.record_signals.video_fps.connect(self.set_fps)
        all_signals.record_signals.imu_acc_data.connect(self.set_acc_data)
        all_signals.record_signals.imu_gyro_data.connect(self.set_gyro_data)
        all_signals.record_signals.audio_data.connect(self.set_audio_data)

    def select_option(self, value):
        if value == "viewer":
            self.streaming()
        else:
            self.recording()

    def streaming(self) -> None:
        self.is_record = False
        self.play()

    def recording(self) -> None:
        self.is_record = True
        self.play()

    def play(self) -> None:
        if self.is_play:
            self.set_filename()
            for k, v in self.emit_configs["color"].items():
                setattr(self.config, k, v)
                
            self.device = start_device(
                config=self.config, 
                record=self.is_record, 
                record_filepath=self.filename_video
            )
            setattr(self.config, "depth_mode", self.emit_configs["depth_mode"])
            for k, v in self.emit_configs["color_option"].items():
                k4a_device_set_color_control(
                    self.device._handle, color_command_dict[k], K4A_COLOR_CONTROL_MODE_MANUAL, ctypes.c_int32(int(v))
                )

            self.viewer = RecordSensors(device=self.device)
            self.viewer.start_audio()
            self.viewer.timer.start()
            self.is_play = False
        else:
            self.viewer.timer.stop()
            self.viewer.stop_audio()
            self.viewer.quit()
            self.device.close()
            self.is_play = True

            if self.is_record:
                wait_dialog = CustomProgressBarDialog(msec=500)
                wait_dialog.show()

    def set_filename(self) -> None:
        if self.base_path is None:
            self.base_path = os.path.join(Path.home(), "Videos")

        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")

        self.filename_video = os.path.join(self.base_path, f"{filename}.mkv")
        if sys.flags.debug:
            print(self.base_path, self.filename_video)

    @Slot(dict)
    def set_config(self, value: dict) -> None:
        self.emit_configs = value

    @Slot(str)
    def set_base_path(self, value: str) -> None:
        self.base_path = value

    def eventFilter(self, watched, event):
        if event.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(event)
        elif event.type() == QEvent.MouseMove:
            self.mouseMoveEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            self.mouseReleaseEvent(event)
        return super().eventFilter(watched, event)

    def get_index(self, pos):
        for i in range(self.main_layout.count()):
            if self.main_layout.itemAt(i).geometry().contains(pos) and i != self.target:
                return i

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.target = self.get_index(event.windowPos().toPoint())
        else:
            self.target = None

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.target is not None:
            drag = QDrag(self.main_layout.itemAt(self.target).widget())
            pix = self.main_layout.itemAt(self.target).widget().grab()
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
            p1, p2 = self.main_layout.getItemPosition(i), self.main_layout.getItemPosition(j)

            self.main_layout.addItem(self.main_layout.takeAt(i), *p2)
            self.main_layout.addItem(self.main_layout.takeAt(j), *p1)
            event.accept()

    @Slot(QImage)
    def set_rgb_image(self, image: QImage) -> None:
        w, h = self.frame_rgb.label_image.width(), self.frame_rgb.label_image.height()
        image = image.scaled(w-5, h-5, Qt.KeepAspectRatio)
        self.frame_rgb.label_image.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def set_depth_image(self, image: QImage) -> None:
        w, h = self.frame_depth.label_image.width(), self.frame_depth.label_image.height()
        image = image.scaled(w-5, h-5, Qt.KeepAspectRatio)
        self.frame_depth.label_image.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def set_ir_image(self, image: QImage) -> None:
        w, h = self.frame_ir.label_image.width(), self.frame_ir.label_image.height()
        image = image.scaled(w-5, h-5, Qt.KeepAspectRatio)
        self.frame_ir.label_image.setPixmap(QPixmap.fromImage(image))

    @Slot(float)
    def set_time(self, time) -> None:
        self.imu_senser.label_time.setText("Time(s) : %.3f" % time)

    @Slot(int)
    def set_fps(self, value) -> None:
        self.imu_senser.label_fps.setText("FPS : %d" % value)

    @Slot(list)
    def set_acc_data(self, values) -> None:
        self.imu_senser.label_acc_x.setText("X : %.5f" % values[0])
        self.imu_senser.label_acc_y.setText("Y : %.5f" % values[1])
        self.imu_senser.label_acc_z.setText("Z : %.5f" % values[2])

    @Slot(float)
    def set_gyro_data(self, values) -> None:
        # self.imu_senser.label_gyro_x.setText("X : %.5f" % values[0])
        self.imu_senser.label_gyro_x.setText(f"X : {values[0]:.5f}")
        self.imu_senser.label_gyro_y.setText("Y : %.5f" % values[1])
        self.imu_senser.label_gyro_z.setText("Z : %.5f" % values[2])

    @Slot(list)
    def set_audio_data(self, values) -> None:
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

    def clear_frame(self):
        self.frame_rgb.label_image.clear()
        self.frame_depth.label_image.clear()
        self.frame_ir.label_image.clear()
        self.imu_senser.label_time.setText("Time(s) : ")
        self.imu_senser.label_fps.setText("FPS : ")
        self.imu_senser.label_acc_x.setText("X : ")
        self.imu_senser.label_acc_y.setText("Y : ")
        self.imu_senser.label_acc_z.setText("Z : ")
        self.imu_senser.label_gyro_x.setText("X : ")
        self.imu_senser.label_gyro_y.setText("Y : ")
        self.imu_senser.label_gyro_z.setText("Z : ")
    