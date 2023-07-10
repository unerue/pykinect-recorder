import time

from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QSize, QPointF
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QFrame, QGridLayout,
    QDialog, QVBoxLayout
)
import qtawesome as qta

from .playback_sensors import PlaybackSensors
from .viewer_video_clipping import VideoClippingDialog
from .viewer_imu_sensors import ImuSensors
from ..signals import all_signals
from ..common_widgets import Frame, Slider, Label
from ...pyk4a.pykinect import initialize_libraries, start_playback


class PlaybackViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(2000, 2000))
        self.setStyleSheet("background-color: #1e1e1e;")
        self.viewer = None
        self.playback = None
        self.file_path = None
        self.is_run = False

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.captured_viewer_frame = CapturedImageViewer()
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setSpacing(10)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_stop = self.make_icons(qta.icon("mdi.stop"), "Start & Stop", scale=0.7)
        self.btn_stop.setFixedSize(50, 50)
        self.btn_stop.setStyleSheet("""
            QPushButton:hover {
                border-color: "white";
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)
        # self.btn_clip = self.make_icons(qta.icon("mdi6.scissors-cutting"),"Video Clipping", scale=0.7)
        # self.btn_clip.setFixedSize(50, 50)
        # self.btn_clip.setStyleSheet("""
        #     QPushButton:hover {
        #         border-color: "white";
        #     }
        #     QToolTip {
        #         font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
        #     }
        # """)

        self.slider_time = Slider(Qt.Orientation.Horizontal, (0, 1000000), 0)
        self.slider_time.setFixedHeight(40)
        self.slider_time.setMinimumWidth(400)
        self.slider_time.setMaximumWidth(2000)
        self.slider_time.setTickInterval(33333)
        
        self.bottom_layout.addWidget(self.btn_stop)
        # self.bottom_layout.addWidget(self.btn_clip)
        self.bottom_layout.addWidget(self.slider_time)

        self.main_layout.addWidget(self.captured_viewer_frame)
        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

        # playback signals
        self.btn_stop.clicked.connect(self.stop_playback)
        self.slider_time.valueChanged.connect(self.control_time)
        all_signals.playback_signals.time_value.connect(self.set_slider_value)
        all_signals.playback_signals.playback_filepath.connect(self.start_playback)
        
        # video clipping signals
        # self.btn_clip.clicked.connect(self.extract_video_to_frame)

    def make_icons(self, icon: qta, tooltip: str, scale: float = 0.8) -> QPushButton:
        w, h = int(35 * scale), int(35 * scale)
        btn = QPushButton(icon, "")
        btn.setFixedSize(40, 40)
        btn.setIconSize(QSize(w, h))
        btn.setToolTip(f"<b>{tooltip}<b>")
        return btn

    def set_slider_value(self, value):
        _time = self.slider_time.value() + value
        self.slider_time.setValue(_time)

    @Slot(str)
    def start_playback(self, filepath) -> None:
        if self.viewer is not None:
            time.sleep(0.5)
            self.viewer.timer.stop()
            self.btn_stop.setIcon(qta.icon("mdi.stop"))
            self.playback.close()
        try:
            self.file_path = filepath
            initialize_libraries()
            self.playback = start_playback(filepath)
            
            self.is_run = True
            self.viewer = PlaybackSensors(playback=self.playback)
            self.start_time = self.playback.get_record_configuration()._handle.start_timestamp_offset_usec
            self.slider_time.setRange(self.start_time, self.playback.get_recording_length()-self.start_time)
            self.slider_time.setValue(self.start_time)
            self.viewer.timer.start()
        except:
            modal = QDialog()
            layout_modal = QVBoxLayout()
            e_message = Label(
                "<b>Can't load video. <br>Please select another video.</b>", 
                "Arial", 20, Qt.AlignmentFlag.AlignCenter
            )
            layout_modal.addWidget(e_message)
            modal.setLayout(layout_modal)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()

    def stop_playback(self):
        if self.is_run is True:
            self.is_run = False
            self.viewer.timer.stop()
            self.btn_stop.setIcon(qta.icon("fa.play"))
        else:
            self.is_run = True
            self.viewer.timer.start()
            self.btn_stop.setIcon(qta.icon("mdi.stop"))

    def control_time(self):
        if self.viewer is not None:
            all_signals.playback_signals.time_control.emit(self.slider_time.value())

    # def extract_video_to_frame(self):
    #     self.viewer.timer.stop()
    #     video_clip_dialog = VideoClippingDialog(self.file_path)
    #     video_clip_dialog.exec_()
    #     self.viewer.timer.start()


class CapturedImageViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.target = None
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QGridLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_rgb = Frame("RGB Sensor", min_size=(460, 300), max_size=(595, 510))
        self.frame_depth = Frame("Depth Sensor", min_size=(460, 300), max_size=(595, 510))
        self.frame_ir = Frame("IR Sensor", min_size=(460, 300), max_size=(595, 510))

        self.sensor_data_layout = QHBoxLayout()
        self.sensor_data_layout.setSpacing(0)
        self.sensor_data_layout.setContentsMargins(0, 0, 0, 0)
        self.imu_senser = ImuSensors(min_size=(450, 270), max_size=(595, 480))

        self.sensor_data_layout.addWidget(self.imu_senser)
        self.frame_subdata = Frame(
            "IMU Sensor", 
            layout=self.sensor_data_layout, 
            min_size=(460, 300), 
            max_size=(595, 510)
        )

        # UI option signal
        all_signals.option_signals.clear_frame.connect(self.clear_frame)

        # Playback signals
        all_signals.playback_signals.rgb_image.connect(self.set_rgb_image)
        all_signals.playback_signals.depth_image.connect(self.set_depth_image)
        all_signals.playback_signals.ir_image.connect(self.set_ir_image)
        all_signals.playback_signals.record_time.connect(self.set_time)
        all_signals.playback_signals.video_fps.connect(self.set_fps)
        all_signals.playback_signals.imu_acc_data.connect(self.set_acc_data)
        all_signals.playback_signals.imu_gyro_data.connect(self.set_gyro_data)

        self.main_layout.addWidget(self.frame_ir, 0, 0)
        self.main_layout.addWidget(self.frame_depth, 0, 1)
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
    def set_fps(self, value) -> None:
        self.imu_senser.label_fps.setText("FPS : %.2f" % value)

    @Slot(float)
    def set_time(self, time) -> None:
        self.imu_senser.label_time.setText("Time(s) : %.3f" % time)

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
