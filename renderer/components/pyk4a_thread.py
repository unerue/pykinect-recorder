import os
import sys
import cv2
import datetime
from pathlib import Path

from numpy.typing import NDArray
from typing import Optional, Tuple

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QImage
from main._pyk4a.k4a import Device


class Pyk4aThread(QThread):
    RGBUpdateFrame = Signal(QImage)
    DepthUpdateFrame = Signal(QImage)
    IRUpdateFrame = Signal(QImage)
    
    def __init__(self, device: Device, is_record: bool, parent=None) -> None:
        QThread.__init__(self, parent)
        self.device = device
        self.is_record = is_record
        self.status = None
        
        if self.is_record:
            self.set_filename()
    
    def run(self):
        # TODO Record 불러오는 코드 추가.
        if self.is_record:
            pass
        
        while self.status:
            cur_frame = self.device.update()
            # (Success, frame)
            cur_rgb_frame = cur_frame.get_color_image()
            cur_depth_frame = cur_frame.get_depth_image()
            cur_ir_frame = cur_frame.get_ir_image()

            if cur_rgb_frame[0]:
                rgb_frame = cur_rgb_frame[1]
                rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
                
                h, w, ch = rgb_frame.shape
                rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_rgb_frame = rgb_frame.scaled(720, 440, Qt.KeepAspectRatio)
                self.RGBUpdateFrame.emit(scaled_rgb_frame)

            if cur_depth_frame[0]:
                depth_frame = self.colorize(
                    cur_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV
                )
                h, w, ch = depth_frame.shape

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(440, 440, Qt.KeepAspectRatio)
                self.DepthUpdateFrame.emit(scaled_depth_frame)

            if cur_ir_frame[0]:
                ir_frame = self.colorize(
                    cur_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE
                )
                h, w, ch = ir_frame.shape

                ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_ir_frame = ir_frame.scaled(440, 440, Qt.KeepAspectRatio)
                self.IRUpdateFrame.emit(scaled_ir_frame)
                
                
    def set_filename(self) -> None:
        base_path = os.path.join(Path.home(), "Videos")

        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")

        self.filename_video = os.path.join(base_path, f"{filename}.mkv")
        self.filename_audio = os.path.join(base_path, f"{filename}.wav")
        if sys.flags.debug:
            print(base_path, self.filename_video, self.filename_audio)
            
            
    def colorize(
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