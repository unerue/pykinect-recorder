import os
from typing import Tuple, Union, List
from PySide6.QtCore import Qt, QPoint, QRect
from PySide6.QtGui import (
    QFont, QPen, QPainter, QFontMetrics, 
    QPalette, QBrush, QColor
)

from PySide6.QtWidgets import (
    QLabel, QComboBox, QPushButton, QSlider, 
    QFrame, QVBoxLayout, QHBoxLayout
)

"""
In script file, There are many custom widgets to use frequently in this project.

Using custom widget can manage QWidget module more efficient.
"""


class ComboBox(QComboBox):
    def __init__(self, items: List[str], current_index: int, stylesheet: Union[str, os.PathLike] = None) -> None:
        super().__init__()
        self.addItems(items)
        self.setCurrentIndex(current_index)

        # if stylesheet is not None:
        #     with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
        #         stylesheet = f.read()
        #         print(stylesheet)
        #     self.setStyleSheet(str(stylesheet))


class PushButton(QPushButton):
    def __init__(
        self, text: str = "", font: str = "Arial", fontsize: int = 10, stylesheet: Union[str, os.PathLike] = None
    ) -> None:
        super().__init__()
        self.setText(text)
        self.setFont(QFont(f"{font}", fontsize))
        self.setStyleSheet("color: white;")

        # if stylesheet is not None:
        #     with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
        #         stylesheet = f.read()
        #         print(stylesheet)
        #     self.setStyleSheet(str(stylesheet))


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
        layout: Union[QVBoxLayout, QHBoxLayout] = None,
    ) -> None:
        super().__init__()
        self.setMaximumHeight(480)
        self.setFixedWidth(640)
        self.setContentsMargins(0, 0, 0, 0)

        self.setObjectName("Frame")
        self.setStyleSheet(
            """QFrame#Frame {
                border-color: white;
            }"""
        )
        self.layout_main = QVBoxLayout()
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.title_layout = QHBoxLayout()
        self.title_layout.setSpacing(0)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_name = Label(text, orientation=Qt.AlignCenter)
        self.title_name.setFixedHeight(30)
        self.title_name.setStyleSheet("""
            background-color: #2c2e37;
        """)
        self.title_layout.addWidget(self.title_name)

        if layout is None:
            self.frame = QLabel()
            self.layout_main.addLayout(self.title_layout)
            self.layout_main.addWidget(self.frame)
            
        else:
            self.layout_main.addLayout(self.title_layout)
            self.layout_main.addLayout(layout)
        self.setLayout(self.layout_main)

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
        self.setMaximumHeight(600)
        self.setContentsMargins(0, 0, 0, 0)


class ToggleButton(QPushButton):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.bg_color = QColor(0, 188, 248)

        self.setCheckable(True)
        self.setMinimumWidth(55)  # 55
        self.setMinimumHeight(22)  # 22

    def paintEvent(self, event) -> None:
        self.bg_color = QColor(255, 40, 40) if self.isChecked() else QColor(0, 188, 248)

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
