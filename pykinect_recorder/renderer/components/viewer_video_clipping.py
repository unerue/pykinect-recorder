import os
import cv2
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Slot, Qt, QSize, QTimer
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QMainWindow,
    QPushButton, QFrame, QWidget, QFileDialog, QProgressBar
)

from ..signals import all_signals
from superqt import QLabeledRangeSlider
from pykinect_recorder.main._pyk4a.pykinect import start_playback


class VideoClippingDialog(QDialog):
    def __init__(self, file_name: str):
        super().__init__()
        self.setFixedSize(QSize(1120, 920))

        self.cnt = 0
        self.root_path = None
        self.file_name = file_name
        self.save_file_name = self.file_name.split('/')[-1][:-4]
        self.left, self.right = None, None
        self.progress_dialog = ProgressBarDialog()

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
        self.save_btn = QPushButton("추출")
        self.save_btn.setFixedHeight(40)
        self.exit_btn = QPushButton("종료")
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
        self.update_next_frame()
        self.save_btn.clicked.connect(self.select_root_path)
        self.exit_btn.clicked.connect(self.close_dialog)
        self.time_slider.valueChanged.connect(self.control_timestamp)

    def close_dialog(self):
        self.close()

    def initialize_playback(self):
        self.playback = start_playback(self.file_name)
        self.left, self.right = 0, self.playback.get_recording_length()//33333
        self.total_frame = self.right - self.left

        self.time_slider.setTickInterval(1)
        self.time_slider.setRange(self.left, self.right)  ## 마이크로세컨 -> 프레임단위
        self.time_slider.setValue([self.left, self.right])

    def control_timestamp(self):
        cur_left, cur_right = self.time_slider.value()
        if cur_left != self.left:
            self.left = cur_left
            self.playback.seek_timestamp(self.left*33333)
        elif cur_right != self.right:
            self.right = cur_right
            self.playback.seek_timestamp(self.right*33333)
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

    def colorize(self, image, clipping_range, colormap):
        if clipping_range[0] or clipping_range[1]:
            img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
        else:
            img = image.copy()
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img = cv2.applyColorMap(img, colormap)
        return img
    
    def select_root_path(self):
        self.root_path = QFileDialog.getExistingDirectory(self, "Open Data Files", ".", QFileDialog.ShowDirsOnly)
        self.extract_frame()

    def extract_frame(self):
        self.total_frame = self.right - self.left
        all_signals.video_total_frame.emit(int(self.total_frame))
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
            ir_frame = self.colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
            cv2.imwrite(os.path.join(
                self.root_path, self.save_file_name, "ir", f"{self.save_file_name}_ir_{str(self.cnt).zfill(6)}.png"), ir_frame,
            )

        if current_depth_frame[0]:
            current_depth_frame = self.colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
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
        all_signals.current_frame_cnt.emit(self.cnt)


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

        all_signals.current_frame_cnt.connect(self.set_value)
        all_signals.video_total_frame.connect(self.set_total_frame)
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