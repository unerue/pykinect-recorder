import cv2

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage
from ...pyk4a.k4arecord.playback import Playback
from ...pyk4a.utils import colorize
from ..signals import all_signals


class PlaybackSensors:
    def __init__(self, playback: Playback) -> None:
        self.playback = playback
        self.odd = True
        self.time_tick = 33322
        self.timer = QTimer()
        self.timer.setInterval(30)
        self.timer.timeout.connect(self.run)
        all_signals.time_control.connect(self.change_timestamp)

    def change_timestamp(self, time: int):
        self.playback.seek_timestamp(time)
        self.update_next_frame()

    def update_next_frame(self):
        _, current_frame = self.playback.update()
        current_rgb_frame = current_frame.get_color_image()
        current_depth_frame = current_frame.get_depth_image()
        current_ir_frame = current_frame.get_ir_image()

        if current_rgb_frame[0]:
            rgb_frame = current_rgb_frame[1]
            rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)

            h, w, ch = rgb_frame.shape
            rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
            scaled_rgb_frame = rgb_frame.scaled(720, 440, Qt.KeepAspectRatio)
            all_signals.captured_rgb.emit(scaled_rgb_frame)

        if current_depth_frame[0]:
            depth_frame = colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
            h, w, ch = depth_frame.shape

            depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
            scaled_depth_frame = depth_frame.scaled(440, 440, Qt.KeepAspectRatio)
            all_signals.captured_depth.emit(scaled_depth_frame)

        if current_ir_frame[0]:
            ir_frame = colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
            h, w, ch = ir_frame.shape

            ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
            scaled_ir_frame = ir_frame.scaled(440, 440, Qt.KeepAspectRatio)
            all_signals.captured_ir.emit(scaled_ir_frame)

    def run(self):
        all_signals.time_value.emit(self.time_tick)
        if self.odd:
            self.odd = False
            self.time_tick = 33345
        else:
            self.odd = True
            self.time_tick = 33322
