from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QFrame,
    QSizePolicy,
    QScrollArea,
)
from PySide6.QtCore import Qt, QSize
import qtawesome as qta

class SolutionSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: #252526;
            border-radius: 0px;                   
        """)
        self.setMinimumSize(QSize(200, 670))
        self.setMaximumSize(QSize(330, 1340))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # define variables 
        self.obj_detect_title_btn_clicked = True
        self.semantic_seg_title_btn_clicked = True
        self.face_detect_title_btn_clicked = True
        self.pose_landmark_title_btn_clicked = True

        # define layouts
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.title_layout = QVBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("Mediapipe Solutions")
        self.title_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 10px;
        """)
        self.title_layout.addWidget(self.title_label)
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

        self.obj_detect_layout = QVBoxLayout()
        self.obj_detect_layout.setSpacing(0)
        self.obj_detect_layout.setContentsMargins(0, 0, 0, 0)
        self.obj_detect_layout.setAlignment(Qt.AlignTop)
        
        self.obj_detect_title_layout = QHBoxLayout()
        self.obj_detect_title_layout.setSpacing(0)
        self.obj_detect_title_layout.setContentsMargins(0, 0, 0, 0)
        self.obj_detect_title_layout.setAlignment(Qt.AlignLeft)

        #fa.caret-down
        self.obj_detect_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Object detection')
        self.obj_detect_title_btn.setObjectName("Object detection")
        self.obj_detect_title_btn.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
        """)

        self.obj_detect_title_btn.setFlat(True)
        self.obj_detect_title_layout.addWidget(self.obj_detect_title_btn)
        self.obj_detect_layout.addLayout(self.obj_detect_title_layout)

        self.obj_detect_option_layout = QVBoxLayout()
        self.obj_detect_option_layout.setSpacing(0)
        self.obj_detect_option_layout.setContentsMargins(0, 0, 0, 0)
        self.obj_detect_option_layout.setAlignment(Qt.AlignLeft)

        self.obj_detect_option_btn1 = CustomOptionButton("SSD")
        self.obj_detect_option_btn2 = CustomOptionButton("SSD")
        self.obj_detect_option_btn3 = CustomOptionButton("SSD")
        self.obj_detect_option_btn4 = CustomOptionButton("SSD")
        self.obj_detect_option_btn5 = CustomOptionButton("SSD")

        self.obj_detect_option_layout.addWidget(self.obj_detect_option_btn1)
        self.obj_detect_option_layout.addWidget(self.obj_detect_option_btn2)
        self.obj_detect_option_layout.addWidget(self.obj_detect_option_btn3)
        self.obj_detect_option_layout.addWidget(self.obj_detect_option_btn4)
        self.obj_detect_option_layout.addWidget(self.obj_detect_option_btn5)
        self.obj_detect_layout.addLayout(self.obj_detect_option_layout)

        # segmentation
        self.semantic_seg_layout = QVBoxLayout()
        self.semantic_seg_layout.setSpacing(0)
        self.semantic_seg_layout.setContentsMargins(0, 0, 0, 0)
        self.semantic_seg_layout.setAlignment(Qt.AlignTop)
        
        self.semantic_seg_title_layout = QHBoxLayout()
        self.semantic_seg_title_layout.setSpacing(0)
        self.semantic_seg_title_layout.setContentsMargins(0, 0, 0, 0)
        self.semantic_seg_title_layout.setAlignment(Qt.AlignLeft)

        self.semantic_seg_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Semantic segmentation')
        self.semantic_seg_title_btn.setObjectName("Semantic segmentation")
        self.semantic_seg_title_btn.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
        """)

        self.semantic_seg_title_btn.setFlat(True)
        self.semantic_seg_title_layout.addWidget(self.semantic_seg_title_btn)
        self.semantic_seg_layout.addLayout(self.semantic_seg_title_layout)

        self.semantic_seg_option_layout = QVBoxLayout()
        self.semantic_seg_option_layout.setSpacing(0)
        self.semantic_seg_option_layout.setContentsMargins(0, 0, 0, 0)
        self.semantic_seg_option_layout.setAlignment(Qt.AlignLeft)

        self.semantic_seg_option_btn1 = CustomOptionButton("SSD")
        self.semantic_seg_option_btn2 = CustomOptionButton("SSD")
        self.semantic_seg_option_btn3 = CustomOptionButton("SSD")
        self.semantic_seg_option_btn4 = CustomOptionButton("SSD")
        self.semantic_seg_option_btn5 = CustomOptionButton("SSD")

        self.semantic_seg_option_layout.addWidget(self.semantic_seg_option_btn1)
        self.semantic_seg_option_layout.addWidget(self.semantic_seg_option_btn2)
        self.semantic_seg_option_layout.addWidget(self.semantic_seg_option_btn3)
        self.semantic_seg_option_layout.addWidget(self.semantic_seg_option_btn4)
        self.semantic_seg_option_layout.addWidget(self.semantic_seg_option_btn5)
        self.semantic_seg_layout.addLayout(self.semantic_seg_option_layout)

        # face detection
        self.face_detect_layout = QVBoxLayout()
        self.face_detect_layout.setSpacing(0)
        self.face_detect_layout.setContentsMargins(0, 0, 0, 0)
        self.face_detect_layout.setAlignment(Qt.AlignTop)
        
        self.face_detect_title_layout = QHBoxLayout()
        self.face_detect_title_layout.setSpacing(0)
        self.face_detect_title_layout.setContentsMargins(0, 0, 0, 0)
        self.face_detect_title_layout.setAlignment(Qt.AlignLeft)

        self.face_detect_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Face detection')
        self.face_detect_title_btn.setObjectName("Face detection")
        self.face_detect_title_btn.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
        """)

        self.face_detect_title_btn.setFlat(True)
        self.face_detect_title_layout.addWidget(self.face_detect_title_btn)
        self.face_detect_layout.addLayout(self.face_detect_title_layout)

        self.face_detect_option_layout = QVBoxLayout()
        self.face_detect_option_layout.setSpacing(0)
        self.face_detect_option_layout.setContentsMargins(0, 0, 0, 0)
        self.face_detect_option_layout.setAlignment(Qt.AlignLeft)

        self.face_detect_option_btn1 = CustomOptionButton("SSD")
        self.face_detect_option_btn2 = CustomOptionButton("SSD")
        self.face_detect_option_btn3 = CustomOptionButton("SSD")
        self.face_detect_option_btn4 = CustomOptionButton("SSD")
        self.face_detect_option_btn5 = CustomOptionButton("SSD")

        self.face_detect_option_layout.addWidget(self.face_detect_option_btn1)
        self.face_detect_option_layout.addWidget(self.face_detect_option_btn2)
        self.face_detect_option_layout.addWidget(self.face_detect_option_btn3)
        self.face_detect_option_layout.addWidget(self.face_detect_option_btn4)
        self.face_detect_option_layout.addWidget(self.face_detect_option_btn5)
        self.face_detect_layout.addLayout(self.face_detect_option_layout)

        # pose landmark detection
        self.pose_landmark_layout = QVBoxLayout()
        self.pose_landmark_layout.setSpacing(0)
        self.pose_landmark_layout.setContentsMargins(0, 0, 0, 0)
        self.pose_landmark_layout.setAlignment(Qt.AlignTop)
        
        self.pose_landmark_title_layout = QHBoxLayout()
        self.pose_landmark_title_layout.setSpacing(0)
        self.pose_landmark_title_layout.setContentsMargins(0, 0, 0, 0)
        self.pose_landmark_title_layout.setAlignment(Qt.AlignLeft)

        self.pose_landmark_title_btn = QPushButton(qta.icon('fa5s.caret-right', color='white'), 'Pose landmark detection')
        self.pose_landmark_title_btn.setObjectName("Pose landmark detection")
        self.pose_landmark_title_btn.setStyleSheet("""
            color: white;
            font-size: 15px;
            font-weight: bold;
        """)

        self.pose_landmark_title_btn.setFlat(True)
        self.pose_landmark_title_layout.addWidget(self.pose_landmark_title_btn)
        self.pose_landmark_layout.addLayout(self.pose_landmark_title_layout)

        self.pose_landmark_option_layout = QVBoxLayout()
        self.pose_landmark_option_layout.setSpacing(0)
        self.pose_landmark_option_layout.setContentsMargins(0, 0, 0, 0)
        self.pose_landmark_option_layout.setAlignment(Qt.AlignLeft)

        self.pose_landmark_option_btn1 = CustomOptionButton("SSD")
        self.pose_landmark_option_btn2 = CustomOptionButton("SSD")
        self.pose_landmark_option_btn3 = CustomOptionButton("SSD")
        self.pose_landmark_option_btn4 = CustomOptionButton("SSD")
        self.pose_landmark_option_btn5 = CustomOptionButton("SSD")

        self.pose_landmark_option_layout.addWidget(self.pose_landmark_option_btn1)
        self.pose_landmark_option_layout.addWidget(self.pose_landmark_option_btn2)
        self.pose_landmark_option_layout.addWidget(self.pose_landmark_option_btn3)
        self.pose_landmark_option_layout.addWidget(self.pose_landmark_option_btn4)
        self.pose_landmark_option_layout.addWidget(self.pose_landmark_option_btn5)
        self.pose_landmark_layout.addLayout(self.pose_landmark_option_layout)

        # add to scroll layout
        self.option_layout.addLayout(self.obj_detect_layout)
        self.option_layout.addLayout(self.semantic_seg_layout)
        self.option_layout.addLayout(self.face_detect_layout)
        self.option_layout.addLayout(self.pose_landmark_layout)
        self.option_scroll_area.setWidget(self.widget_option)
        self.main_layout.addWidget(self.option_scroll_area)

        self.setLayout(self.main_layout)

        self.obj_detect_title_btn.clicked.connect(self.option_toggle)
        self.semantic_seg_title_btn.clicked.connect(self.option_toggle)
        self.face_detect_title_btn.clicked.connect(self.option_toggle)
        self.pose_landmark_title_btn.clicked.connect(self.option_toggle)

    def option_toggle(self) -> None:
        if self.sender().objectName() == "Object detection":
            if self.obj_detect_title_btn_clicked:
                self.obj_detect_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.obj_detect_option_layout.count()):
                    self.obj_detect_option_layout.itemAt(i).widget().hide()
            else:
                self.obj_detect_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.obj_detect_option_layout.count()):
                    self.obj_detect_option_layout.itemAt(i).widget().show() 
            self.obj_detect_title_btn_clicked = not self.obj_detect_title_btn_clicked

        elif self.sender().objectName() == "Semantic segmentation":
            if self.semantic_seg_title_btn_clicked:
                self.semantic_seg_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.semantic_seg_option_layout.count()):
                    self.semantic_seg_option_layout.itemAt(i).widget().hide()
            else:
                self.semantic_seg_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.semantic_seg_option_layout.count()):
                    self.semantic_seg_option_layout.itemAt(i).widget().show() 
            self.semantic_seg_title_btn_clicked = not self.semantic_seg_title_btn_clicked

        elif self.sender().objectName() == "Face detection":
            if self.face_detect_title_btn_clicked:
                self.face_detect_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.face_detect_option_layout.count()):
                    self.face_detect_option_layout.itemAt(i).widget().hide()
            else:
                self.face_detect_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.face_detect_option_layout.count()):
                    self.face_detect_option_layout.itemAt(i).widget().show()
            self.face_detect_title_btn_clicked = not self.face_detect_title_btn_clicked

        elif self.sender().objectName() == "Pose landmark detection":
            if self.pose_landmark_title_btn_clicked:
                self.pose_landmark_title_btn.setIcon(qta.icon('fa5s.caret-right', color='white'))
                for i in range(self.pose_landmark_option_layout.count()):
                    self.pose_landmark_option_layout.itemAt(i).widget().hide()
            else:
                self.pose_landmark_title_btn.setIcon(qta.icon('fa5s.caret-down', color='white'))
                for i in range(self.pose_landmark_option_layout.count()):
                    self.pose_landmark_option_layout.itemAt(i).widget().show()
            self.pose_landmark_title_btn_clicked = not self.pose_landmark_title_btn_clicked


class CustomOptionButton(QPushButton):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.setText(name)
        self.setObjectName(name)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
                border: 1px solid transparent;
                margin-left: 30px;
            }
            QPushButton:hover {
                border-color: red;
            }
        """)

        self.clicked.connect(self.select_option)

    def select_option(self) -> None:
        pass
