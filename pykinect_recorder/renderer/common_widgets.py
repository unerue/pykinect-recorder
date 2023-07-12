import os
from typing import Tuple, Union, List

from PySide6.QtCore import Qt, QPoint, QRect, QSize, QTimer
from PySide6.QtGui import QFont, QPen, QPainter, QFontMetrics, QColor
from PySide6.QtWidgets import (
    QLabel, QComboBox, QPushButton, QSlider, QFrame, QDialog,
    QVBoxLayout, QHBoxLayout, QSizePolicy, QProgressBar, QLineEdit
)

from .signals import all_signals

"""
In script file, There are many custom widgets to use frequently in this project.

Using custom widget can manage QWidget module more efficient.
"""


class ComboBox(QComboBox):
    def __init__(self, items: List[str], current_index: int, stylesheet: Union[str, os.PathLike] = None) -> None:
        super().__init__()
        self.addItems(items)
        self.setCurrentIndex(current_index)


class PushButton(QPushButton):
    def __init__(
        self, text: str = "", font: str = "Arial", fontsize: int = 10, icon_path: str = ""
    ) -> None:
        super().__init__()
        self.setText(text)
        self.setFont(QFont(f"{font}", fontsize))
        self.setStyleSheet("""
            QPushButton {
                color: white;
            }
            QPushButton:hover {
                border-color: red;
            }
        """)


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
            horizontal_x_pos = rect.width() // 2 - font_width // 2 - 5
            horizontal_y_pos = rect.height() * 0.67
            painter.drawText(QPoint(horizontal_x_pos, horizontal_y_pos), curr_value)
        else:
            pass


class Label(QLabel):
    def __init__(
        self,
        text: str = "",
        font: str = "Arial",
        fontsize: int = 10,
        orientation=None,
        stylesheet: Union[str, os.PathLike] = None,
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
        min_size: Tuple[int, int],
        max_size: Tuple[int, int],
        layout: Union[QVBoxLayout, QHBoxLayout] = None,
    ) -> None:
        super().__init__()
        self.setMinimumSize(QSize(min_size[0], min_size[1]))
        self.setMaximumSize(QSize(max_size[0], max_size[1]))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_image = QFrame()
        self.frame_image.setObjectName("Frame_image")
        self.frame_image.setContentsMargins(0, 0, 0, 0)
        self.frame_image.setStyleSheet(""" 
            QFrame#Frame_image {
                border: 1px solid white; 
                border-radius: 0px;
            }
        """)
        self.frame_layout = QVBoxLayout(self.frame_image)
        self.frame_layout.setSpacing(0)
        self.frame_layout.setContentsMargins(0, 0, 0, 0)

        self.letter_box_frame = QFrame()
        self.letter_box_frame.setContentsMargins(0, 0, 0, 0)
        self.letter_box_frame.setStyleSheet( """ background-color: #1e1e1e; """ )

        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_name = Label(text, orientation=Qt.AlignCenter)
        self.title_name.setFixedHeight(30)
        self.title_name.setStyleSheet(
            """
            background-color: #2c2e37;
        """
        )
        self.title_layout.addWidget(self.title_name)

        if layout is None:
            self.label_image = QLabel()
            self.frame_layout.addLayout(self.title_layout)
            self.frame_layout.addWidget(self.label_image)
            self.main_layout.addWidget(self.frame_image)

            if text in ["Depth Sensor", "IR Sensor"]:
                self.letter_box_frame.setMinimumSize(min_size[0]-min_size[1]-30, min_size[1])
                self.letter_box_frame.setMaximumSize(max_size[0]-max_size[1]-30, max_size[1])
                self.main_layout.addWidget(self.letter_box_frame)
        else:
            self.frame_layout.addLayout(self.title_layout)
            self.frame_layout.addLayout(layout)
            self.main_layout.addWidget(self.frame_image)

        self.setLayout(self.main_layout)


class LineEdit(QLineEdit):
    def __init__(self, width: int = None, height: int = None, name: str = None) -> QLineEdit:
        super().__init__()
        if width:
            self.setFixedWidth(width)
        if height:
            self.setFixedHeight(height)
        if name:
            self.setObjectName(name)        
        self.editingFinished.connect(self.emit_objname)
    
    def emit_objname(self):
        all_signals.option_signals.color_option.emit(self.objectName())


class HLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(" border-color: #808080; ")
        self.setFixedHeight(1)
        self.setContentsMargins(0, 0, 0, 0)


class VLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(" border-color: #808080; ")
        self.setFixedWidth(1)
        self.setMaximumHeight(1000)
        self.setContentsMargins(0, 0, 0, 0)


class ToggleButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.bg_color = QColor(0, 188, 248)

        self.setCheckable(True)
        self.setChecked(True)
        self.setMinimumWidth(55)  # 55
        self.setMinimumHeight(22)  # 22
        self.clicked.connect(self._toggle)

    def paintEvent(self, event) -> None:
        if self.isChecked() is True:
            self.bg_color = QColor(255, 40, 40)
        else:
            self.bg_color = QColor(0, 188, 248)

        radius = 7
        width = 2 * radius + 2
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0, 0, 0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.MPenStyle)
        painter.setPen(pen)

        painter.setBrush(QColor(63, 64, 66))
        painter.drawRoundedRect(QRect(-width - 1, -radius - 1, 2 * width + 2, 2 * radius + 2), 3, 3)

        painter.setBrush(self.bg_color)
        sw_rect = QRect(-width + 2, -radius + 1, 2 * radius - 2, 2 * radius - 2)
        if not self.isChecked():
            sw_rect.moveLeft(width - radius * 2)
        painter.drawRoundedRect(sw_rect, 3, 3)

    def _toggle(self):
        self.toggle()


class CustomProgressBarDialog(QDialog):
    def __init__(self, msec: int = 1000):
        super().__init__()
        self.setFixedSize(QSize(500, 200))
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.title_label = QLabel("Extract Frames...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedSize(QSize(450, 100))
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)

        self.cnt, self.boundary = 0, msec
        self.timer = QTimer()
        self.timer.setInterval(1)
        self.timer.timeout.connect(self.set_value)
        self.timer.start()

    def set_value(self):
        if self.cnt == self.boundary:
            self.close()
        self.cnt += 1
        tmp = (self.cnt / self.boundary) * 100
        self.progress_bar.setValue(tmp)
        self.progress_bar.setFormat("%.02f %%" % tmp)
