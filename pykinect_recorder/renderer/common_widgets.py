import os
from typing import Tuple, Union, List, Any
from PySide6.QtCore import Qt, Signal, QObject, QPoint
from PySide6.QtGui import QFont, QImage, QPen, QPainter, QFontMetrics

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
        self.setStyleSheet(
            "color: white;"
        )

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
            QSlider { 
                margin: 0px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background-color: #3f4042;
                height: 12px;
                border-radius: 4px;
            }
            QSlider::groove:horizontal {
                height: 12px;
                margin: 1px;
                border-radius: 4px;
                background-color: "#3f4042"
            }
            QSlider::handle:horizontal {
                border: 10px;
                margin: 0px;
                border-radius: 3px;
                background-color: "#00bcf8";
            }
            QSlider:handle:horizontal:hover {
                background-color: "#4d96FF";
            }
            QSlider:handle:horizontal:pressed {
                background-color: "#FFFFFF";
            }
            """
        )

    def paintEvent(self, event):
        QSlider.paintEvent(self, event)

        curr_value = str(self.value())
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white))

        font_metrics = QFontMetrics(self.font())
        font_width = font_metrics.boundingRect(curr_value).width()

        rect = self.geometry()
        if self.orientation() == Qt.Horizontal:
            horizontal_x_pos = rect.width()//2 - font_width//2 - 5
            horizontal_y_pos = rect.height() * 0.7
            painter.drawText(QPoint(horizontal_x_pos, horizontal_y_pos), curr_value)
        else:
            pass


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
        self.setMaximumHeight(480)
        self.setFixedWidth(640)
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

    # playback/save_path Signals
    playback_filepath = Signal(str)
    save_filepath = Signal(str)
    is_run = Signal(bool)

    # config Signals
    config_viewer = Signal(dict)

    def __init__(self):
        super().__init__()
        pass
        

all_signals = AllSignals()
default_configs = {
    "color": {
        "color_resolution": 1,
        "color_format": 0,
        "camera_fps": 2
    },
    "color_option": {
        "K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE": 33300,
        "K4A_COLOR_CONTROL_WHITEBALANCE": 4500,
        "K4A_COLOR_CONTROL_CONTRAST": 5,
        "K4A_COLOR_CONTROL_SATURATION": 32,
        "K4A_COLOR_CONTROL_SHARPNESS": 2,
        "K4A_COLOR_CONTROL_BRIGHTNESS": 128,
        "K4A_COLOR_CONTROL_GAIN": 128,
        "K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION": 1,
        "K4A_COLOR_CONTROL_POWERLINE_FREQUENCY": 2,
    },
    "depth_mode": 2,
}