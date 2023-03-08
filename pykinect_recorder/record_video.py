import os
import sys
import cv2
import datetime
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
from numpy.typing import NDArray
from pyk4a import PyK4A, PyK4ARecord
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QImage


class RecordVideo(QThread):
    RGBUpdateFrame = Signal(QImage)
    DepthUpdateFrame = Signal(QImage)

    def __init__(self, config, parent=None):
        QThread.__init__(self, parent)
        self.config = config
        self.status = True
        self.set_filename()

    def set_filename(self) -> None:
        base_path = os.path.join(Path.home(), 'Videos')

        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")

        self.filename_video = os.path.join(base_path, f'{filename}.mkv')
        self.filename_audio = os.path.join(base_path, f'{filename}.wav')
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

    def run(self):
        azure_device = PyK4A(config=self.config, device_id=0)
        azure_device.start()
        record = PyK4ARecord(
            device=azure_device, 
            config=self.config, 
            path=self.filename_video
        )
        record.create()
        while self.status:
            cur_frame = azure_device.get_capture()
            record.write_capture(cur_frame)

            if np.any(cur_frame.color):
                color_frame = cur_frame.color[:, :, :3].copy()
                color_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2RGB)

                h, w, ch = color_frame.shape
                if sys.flags.debug:
                    print(h, w)
                img = QImage(color_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
                self.RGBUpdateFrame.emit(scaled_img)

            if np.any(cur_frame.depth):
                depth_frame = self.colorize(cur_frame.depth, (None, 5000), cv2.COLORMAP_HSV)
                h, w, ch = depth_frame.shape
                if sys.flags.debug:
                    print(h, w)

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(400, 360, Qt.KeepAspectRatio)
                self.DepthUpdateFrame.emit(scaled_depth_frame)
