import time
from PySide6.QtCore import Qt, Slot, QEvent, QMimeData
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QFrame, QGridLayout,
    QDialog, QVBoxLayout
)

from ..common_widgets import Frame, Slider, Label
from .playback_sensors import PlaybackSensors
from .viewer_video_clipping import VideoClippingDialog
from .viewer_imu_sensors import ImuSensors
from .viewer_audio import AudioSensor
from pykinect_recorder.main._pyk4a.pykinect import initialize_libraries, start_playback
from ..signals import all_signals


SAMPLE_COUNT = 10000
RESOLUTION = 4


class PlaybackViewer(QFrame):
    def __init__(self, size: tuple[int, int] = (1200, 1000)) -> None:
        super().__init__()

        self.setStyleSheet("background-color: #1e1e1e;")
        self.th = None
        self.playback = None
        self.file_path = None
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

        layout_top = QHBoxLayout()
        layout_top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider_time = Slider(Qt.Orientation.Horizontal, (333555, 1000000), 333555)
        self.slider_time.setFixedSize(400, 40)
        self.slider_time.setTickInterval(33322)
        layout_top.addWidget(self.slider_time)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setFixedSize(200, 40)
        self.btn_stop.setStyleSheet(
            """
            QPushButton:hover {
                border-color: "white";
            }
        """
        )
        self.btn_clip = QPushButton("Clipping")
        self.btn_clip.setFixedSize(200, 40)
        self.btn_clip.setStyleSheet(
            """
            QPushButton:hover {
                border-color: "white";
            }
        """
        )
        layout_top.addWidget(self.btn_stop)
        layout_top.addWidget(self.btn_clip)
        self.btn_stop.clicked.connect(self.stop_playback)
        self.btn_clip.clicked.connect(self.extract_video_to_frame)
        self.slider_time.valueChanged.connect(self.control_time)

        self.target = None
        self.grid_layout.addLayout(layout_top, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.frame_rgb, 1, 0)
        self.grid_layout.addWidget(self.frame_depth, 1, 1)
        self.grid_layout.addWidget(self.frame_ir, 2, 0)
        self.grid_layout.addWidget(self.frame_subdata, 2, 1)

        all_signals.captured_rgb.connect(self.setRGBImage)
        all_signals.captured_depth.connect(self.setDepthImage)
        all_signals.captured_ir.connect(self.setIRImage)
        all_signals.captured_time.connect(self.setTime)
        all_signals.captured_fps.connect(self.setFps)
        all_signals.time_value.connect(self.set_slider_value)
        
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
            playback_config = self.playback.get_record_configuration()
            
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

    def extract_video_to_frame(self):
        self.th.timer.stop()
        video_clip_dialog = VideoClippingDialog(self.file_path)
        video_clip_dialog.exec_()
        self.th.timer.start()