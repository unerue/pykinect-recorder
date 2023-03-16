from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)


class RecordViewLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        layout = QVBoxLayout()

        rgb_label = QLabel("RGB 영상", self)
        rgb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rgb_label.setStyleSheet(
            "background-color: black;"
        )

        depth_label = QLabel("Depth 영상", self)
        depth_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        depth_label.setStyleSheet(
            "background-color: black;"
        )

        ir_label = QLabel("IR 영상", self)
        ir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ir_label.setStyleSheet(
            "background-color: black;"
        )
        ir_label.setFixedWidth(440)

        top_layout = QHBoxLayout()
        top_layout.addWidget(rgb_label)
        top_layout.addWidget(depth_label)

        btn_layout = QHBoxLayout()
        record_btn = QPushButton("녹화")
        stop_btn = QPushButton("정지")
        btn_layout.addWidget(record_btn)
        btn_layout.addWidget(stop_btn)
        
        layout.addLayout(top_layout)
        layout.addWidget(ir_label)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)


