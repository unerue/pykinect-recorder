import os
import cv2

from superqt import QLabeledRangeSlider
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Slot, Qt, QSize, QTimer
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QWidget, QFileDialog, QProgressBar
)

from ..signals import all_signals
from ...pyk4a.utils import colorize
from ...pyk4a.pykinect import start_playback, start_device, initialize_libraries
from ...pyk4a.k4a.configuration import Configuration


class VideoClippingDialog(QDialog):
    def __init__(self, file_name: str):
        super().__init__()
        self.setFixedSize(QSize(1120, 920))

        self.cnt = 0
        self.root_path = None
        self.file_name = file_name
        self.clip_option = None
        self.save_file_name = self.file_name.split('/')[-1][:-4]
        self.left, self.right = None, None
        self.progress_dialog = ProgressBarDialog()
        self.fps_dict = {0: "5", 1: "15", 2: "30"}

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()
        # top layout
        self.top_layout = QHBoxLayout()
        self.title_layout = QHBoxLayout()
        self.title_layout.setAlignment(Qt.AlignLeft)
        self.title_label = QLabel(f"{file_name.split('/')[-1]}")
        self.title_label.setFixedHeight(40)
        self.title_layout.addWidget(self.title_label)
        
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignRight)
        self.save_btn = QPushButton("extract")
        self.save_btn.setFixedHeight(40)
        self.exit_btn = QPushButton("exit")
        self.exit_btn.setFixedHeight(40)
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.exit_btn)

        self.top_layout.addLayout(self.title_layout)
        self.top_layout.addLayout(self.btn_layout)
        self.main_layout.addLayout(self.top_layout)

        # media frame
        self.media_frame = QFrame()
        self.media_layout = QVBoxLayout()
        self.media_label = QLabel("Label")
        self.media_label.setFixedSize(QSize(1080, 720))
        self.media_label.setAlignment(Qt.AlignCenter)
        self.media_label.setStyleSheet(" border-color: white; ")
        self.media_layout.addWidget(self.media_label)
        self.media_frame.setLayout(self.media_layout)
        self.main_layout.addWidget(self.media_frame)

        # time control layout
        self.time_layout = QHBoxLayout()
        self.time_layout.setAlignment(Qt.AlignCenter)
        self.time_slider = QLabeledRangeSlider(Qt.Horizontal, self)
        self.time_slider.setStyleSheet("""
            QSlider { 
                margin: 0px;
                border-radius: 4px;
                background-color: white;
            }
            QSlider::sub-page:horizontal {
                background-color: #3f4042;
                height: 12px;
                border-radius: 4px;
            }
            QSlider::groove:horizontal {
                height: 12px;
                margin: 1px;
                border-radius: 4px;
                background-color: "#3f4042"
            }
            QSlider::handle:horizontal {
                border: 10px;
                margin: 0px;
                border-radius: 3px;
                background-color: "#00bcf8";
            }
            QSlider:handle:horizontal:hover {
                background-color: "#4d96FF";
            }
            QSlider:handle:horizontal:pressed {
                background-color: "#000000";
            }
        """)
        self.time_slider.setFixedSize(QSize(800, 80))
        self.time_layout.addWidget(self.time_slider)
        self.main_layout.addLayout(self.time_layout)
        self.setLayout(self.main_layout)

        self.initialize_playback()
        self.save_btn.clicked.connect(self.select_root_path)
        self.exit_btn.clicked.connect(self.close_dialog)
        self.time_slider.valueChanged.connect(self.control_timestamp)
        all_signals.playback_signals.clip_option.connect(self.set_clip_option)

        self.playback.seek_timestamp(self.start_time+self.ticks)
        self.update_next_frame()

    def close_dialog(self):
        self.close()

    def initialize_playback(self):
        self.playback = start_playback(self.file_name)
        self.start_time = self.playback.get_record_configuration()._handle.start_timestamp_offset_usec
        self.device_fps = self.playback.get_record_configuration()._handle.camera_fps
        self.ticks = int(1e6 // int(self.fps_dict[self.device_fps]))

        self.left = 0
        self.right = (self.playback.get_recording_length()-self.start_time) // self.ticks - 1
        self.total_frame = self.right - self.left

        self.time_slider.setTickInterval(1)
        self.time_slider.setRange(self.left, self.right)
        self.time_slider.setValue([self.left, self.right])

    def control_timestamp(self):
        cur_left, cur_right = self.time_slider.value()
        if cur_left != self.left:
            self.left = cur_left
            self.playback.seek_timestamp(self.start_time + self.left*self.ticks)
        elif cur_right != self.right:
            self.right = cur_right
            self.playback.seek_timestamp(self.start_time + self.right*self.ticks)
        self.update_next_frame()

    def update_next_frame(self):
        _, current_frame = self.playback.update()
        current_rgb_frame = current_frame.get_color_image()
        rgb_frame = current_rgb_frame[1]
        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)

        h, w, ch = rgb_frame.shape
        rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
        scaled_rgb_frame = rgb_frame.scaled(1080, 720, Qt.KeepAspectRatio)
        self.media_label.setPixmap(QPixmap.fromImage(scaled_rgb_frame))
    
    @Slot(str)
    def set_clip_option(self, value):
        self.clip_option = value

    def select_root_path(self):
        option_dialog = SelectClipOptionDialog()
        option_dialog.exec()
        self.root_path = QFileDialog.getExistingDirectory(self, "Open Data Files", ".", QFileDialog.ShowDirsOnly)
        if self.clip_option == "mkv":
            self.extract_mkv()
        elif self.clip_option == "jpg":
            self.extract_frame()

    def extract_mkv(self):
        self.total_frame = self.right - self.left
        all_signals.playback_signals.video_total_frame.emit(int(self.total_frame))
        config = self.record_config_to_config()
        
        initialize_libraries()
        self.device = start_device(
            config=config,
            record=True,
            record_filepath=os.path.join(self.root_path, self.save_file_name+"_extract.mkv")
        )
        self.playback.seek_timestamp(self.left)

        self.timer = QTimer()
        self.timer.setInterval(0.001)
        self.timer.timeout.connect(self.save_to_mkv)
        self.timer.start()
        self.progress_dialog.exec()
        self.device.close()

    def record_config_to_config(self):
        record_config = self.playback.get_record_configuration()
        config = Configuration()

        setattr(config, "color_format", record_config._handle.color_format)
        setattr(config, "depth_mode", record_config._handle.depth_mode)
        setattr(config, "color_resolution", record_config._handle.color_resolution)
        setattr(config, "camera_fps", record_config._handle.camera_fps)
        return config
        
    def save_to_mkv(self):
        if self.cnt == self.total_frame:
            self.timer.stop()

        self.cnt += 1
        self.device.save_frame_for_clip(self.playback._handle, self.playback.calibration)
        all_signals.playback_signals.current_frame_cnt.emit(self.cnt)

    def extract_frame(self):
        self.total_frame = self.right - self.left
        all_signals.playback_signals.video_total_frame.emit(int(self.total_frame))
        self.playback.seek_timestamp(self.left)
        os.makedirs(os.path.join(self.root_path, self.save_file_name, "rgb"), exist_ok=True)
        os.makedirs(os.path.join(self.root_path, self.save_file_name, "ir"), exist_ok=True)
        os.makedirs(os.path.join(self.root_path, self.save_file_name, "depth"), exist_ok=True)
        
        self.timer = QTimer()
        self.timer.setInterval(0.033)
        self.timer.timeout.connect(self.save_frame)
        self.timer.start()
        self.progress_dialog.exec()

    def save_frame(self):
        if self.cnt == self.total_frame:
            self.timer.stop()
        
        _, current_frame = self.playback.update()
        current_rgb_frame = current_frame.get_color_image()
        current_depth_frame = current_frame.get_depth_image()
        current_ir_frame = current_frame.get_ir_image()

        if current_ir_frame[0]:
            ir_frame = colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
            cv2.imwrite(os.path.join(
                self.root_path, self.save_file_name, "ir", f"{self.save_file_name}_ir_{str(self.cnt).zfill(6)}.png"), ir_frame,
            )

        if current_depth_frame[0]:
            current_depth_frame = colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
            cv2.imwrite(os.path.join(
                self.root_path, self.save_file_name, "depth", f"{self.save_file_name}_depth_{str(self.cnt).zfill(6)}.png"), current_depth_frame,
            )

        if current_rgb_frame[0]:
            rgb_frame = current_rgb_frame[1]
            cv2.imwrite(os.path.join(
                self.root_path, self.save_file_name, "rgb", f"{self.save_file_name}_rgb_{str(self.cnt).zfill(6)}.jpg"), rgb_frame,
                [cv2.IMWRITE_JPEG_QUALITY, 100]
            )
        self.cnt += 1
        all_signals.playback_signals.current_frame_cnt.emit(self.cnt)


class ProgressBarDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(500, 200))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.total_frame = None

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Extract Frames...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(QSize(450, 100))
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.progress_bar)

        all_signals.playback_signals.current_frame_cnt.connect(self.set_value)
        all_signals.playback_signals.video_total_frame.connect(self.set_total_frame)
        self.setLayout(self.main_layout)

    @Slot(int)
    def set_total_frame(self, total):
        self.total_frame = total

    @Slot(int)
    def set_value(self, value):
        if value == self.total_frame:
            self.close()
        tmp = (value / self.total_frame) * 100
        self.progress_bar.setValue(tmp)
        self.progress_bar.setFormat("%.02f %%" % tmp)


class SelectClipOptionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(500, 200))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Save To")

        self.btn_layout = QHBoxLayout()
        self.btn_mkv = QPushButton("video as '.mkv'")
        self.btn_mkv.setObjectName("btn_mkv")
        self.btn_mkv.setDisabled(True)
        self.btn_jpg = QPushButton("rgb/ir/depth frame as '.jpg'")
        self.btn_jpg.setObjectName("btn_jpg")
        self.btn_layout.addWidget(self.btn_mkv)
        self.btn_layout.addWidget(self.btn_jpg)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.btn_layout)

        self.setLayout(self.main_layout)
        self.btn_mkv.clicked.connect(self.emit_status)
        self.btn_jpg.clicked.connect(self.emit_status)

    def emit_status(self):
        if self.sender().objectName() == "btn_mkv":
            all_signals.playback_signals.clip_option.emit("mkv")
        else:
            all_signals.playback_signals.clip_option.emit("jpg")
        self.close()