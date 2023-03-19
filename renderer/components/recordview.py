import os
import sys
import cv2
import time
import datetime
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from typing import Optional, Tuple

from PySide6.QtCore import Qt, Slot, Signal, QThread
from PySide6.QtGui import QImage, QPixmap, QFont, QPalette, QColor
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QToolTip, QFrame
)

from .sidebar import SidebarLayout
from main._pyk4a.pykinect import start_device, initialize_libraries
from main._pyk4a.k4a import Device


class RecordViewLayout(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: black;") 
        layout = QVBoxLayout()

        self.rgb_label = QLabel("RGB Sensor", self)
        self.rgb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rgb_label.setFixedWidth(440)
        self.rgb_label.setStyleSheet(
            "background-color: black; border-color: white;"
        )

        self.depth_label = QLabel("Depth Sensor", self)
        self.depth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.depth_label.setFixedWidth(440)
        self.depth_label.setStyleSheet(
            "background-color: black;"
        )

        self.ir_label = QLabel("IR Sensor", self)
        self.ir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ir_label.setFixedWidth(440)
        self.ir_label.setStyleSheet(
            "background-color: black;"
        )
        self.setFixedWidth(440)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.rgb_label)
        top_layout.addWidget(self.depth_label)

        btn_layout = QHBoxLayout()
        self.test_btn = QPushButton("test")
        self.btn_open = QPushButton("Device open")
        self.btn_viewer = QPushButton("▶")
        self.btn_record = QPushButton("●")
        self.btn_viewer.setStyleSheet("""
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            """
        )
        self.btn_viewer.setStyleSheet("background-color: red;")
        self.btn_record.setStyleSheet("""
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
            """
        )

        self.btn_viewer.setToolTip("<b>Streaming Button</b>")
        self.btn_record.setToolTip("<b>Recording Button</b>")
        
        btn_layout.addWidget(self.test_btn)
        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_viewer)
        btn_layout.addWidget(self.btn_record)
        
        self.device_flag = True
        self.viewer_flag = True
        self.record_flag = True
        self.test_btn.clicked.connect(self.set_config)
        self.btn_open.clicked.connect(self.open_device)
        self.btn_viewer.clicked.connect(self.streaming)
        self.btn_record.clicked.connect(self.recording)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.ir_label)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        

    def set_config(self) -> None:
        pass
    
    

    def open_device(self):
        if self.device_flag:
            #config = self.set_config()
            self.device_flag = False
            initialize_libraries()
            self.device = start_device()
        else:
            self.device_flag = True
            self.device = None
    
    def streaming(self) -> None:
        if self.viewer_flag:
            self.th = Pyk4aThread(device=self.device, record=False)
            self.th.RGBUpdateFrame.connect(self.setRGBImage)
            self.th.DepthUpdateFrame.connect(self.setDepthImage)
            self.th.IRUpdateFrame.connect(self.setIRImage)
            
            self.record_btn.setEnabled(False)
            self.th.status = True
            self.viewer_btn.setText("■")
            self.viewer_flag = False
            self.th.start()
        else:
            self.record_btn.setEnabled(True)
            self.th.status = False
            self.viewer_btn.setText("▶")
            self.viewer_flag = True
            time.sleep(1)
            
        
    def recording(self) -> None:
        if self.record_flag:
            self.th = Pyk4aThread(device=self.device, record=True)
            self.th.RGBUpdateFrame.connect(self.setRGBImage)
            self.th.DepthUpdateFrame.connect(self.setDepthImage)
            self.th.IRUpdateFrame.connect(self.setIRImage)
            
            self.record_btn.setEnabled(False)
            self.th.status = True
            self.viewer_btn.setText("■")
            self.viewer_flag = False
            self.th.start()
        else:
            self.record_btn.setEnabled(True)
            self.th.status = False
            self.viewer_btn.setText("▶")
            self.viewer_flag = True
            time.sleep(1)
        


    @Slot(QImage)
    def setRGBImage(self, image: QImage) -> None:
        self.rgb_label.setPixmap(QPixmap.fromImage(image))
    
    @Slot(QImage)
    def setDepthImage(self, image: QImage) -> None:
        self.depth_label.setPixmap(QPixmap.fromImage(image))
        
    @Slot(QImage)
    def setIRImage(self, image: QImage) -> None:
        self.ir_label.setPixmap(QPixmap.fromImage(image))
        
        
class Pyk4aThread(QThread):
    RGBUpdateFrame = Signal(QImage)
    DepthUpdateFrame = Signal(QImage)
    IRUpdateFrame = Signal(QImage)
    
    def __init__(self, device: Device, record: bool, parent=None) -> None:
        QThread.__init__(self, parent)
        self.device = device
        self.record = record
        self.status = None
        
        if self.record:
            self.set_filename()
    
    def run(self):
        # TODO Record 불러오는 코드 추가.
        if self.record:
            pass
        
        while self.status:
            cur_frame = self.device.update()
            # (Success, frame)
            tmp_rgb_frame = cur_frame.get_color_image()
            tmp_depth_frame = cur_frame.get_depth_image()
            tmp_ir_frame = cur_frame.get_ir_image()

            if tmp_rgb_frame[0]:
                rgb_frame = tmp_rgb_frame[1]
                rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
                
                h, w, ch = rgb_frame.shape
                rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
                scaled_rgb_frame = rgb_frame.scaled(440, 360, Qt.KeepAspectRatio)
                self.RGBUpdateFrame.emit(scaled_rgb_frame)

            if tmp_depth_frame[0]:
                depth_frame = self.colorize(
                    tmp_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV
                )
                h, w, ch = depth_frame.shape

                depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_depth_frame = depth_frame.scaled(440, 360, Qt.KeepAspectRatio)
                self.DepthUpdateFrame.emit(scaled_depth_frame)

            if tmp_ir_frame[0]:
                ir_frame = self.colorize(
                    tmp_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE
                )
                h, w, ch = ir_frame.shape

                ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
                scaled_ir_frame = ir_frame.scaled(440, 360, Qt.KeepAspectRatio)
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