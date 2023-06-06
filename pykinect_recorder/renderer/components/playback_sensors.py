import cv2
import time

from numpy.typing import NDArray
from typing import Optional, Tuple

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QImage
from pykinect_recorder.main._pyk4a.k4arecord.playback import Playback
from ..signals import all_signals


class PlaybackSensors(QThread):
    def __init__(self, playback: Playback, parent=None) -> None:
        QThread.__init__(self, parent)
        self.playback = playback
        self.is_run = None
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
            depth_frame = self._colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
            h, w, ch = depth_frame.shape

            depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
            scaled_depth_frame = depth_frame.scaled(440, 440, Qt.KeepAspectRatio)
            all_signals.captured_depth.emit(scaled_depth_frame)

        if current_ir_frame[0]:
            ir_frame = self._colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
            h, w, ch = ir_frame.shape

            ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
            scaled_ir_frame = ir_frame.scaled(440, 440, Qt.KeepAspectRatio)
            all_signals.captured_ir.emit(scaled_ir_frame)

    def run(self):
        while self.is_run:
            self.update_next_frame()

    def _colorize(
        self,
        image: NDArray,
        clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
        colormap: int = cv2.COLORMAP_HSV,
    ) -> NDArray:
        if clipping_range[0] or clipping_range[1]:
            img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
        else:
            img = image.copy()
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img = cv2.applyColorMap(img, colormap)
        return img
