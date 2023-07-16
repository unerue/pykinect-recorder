import cv2

from PySide6.QtCore import Qt, QTimer, QThread
from PySide6.QtGui import QImage
from ...pyk4a.k4arecord.playback import Playback
from ...pyk4a.utils import colorize
from ..signals import all_signals


class PlaybackSensors(QThread):
    def __init__(self, playback: Playback) -> None:
        super().__init__()
        self.playback = playback
        dict_fps = {0: "5", 1: "15", 2: "30"}
        self.device_fps = int(dict_fps[self.playback.get_record_configuration()._handle.camera_fps])

        self.timer = QTimer()
        self.timer.setInterval(1000 / self.device_fps)
        self.timer.timeout.connect(self.run)
        all_signals.playback_signals.time_control.connect(self.change_timestamp)

    def change_timestamp(self, time: int):
        self.playback.seek_timestamp(time)
        self.update_next_frame()

    def update_next_frame(self):
        try:
            _, current_frame = self.playback.update()
            current_imu_data = self.playback.get_next_imu_sample()
            current_rgb_frame = current_frame.get_color_image()
            current_depth_frame = current_frame.get_colored_depth_image()
            current_ir_frame = current_frame.get_ir_image()

            if current_rgb_frame[0]:
                rgb_frame = cv2.cvtColor(current_rgb_frame[1], cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
                all_signals.playback_signals.rgb_image.emit(rgb_frame)

            if current_depth_frame[0]:
                depth_frame = colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
                h, w, ch = depth_frame.shape
                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                all_signals.playback_signals.depth_image.emit(depth_frame)

            if current_ir_frame[0]:
                ir_frame = colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
                h, w, ch = ir_frame.shape
                ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)     
                all_signals.playback_signals.ir_image.emit(ir_frame)
    
            acc_time = current_imu_data.acc_time
            acc_data = current_imu_data.acc
            gyro_data = current_imu_data.gyro

            all_signals.playback_signals.video_fps.emit(int(self.device_fps))
            all_signals.playback_signals.record_time.emit(acc_time / 1e6)
            all_signals.playback_signals.imu_acc_data.emit(acc_data)
            all_signals.playback_signals.imu_gyro_data.emit(gyro_data)
        except:
            self.timer.stop()

    def run(self):
        all_signals.playback_signals.time_value.emit(1e6//self.device_fps)
