import os
import sys
import ctypes
import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFrame,
    QSizePolicy,
    QScrollArea,
    QRadioButton
)

from PySide6.QtCore import Qt, QSize, Slot
import qtawesome as qta

from .mediapipe_control import MediaPipeObjectDetector, MediaPipeConfig, MediaPipeModel
from ..common_widgets import HLine
from ..signals import all_signals
from ...pyk4a.k4a.configuration import Configuration
from ...pyk4a.pykinect import start_device

class SolutionSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: #252526;
        """)
        self.setMinimumSize(QSize(200, 670))
        self.setMaximumSize(QSize(330, 1340))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # define variables 
        self.is_run = True
        self.config = None
        self.obj_detect_title_btn_clicked = True
        self.mediapipe_semantic_seg_title_btn_clicked = True
        self.mediapipe_face_detect_title_btn_clicked = True
        self.mediapipe_pose_landmark_title_btn_clicked = True

        # define layouts
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Vision Solutions")
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
        """)
        self.btn_start = QPushButton("Start")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setStyleSheet("""
            QPushButton#btn_start {
                color: white;
                font-size: 13px;
                background-color: #1e1e1e;
                border: 1px solid #1e1e1e;
                border-radius: 0px;
            }
            QPushButton#btn_start:hover {
                background-color: #1e1e1e;
                border: 1px solid white;
            }
        """)
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch()
        self.title_layout.addWidget(self.btn_start)
        self.main_layout.addLayout(self.title_layout)

        # define option scroll area
        self.option_scroll_area = QScrollArea()
        self.option_scroll_area.setWidgetResizable(True)
        self.option_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.option_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.widget_option = QWidget()
        self.option_layout = QVBoxLayout(self.widget_option)
        self.option_layout.setSpacing(5)
        self.option_layout.setContentsMargins(0, 0, 0, 0)
        self.option_layout.setAlignment(Qt.AlignTop) 

        self.mediapipe_frame = QFrame()
        self.mediapipe_frame.setObjectName("mediapipe")
        self.mediapipe_frame.setStyleSheet("""
            QFrame#mediapipe {
                border: 1px solid white;                         
            }
        """)
        
        self.mediapipe_layout = QVBoxLayout(self.mediapipe_frame)
        self.mediapipe_layout.setSpacing(0)
        self.mediapipe_layout.setContentsMargins(5, 0, 5, 0)
        self.mediapipe_layout.setAlignment(Qt.AlignTop)

        self.mediapipe_title_layout = QHBoxLayout()
        self.mediapipe_title_layout.setSpacing(0)
        self.mediapipe_title_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_title_layout.setAlignment(Qt.AlignLeft)
        self.title_label = QLabel("MediaPipe")
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
            padding: 10px;
        """)
        self.mediapipe_title_layout.addWidget(self.title_label)
        self.mediapipe_layout.addLayout(self.mediapipe_title_layout)
        self.mediapipe_layout.addWidget(HLine())

        self.mediapipe_obj_detect_layout = QVBoxLayout()
        self.mediapipe_obj_detect_layout.setSpacing(0)
        self.mediapipe_obj_detect_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_obj_detect_layout.setAlignment(Qt.AlignTop)
        
        self.mediapipe_obj_detect_title_layout = QHBoxLayout()
        self.mediapipe_obj_detect_title_layout.setSpacing(0)
        self.mediapipe_obj_detect_title_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_obj_detect_title_layout.setAlignment(Qt.AlignLeft)

        #fa.caret-down
        self.obj_detect_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Object detection')
        self.obj_detect_title_btn.setObjectName("Object detection")
        self.obj_detect_title_btn.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
        """)

        self.obj_detect_title_btn.setFlat(True)
        self.mediapipe_obj_detect_title_layout.addWidget(self.obj_detect_title_btn)
        self.mediapipe_obj_detect_layout.addLayout(self.mediapipe_obj_detect_title_layout)

        self.mediapipe_obj_detect_option_layout = QVBoxLayout()
        self.mediapipe_obj_detect_option_layout.setSpacing(0)
        self.mediapipe_obj_detect_option_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_obj_detect_option_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_obj_detect_option_btn1 = CustomOptionButton("efficientdet_lite0_int8", "object_detection")
        self.mediapipe_obj_detect_option_btn2 = CustomOptionButton("efficientdet_lite0_float16", "object_detection")
        self.mediapipe_obj_detect_option_btn3 = CustomOptionButton("efficientdet_lite0_float32", "object_detection")
        self.mediapipe_obj_detect_option_btn4 = CustomOptionButton("efficientdet_lite2_int8", "object_detection")
        self.mediapipe_obj_detect_option_btn5 = CustomOptionButton("efficientdet_lite2_float16", "object_detection")
        self.mediapipe_obj_detect_option_btn6 = CustomOptionButton("efficientdet_lite2_float32", "object_detection")
        self.mediapipe_obj_detect_option_btn7 = CustomOptionButton("ssdmobilenet_v2_int8", "object_detection")
        self.mediapipe_obj_detect_option_btn8 = CustomOptionButton("ssdmobilenet_v2_float32", "object_detection")

        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn1)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn2)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn3)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn4)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn5)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn6)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn7)
        self.mediapipe_obj_detect_option_layout.addWidget(self.mediapipe_obj_detect_option_btn8)
        self.mediapipe_obj_detect_layout.addLayout(self.mediapipe_obj_detect_option_layout)

        # segmentation
        self.mediapipe_semantic_seg_layout = QVBoxLayout()
        self.mediapipe_semantic_seg_layout.setSpacing(0)
        self.mediapipe_semantic_seg_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_semantic_seg_layout.setAlignment(Qt.AlignTop)
        
        self.mediapipe_semantic_seg_title_layout = QHBoxLayout()
        self.mediapipe_semantic_seg_title_layout.setSpacing(0)
        self.mediapipe_semantic_seg_title_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_semantic_seg_title_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_semantic_seg_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Semantic segmentation')
        self.mediapipe_semantic_seg_title_btn.setObjectName("Semantic segmentation")
        self.mediapipe_semantic_seg_title_btn.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
        """)

        self.mediapipe_semantic_seg_title_btn.setFlat(True)
        self.mediapipe_semantic_seg_title_layout.addWidget(self.mediapipe_semantic_seg_title_btn)
        self.mediapipe_semantic_seg_layout.addLayout(self.mediapipe_semantic_seg_title_layout)

        self.mediapipe_semantic_seg_option_layout = QVBoxLayout()
        self.mediapipe_semantic_seg_option_layout.setSpacing(0)
        self.mediapipe_semantic_seg_option_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_semantic_seg_option_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_semantic_seg_option_btn1 = CustomOptionButton("SSD", "semantic_segmentation")
        self.mediapipe_semantic_seg_option_btn2 = CustomOptionButton("SSD", "semantic_segmentation")
        self.mediapipe_semantic_seg_option_btn3 = CustomOptionButton("SSD", "semantic_segmentation")
        self.mediapipe_semantic_seg_option_btn4 = CustomOptionButton("SSD", "semantic_segmentation")
        self.mediapipe_semantic_seg_option_btn5 = CustomOptionButton("SSD", "semantic_segmentation")

        self.mediapipe_semantic_seg_option_layout.addWidget(self.mediapipe_semantic_seg_option_btn1)
        self.mediapipe_semantic_seg_option_layout.addWidget(self.mediapipe_semantic_seg_option_btn2)
        self.mediapipe_semantic_seg_option_layout.addWidget(self.mediapipe_semantic_seg_option_btn3)
        self.mediapipe_semantic_seg_option_layout.addWidget(self.mediapipe_semantic_seg_option_btn4)
        self.mediapipe_semantic_seg_option_layout.addWidget(self.mediapipe_semantic_seg_option_btn5)
        self.mediapipe_semantic_seg_layout.addLayout(self.mediapipe_semantic_seg_option_layout)

        # face detection
        self.mediapipe_face_detect_layout = QVBoxLayout()
        self.mediapipe_face_detect_layout.setSpacing(0)
        self.mediapipe_face_detect_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_face_detect_layout.setAlignment(Qt.AlignTop)
        
        self.mediapipe_face_detect_title_layout = QHBoxLayout()
        self.mediapipe_face_detect_title_layout.setSpacing(0)
        self.mediapipe_face_detect_title_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_face_detect_title_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_face_detect_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Face detection')
        self.mediapipe_face_detect_title_btn.setObjectName("Face detection")
        self.mediapipe_face_detect_title_btn.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
        """)

        self.mediapipe_face_detect_title_btn.setFlat(True)
        self.mediapipe_face_detect_title_layout.addWidget(self.mediapipe_face_detect_title_btn)
        self.mediapipe_face_detect_layout.addLayout(self.mediapipe_face_detect_title_layout)

        self.mediapipe_face_detect_option_layout = QVBoxLayout()
        self.mediapipe_face_detect_option_layout.setSpacing(0)
        self.mediapipe_face_detect_option_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_face_detect_option_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_face_detect_option_btn1 = CustomOptionButton("SSD", "face_detection")
        self.mediapipe_face_detect_option_btn2 = CustomOptionButton("SSD", "face_detection")
        self.mediapipe_face_detect_option_btn3 = CustomOptionButton("SSD", "face_detection")
        self.mediapipe_face_detect_option_btn4 = CustomOptionButton("SSD", "face_detection")
        self.mediapipe_face_detect_option_btn5 = CustomOptionButton("SSD", "face_detection")

        self.mediapipe_face_detect_option_layout.addWidget(self.mediapipe_face_detect_option_btn1)
        self.mediapipe_face_detect_option_layout.addWidget(self.mediapipe_face_detect_option_btn2)
        self.mediapipe_face_detect_option_layout.addWidget(self.mediapipe_face_detect_option_btn3)
        self.mediapipe_face_detect_option_layout.addWidget(self.mediapipe_face_detect_option_btn4)
        self.mediapipe_face_detect_option_layout.addWidget(self.mediapipe_face_detect_option_btn5)
        self.mediapipe_face_detect_layout.addLayout(self.mediapipe_face_detect_option_layout)

        # pose landmark detection
        self.mediapipe_pose_landmark_layout = QVBoxLayout()
        self.mediapipe_pose_landmark_layout.setSpacing(0)
        self.mediapipe_pose_landmark_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_pose_landmark_layout.setAlignment(Qt.AlignTop)
        
        self.mediapipe_pose_landmark_title_layout = QHBoxLayout()
        self.mediapipe_pose_landmark_title_layout.setSpacing(0)
        self.mediapipe_pose_landmark_title_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_pose_landmark_title_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_pose_landmark_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Pose landmark detection')
        self.mediapipe_pose_landmark_title_btn.setObjectName("Pose landmark detection")
        self.mediapipe_pose_landmark_title_btn.setStyleSheet("""
            color: white;
            font-size: 12px;
            font-weight: bold;
        """)

        self.mediapipe_pose_landmark_title_btn.setFlat(True)
        self.mediapipe_pose_landmark_title_layout.addWidget(self.mediapipe_pose_landmark_title_btn)
        self.mediapipe_pose_landmark_layout.addLayout(self.mediapipe_pose_landmark_title_layout)

        self.mediapipe_pose_landmark_option_layout = QVBoxLayout()
        self.mediapipe_pose_landmark_option_layout.setSpacing(0)
        self.mediapipe_pose_landmark_option_layout.setContentsMargins(0, 0, 0, 0)
        self.mediapipe_pose_landmark_option_layout.setAlignment(Qt.AlignLeft)

        self.mediapipe_pose_landmark_option_btn1 = CustomOptionButton("SSD", "pose_landmark_detection")
        self.mediapipe_pose_landmark_option_btn2 = CustomOptionButton("SSD", "pose_landmark_detection")
        self.mediapipe_pose_landmark_option_btn3 = CustomOptionButton("SSD", "pose_landmark_detection")
        self.mediapipe_pose_landmark_option_btn4 = CustomOptionButton("SSD", "pose_landmark_detection")
        self.mediapipe_pose_landmark_option_btn5 = CustomOptionButton("SSD", "pose_landmark_detection")

        self.mediapipe_pose_landmark_option_layout.addWidget(self.mediapipe_pose_landmark_option_btn1)
        self.mediapipe_pose_landmark_option_layout.addWidget(self.mediapipe_pose_landmark_option_btn2)
        self.mediapipe_pose_landmark_option_layout.addWidget(self.mediapipe_pose_landmark_option_btn3)
        self.mediapipe_pose_landmark_option_layout.addWidget(self.mediapipe_pose_landmark_option_btn4)
        self.mediapipe_pose_landmark_option_layout.addWidget(self.mediapipe_pose_landmark_option_btn5)
        self.mediapipe_pose_landmark_layout.addLayout(self.mediapipe_pose_landmark_option_layout)

        # add to scroll layout
        self.mediapipe_layout.addLayout(self.mediapipe_obj_detect_layout)
        self.mediapipe_layout.addLayout(self.mediapipe_semantic_seg_layout)
        self.mediapipe_layout.addLayout(self.mediapipe_face_detect_layout)
        self.mediapipe_layout.addLayout(self.mediapipe_pose_landmark_layout)
        self.option_layout.addWidget(self.mediapipe_frame)

        # set main layout
        self.option_scroll_area.setWidget(self.widget_option)
        self.main_layout.addWidget(self.option_scroll_area)
        self.setLayout(self.main_layout)

        self.btn_start.clicked.connect(self.start_mediapipe)
        self.obj_detect_title_btn.clicked.connect(self.option_toggle)
        self.mediapipe_semantic_seg_title_btn.clicked.connect(self.option_toggle)
        self.mediapipe_face_detect_title_btn.clicked.connect(self.option_toggle)
        self.mediapipe_pose_landmark_title_btn.clicked.connect(self.option_toggle)
        all_signals.mediapipe_signals.model_config.connect(self.set_config)

    def option_toggle(self) -> None:
        if self.sender().objectName() == "Object detection":
            if self.obj_detect_title_btn_clicked:
                self.obj_detect_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.mediapipe_obj_detect_option_layout.count()):
                    self.mediapipe_obj_detect_option_layout.itemAt(i).widget().hide()
            else:
                self.obj_detect_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.mediapipe_obj_detect_option_layout.count()):
                    self.mediapipe_obj_detect_option_layout.itemAt(i).widget().show() 
            self.obj_detect_title_btn_clicked = not self.obj_detect_title_btn_clicked

        elif self.sender().objectName() == "Semantic segmentation":
            if self.mediapipe_semantic_seg_title_btn_clicked:
                self.mediapipe_semantic_seg_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.mediapipe_semantic_seg_option_layout.count()):
                    self.mediapipe_semantic_seg_option_layout.itemAt(i).widget().hide()
            else:
                self.mediapipe_semantic_seg_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.mediapipe_semantic_seg_option_layout.count()):
                    self.mediapipe_semantic_seg_option_layout.itemAt(i).widget().show() 
            self.mediapipe_semantic_seg_title_btn_clicked = not self.mediapipe_semantic_seg_title_btn_clicked

        elif self.sender().objectName() == "Face detection":
            if self.mediapipe_face_detect_title_btn_clicked:
                self.mediapipe_face_detect_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.mediapipe_face_detect_option_layout.count()):
                    self.mediapipe_face_detect_option_layout.itemAt(i).widget().hide()
            else:
                self.mediapipe_face_detect_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.mediapipe_face_detect_option_layout.count()):
                    self.mediapipe_face_detect_option_layout.itemAt(i).widget().show()
            self.mediapipe_face_detect_title_btn_clicked = not self.mediapipe_face_detect_title_btn_clicked

        elif self.sender().objectName() == "Pose landmark detection":
            if self.mediapipe_pose_landmark_title_btn_clicked:
                self.mediapipe_pose_landmark_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.mediapipe_pose_landmark_option_layout.count()):
                    self.mediapipe_pose_landmark_option_layout.itemAt(i).widget().hide()
            else:
                self.mediapipe_pose_landmark_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.mediapipe_pose_landmark_option_layout.count()):
                    self.mediapipe_pose_landmark_option_layout.itemAt(i).widget().show()
            self.mediapipe_pose_landmark_title_btn_clicked = not self.mediapipe_pose_landmark_title_btn_clicked

    @Slot(list)
    def set_config(self, value: list[str, str]) -> None:
        self.config = value

    def set_filename(self) -> None:
        self.base_path = os.path.join(Path.home(), "Videos")
        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")
        self.filename_video = os.path.join(self.base_path, f"{filename}.mkv")

    def start_mediapipe(self) -> None:
        media_config = MediaPipeConfig()
        media_config.set_config(self.config)
        media_model = MediaPipeModel(media_config)
        if self.is_run:
            self.set_filename()
            self.device = start_device(
                config=Configuration(), 
                record=False,
                record_filepath=self.filename_video
            )
            self.detector = MediaPipeObjectDetector(self.device, media_model)
            self.detector.timer.start()
            self.btn_start.setText("Stop")
            self.is_run = False
        else:
            self.detector.timer.stop()
            self.detector.quit()
            self.device.close()
            self.btn_start.setText("Start")
            self.is_run = True


class CustomOptionButton(QRadioButton):
    def __init__(self, name: str, option: str) -> None:
        super().__init__()
        self.setText(name)
        self.setObjectName(name)
        self.setFixedHeight(30)
        self.setMinimumWidth(280)
        self.setMaximumWidth(320)
        self.setStyleSheet("""
            QRadioButton {
                color: white;
                font-size: 11px;
                font-weight: bold;
                border: 1px solid transparent;
                text-align:left;
                margin-left: 30px;
            }
            QRadioButton:hover {
                border-color: red;
            }
        """)

        self.option = option
        self.clicked.connect(self.select_option)

    def select_option(self) -> None:
        all_signals.mediapipe_signals.model_config.emit([self.option, self.objectName()])