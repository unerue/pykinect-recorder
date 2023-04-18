import os
from typing import Tuple, Union, List, Any
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QFont, QImage

from PySide6.QtWidgets import (
    QLabel, QComboBox, QPushButton, QSlider, 
    QFrame, QVBoxLayout, QHBoxLayout
)


class ComboBox(QComboBox):
    def __init__(
        self, 
        items: List[str], 
        current_index: int,
        stylesheet: Union[str, os.PathLike] = None
    ) -> None:
        super().__init__()
        self.addItems(items)
        self.setCurrentIndex(current_index)

        # TODO: 외부 함수화 또는 PySide6에서 이런 함수 있는지 찾아보셈
        if stylesheet is not None:
            with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
                stylesheet = f.read()
                print(stylesheet)
            self.setStyleSheet(str(stylesheet))


class PushButton(QPushButton):
    def __init__(
        self, 
        text: str = "",
        font: str = "Arial", 
        fontsize: int = 10, 
        stylesheet: Union[str, os.PathLike] = None
    ) -> None:
        super().__init__()
        self.setText(text)
        self.setFont(QFont(f"{font}", fontsize))

        if stylesheet is not None:
            with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
                stylesheet = f.read()
                print(stylesheet)
            self.setStyleSheet(str(stylesheet))


class Slider(QSlider):
    def __init__(
        self, 
        orientation, 
        set_range_values: Tuple[int], 
        set_value: int, 
    ) -> None:
        super().__init__(orientation)
        self.setRange(*set_range_values)
        self.setValue(set_value)

        self.setStyleSheet(
            """
            QSlider { margin: 0px; }
            QSlider::groove:horizontal {
                height: 10px;
                margin: 1px;
                background-color: "#1d2e48"
            }
            QSlider::handle:horizontal {
                border: 10px;
                margin: 0px;
                background-color: "#3d85e0";
            }
            QSlider:handle:horizontal:hover {
                background-color: "#4d96FF";
            }
            QSlider:handle:horizontal:pressed {
                background-color: "#FFFFFF";
            }
            """
        )


class Label(QLabel):
    def __init__(
        self, 
        text: str = "",
        font: str = "Arial", 
        fontsize: int = 10, 
        orientation = None,
        stylesheet: Union[str, os.PathLike] = None
    ) -> None:
        super().__init__()
        self.setText(text)
        self.setFont(QFont(f"{font}", fontsize))
        if orientation is not None:
            self.setAlignment(orientation)

        if stylesheet is not None:
            with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
                stylesheet = f.read()
                print(stylesheet)
            self.setStyleSheet(str(stylesheet))


class Frame(QFrame):
    def __init__(
        self,
        text: str,
        layout: Union[QVBoxLayout, QHBoxLayout] = None,
    ) -> None:
        super().__init__()
        self.setFixedSize(570, 460)
        self.setObjectName("Frame")
        self.setStyleSheet(
            """QFrame#Frame {
                border-color: white;
            }"""
        )
        
        if layout is None:
            self.layout_main = QVBoxLayout()
            self.frame = Label(text, orientation=Qt.AlignmentFlag.AlignCenter)
            self.layout_main.addWidget(self.frame)
            self.setLayout(self.layout_main)
        else:
            self.setLayout(layout)


class AllSignals(QObject):
    # Stacked Widget signals
    stacked_sidebar_status = Signal(str)
    stacked_status = Signal(str)

    # Thread Signals
    captured_rgb = Signal(QImage)
    captured_depth = Signal(QImage)
    captured_ir = Signal(QImage)
    captured_time = Signal(float)
    captured_acc_data = Signal(list)
    captured_gyro_data = Signal(list)
    captured_fps = Signal(float)
    captured_audio = Signal(list)

    # playback Signals
    playback_filepath = Signal(str)

    # savepath Signals
    save_filepath = Signal(str)
    
    def __init__(self):
        super().__init__()
        pass
        

all_signals = AllSignals()
