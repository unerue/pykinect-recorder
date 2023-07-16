import time

import cv2
from PySide6.QtCore import Qt, QThread, QTimer
from PySide6.QtGui import QImage
from PySide6.QtMultimedia import (
    QAudioFormat,
    QAudioSource,
    QMediaDevices,
)

from ..signals import all_signals
from ...pyk4a import Device
from ...pyk4a.utils import colorize


RESOLUTION = 4


class RecordSensors(QThread):
    def __init__(self, device: Device) -> None:
        super().__init__()
        self.device = device
        self.audio_input = None
        self.input_devices = QMediaDevices.audioInputs()

        dict_fps = {0: "5", 1: "15", 2: "30"}
        self.device_fps = int(dict_fps[self.device.configuration.camera_fps])

        self.timer = QTimer()
        self.timer.setInterval(1000 / self.device_fps)
        self.timer.timeout.connect(self.update_next_frame)   

    def update_next_frame(self):
        current_frame = self.device.update()
        current_imu_data = self.device.update_imu()
        current_rgb_frame = current_frame.get_color_image()
        current_depth_frame = current_frame.get_colored_depth_image()
        current_ir_frame = current_frame.get_ir_image()

        if current_rgb_frame[0]:
            rgb_frame = cv2.cvtColor(current_rgb_frame[1], cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)    
            all_signals.record_signals.rgb_image.emit(rgb_frame)            

        if current_depth_frame[0]:
            depth_frame = colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
            h, w, ch = depth_frame.shape
            depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
            all_signals.record_signals.depth_image.emit(depth_frame)

        if current_ir_frame[0]:
            ir_frame = colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
            h, w, ch = ir_frame.shape
            ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
            all_signals.record_signals.ir_image.emit(ir_frame)

        end_time = time.time()
        acc_data = current_imu_data.acc
        gyro_data = current_imu_data.gyro

        # audio
        data = self.io_device.readAll()
        available_samples = data.size() // RESOLUTION

        all_signals.record_signals.video_fps.emit(int(self.device_fps))
        all_signals.record_signals.record_time.emit((end_time-self.start_time))
        all_signals.record_signals.imu_acc_data.emit(acc_data)
        all_signals.record_signals.imu_gyro_data.emit(gyro_data)
        all_signals.record_signals.audio_data.emit([data, available_samples])

    def start_audio(self):
        self.ready_audio()
        self.io_device = self.audio_input.start()
        self.start_time = time.time()
    
    def stop_audio(self):
        self.audio_input.stop()
        self.io_device = None

    def ready_audio(self) -> None:
        # https://github.com/ShadarRim/opencvpythonvideoplayer/blob/master/player.py
        format_audio = QAudioFormat()
        format_audio.setSampleRate(44200)
        format_audio.setChannelCount(3)
        format_audio.setSampleFormat(QAudioFormat.SampleFormat.UInt8)
        self.audio_input = QAudioSource(self.input_devices[0], format_audio)
