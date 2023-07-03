import time

from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QSize, QPointF
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QFrame, QGridLayout,
    QDialog, QVBoxLayout
)

from .playback_sensors import PlaybackSensors
from .viewer_video_clipping import VideoClippingDialog
from .viewer_imu_sensors import ImuSensors
from .viewer_audio import AudioSensor
from ..signals import all_signals
from ..common_widgets import Frame, Slider, Label, VLine
from ...pyk4a.pykinect import initialize_libraries, start_playback


SAMPLE_COUNT = 10000
RESOLUTION = 4


class PlaybackViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(2000, 2000))
        self.setStyleSheet("background-color: #1e1e1e;")
        self.th = None
        self.playback = None
        self.file_path = None

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.captured_viewer_frame = CapturedImageViewer()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(5)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setFixedSize(100, 50)
        self.btn_stop.setStyleSheet(
            """
            QPushButton:hover {
                border-color: "white";
            }
        """
        )
        self.btn_clip = QPushButton("Clipping")
        self.btn_clip.setFixedSize(100, 50)
        self.btn_clip.setStyleSheet(
            """
            QPushButton:hover {
                border-color: "white";
            }
        """
        )

        self.slider_time = Slider(Qt.Orientation.Horizontal, (333555, 1000000), 333555)
        self.slider_time.setFixedHeight(50)
        self.slider_time.setMinimumWidth(400)
        self.slider_time.setMaximumWidth(2000)
        self.slider_time.setTickInterval(33322)
        
        self.bottom_layout.addWidget(self.btn_stop)
        self.bottom_layout.addWidget(self.btn_clip)
        self.bottom_layout.addWidget(self.slider_time)

        self.main_layout.addWidget(self.captured_viewer_frame)
        self.main_layout.addLayout(self.bottom_layout)
        
        self.target = None
        self.setLayout(self.main_layout)

        self.btn_stop.clicked.connect(self.stop_playback)
        self.btn_clip.clicked.connect(self.extract_video_to_frame)
        self.slider_time.valueChanged.connect(self.control_time)
        all_signals.time_value.connect(self.set_slider_value)
        
    def set_slider_value(self, value):
        _time = self.slider_time.value() + value
        self.slider_time.setValue(_time)

    @Slot(str)
    def start_playback(self, filepath) -> None:
        if self.th is not None:
            time.sleep(0.5)
            self.th.timer.stop()
            self.btn_stop.setText("Stop")
            self.playback.close()
        try:
            self.file_path = filepath
            initialize_libraries()
            self.playback = start_playback(filepath)
            
            self.th = PlaybackSensors(playback=self.playback)
            self.slider_time.setRange(333555, self.playback.get_recording_length())
            self.slider_time.setValue(333555)
            self.th.timer.start()
        except:
            modal = QDialog()
            layout_modal = QVBoxLayout()
            e_message = Label(
                "<b>영상을 불러올 수 없습니다. <br>다른 영상을 실행해주세요.</b>", 
                "Arial", 20, Qt.AlignmentFlag.AlignCenter
            )
            layout_modal.addWidget(e_message)
            modal.setLayout(layout_modal)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()

    def stop_playback(self):
        if self.btn_stop.text() == "Stop":
            self.th.timer.stop()
            self.btn_stop.setText("Start")
        else:
            self.th.timer.start()
            self.btn_stop.setText("Stop")

    def control_time(self):
        if self.th is not None:
            all_signals.time_control.emit(self.slider_time.value())

    def extract_video_to_frame(self):
        self.th.timer.stop()
        video_clip_dialog = VideoClippingDialog(self.file_path)
        video_clip_dialog.exec_()
        self.th.timer.start()


class CapturedImageViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.target = None
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_rgb = Frame("RGB Sensor", min_size=(480, 270), max_size=(960, 540))
        self.frame_depth = Frame("Depth Sensor", min_size=(400, 400), max_size=(800, 880))
        self.frame_ir = Frame("IR Sensor", min_size=(400, 400), max_size=(800, 800))

        self.sensor_data_layout = QHBoxLayout()
        self.sensor_data_layout.setSpacing(0)
        self.sensor_data_layout.setContentsMargins(0, 0, 0, 0)
        self.imu_senser = ImuSensors(min_size=(220, 270), max_size=(440, 540))
        self.audio_sensor = AudioSensor(min_size=(220, 270), max_size=(440, 540))

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
            min_size=(440, 270), 
            max_size=(880, 540)
        )

        self.buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        all_signals.captured_rgb.connect(self.set_rgb_image)
        all_signals.captured_depth.connect(self.set_depth_image)
        all_signals.captured_ir.connect(self.set_ir_image)
        all_signals.captured_time.connect(self.set_time)
        all_signals.captured_acc_data.connect(self.set_acc_data)
        all_signals.captured_gyro_data.connect(self.set_gyro_data)
        all_signals.captured_fps.connect(self.set_fps)
        all_signals.captured_audio.connect(self.set_audio_data)
        self.main_layout.addWidget(self.frame_depth, 0, 0)
        self.main_layout.addWidget(self.frame_ir, 0, 1)
        self.main_layout.addWidget(self.frame_rgb, 1, 0)
        self.main_layout.addWidget(self.frame_subdata, 1, 1)

        self.setAcceptDrops(True)
        self.setLayout(self.main_layout)

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
        self.frame_rgb.frame.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def set_depth_image(self, image: QImage) -> None:
        self.frame_depth.frame.setPixmap(QPixmap.fromImage(image))

    @Slot(QImage)
    def set_ir_image(self, image: QImage) -> None:
        self.frame_ir.frame.setPixmap(QPixmap.fromImage(image))

    @Slot(float)
    def set_time(self, time) -> None:
        self.imu_senser.label_time.setText("Time(s) : %.3f" % time)

    @Slot(float)
    def set_fps(self, value) -> None:
        self.imu_senser.label_fps.setText("FPS : %.2f" % value)

    @Slot(list)
    def set_acc_data(self, values) -> None:
        self.imu_senser.label_acc_x.setText("X : %.5f" % values[0])
        self.imu_senser.label_acc_y.setText("Y : %.5f" % values[1])
        self.imu_senser.label_acc_z.setText("Z : %.5f" % values[2])

    @Slot(float)
    def set_gyro_data(self, values) -> None:
        self.imu_senser.label_gyro_x.setText("X : %.5f" % values[0])
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
