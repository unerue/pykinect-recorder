import cv2
import time

from numpy.typing import NDArray
from typing import Optional, Tuple

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QImage
from pykinect_recorder.main._pyk4a.k4arecord.playback import Playback


class PlayBackThread(QThread):
    RGBUpdateFrame = Signal(QImage)
    DepthUpdateFrame = Signal(QImage)
    IRUpdateFrame = Signal(QImage)
    Time = Signal(float)
    AccData = Signal(list)
    GyroData = Signal(list)
    Fps = Signal(float)
    
    def __init__(self, playback: Playback, parent=None) -> None:
        QThread.__init__(self, parent)
        self.playback = playback
        self.is_run = None

    def run(self):      
        while self.is_run:
            start_t = time.time()
            _, cur_frame = self.playback.update()

            # (Success flag, numpy data)
            cur_rgb_frame = cur_frame.get_color_image()
            cur_depth_frame = cur_frame.get_depth_image()
            cur_ir_frame = cur_frame.get_ir_image()
            # cur_imu_data = self.playback.update_imu()

            if cur_rgb_frame[0]:
                rgb_frame = cur_rgb_frame[1]
                rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
                
                h, w, ch = rgb_frame.shape
                rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_rgb_frame = rgb_frame.scaled(720, 440, Qt.KeepAspectRatio)
                self.RGBUpdateFrame.emit(scaled_rgb_frame)

            if cur_depth_frame[0]:
                depth_frame = self._colorize(
                    cur_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV
                )
                h, w, ch = depth_frame.shape

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(440, 440, Qt.KeepAspectRatio)
                self.DepthUpdateFrame.emit(scaled_depth_frame)

            if cur_ir_frame[0]:
                ir_frame = self._colorize(
                    cur_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE
                )
                h, w, ch = ir_frame.shape

                ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_ir_frame = ir_frame.scaled(440, 440, Qt.KeepAspectRatio)
                self.IRUpdateFrame.emit(scaled_ir_frame)

            end_time = time.time()
            # acc_time = cur_imu_data.acc_time
            # acc_data = cur_imu_data.acc
            # gyro_data = cur_imu_data.gyro
            fps = 1/(end_time-start_t)

            self.Fps.emit(fps)
            # self.Time.emit(acc_time/1e6)
            # self.AccData.emit(acc_data)
            # self.GyroData.emit(gyro_data)

        if cv2.waitKey(30) == ord("q"):
            self.is_run = False
            self.quit()

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