from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QComboBox, QVBoxLayout, 
    QWidget, QGridLayout, QSlider
)

from PySide6.QtCore import Qt, QRect


# 왜 꼭 addWidget할 때 Instance로 넘겨줘야 하는가?
class SidebarLayout(QWidget):
    # 타이틀 포함
    # 사이드바 레이아웃?
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        option_rgb = RgbCameraOption()
        option_depth = DepthCameraOptions()

        layout.addWidget(QLabel("Azure Kinect Camera DK"))
        layout.addWidget(option_rgb)
        layout.addWidget(option_depth)

        self.setLayout(layout)


class RgbCameraOption(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        layout = QVBoxLayout()

        # 세부레이아웃
        layout_res = QGridLayout()
        
        # 해상도
        combo_res = QComboBox()
        combo_res.addItem("Not use")
        combo_res.addItem("1280x720")
        combo_res.addItem("1920x1080")
        combo_res.addItem("2560x1440")
        combo_res.addItem("3840x2160")
        combo_res.addItem("x")

        layout_res.addWidget(QLabel("Resolution"), 0, 0,)
        layout_res.addWidget(combo_res, 0, 1)

        combo_format = QComboBox()
        combo_format.addItem("Not use")
        combo_format.addItem("BGRA")
        combo_format.addItem("MJPG")
        combo_format.addItem("NV12")
        combo_format.addItem("YUV2")

        layout_res.addWidget(QLabel("Color Format"), 1, 0)
        layout_res.addWidget(combo_format, 1, 1)

        combo_fps = QComboBox()
        combo_fps.addItem("Not use")
        combo_fps.addItem("5")
        combo_fps.addItem("15")
        combo_fps.addItem("30")

        layout_res.addWidget(QLabel("FPS"), 2, 0)
        layout_res.addWidget(combo_fps, 2, 1)

        control_rgb = RGBControlOption()
        layout.addWidget(QLabel("RGB Camera Options"))
        layout.addLayout(layout_res)
        layout.addWidget(control_rgb)
        self.setLayout(layout)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()


class DepthCameraOptions(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        layout = QGridLayout()
        layout.addWidget(QLabel("Depth camera options"), 0, 0, 1, 2)

        combo_depth = QComboBox()
        combo_depth.addItem("Not use")
        combo_depth.addItem("NFOV_Binned")
        combo_depth.addItem("NFOV_Unbinned")
        combo_depth.addItem("WFOV_Binned")
        combo_depth.addItem("WFOV_UnBinned")
        combo_depth.addItem("PASSIVE_IR")

        layout.addWidget(QLabel("Depth mode"), 1, 0)
        layout.addWidget(combo_depth, 1, 1)

        combo_fps = QComboBox()
        combo_fps.addItem("Not use")
        combo_fps.addItem("5")
        combo_fps.addItem("15")
        combo_fps.addItem("30")

        layout.addWidget(QLabel("FPS"), 2, 0)
        layout.addWidget(combo_fps, 2, 1)

        self.setLayout(layout)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()


class IRCameraOptions(QWidget):
    pass


class AudioOptions(QWidget):
    pass


class MotionModule(QWidget):
    """TODO: ten years later~~~"""


# class StateSwitchButton(QPushButton):
#     def __init__(self, parent = None):
#         super().__init__(parent)
#         self.label = "OFF"
#         self.bg_color = Qt.red

#         self.setCheckable(True)
#         self.setMinimumWidth(66)
#         self.setMinimumHeight(22)

#     def paintEvent(self, event):
#         if self.isChecked:
#             self.label, self.bg_color = "ON", Qt.green
#         else:
#             self.label, self.bg_color = "OFF", Qt.red

#         radius, width = 10, 32
#         center = self.rect().center()

#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#         painter.translate(center)
#         painter.setBrush(QColor(0,0,0))

#         pen = QPen(Qt.black)
#         pen.setWidth(2)
#         painter.setPen(pen)

#         painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
#         painter.setBrush(QBrush(self.bg_color))
#         sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
#         if not self.isChecked():
#             sw_rect.moveLeft(-width)
#         painter.drawRoundedRect(sw_rect, radius, radius)
#         painter.drawText(sw_rect, Qt.AlignCenter, self.label)


class RGBControlOption(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # 메인 레이아웃
        layout = QGridLayout()
        brightness = QSlider(Qt.Orientation.Horizontal)
        contrast = QSlider(Qt.Orientation.Horizontal)
        saturation = QSlider(Qt.Orientation.Horizontal)
        sharpness = QSlider(Qt.Orientation.Horizontal)
        gain = QSlider(Qt.Orientation.Horizontal)
            
        layout.addWidget(QLabel("Brightness"), 0, 0)
        layout.addWidget(brightness, 0, 1)
        layout.addWidget(QLabel("contrast"), 1, 0)
        layout.addWidget(contrast, 1, 1)
        layout.addWidget(QLabel("saturation"), 2, 0)
        layout.addWidget(saturation, 2, 1)
        layout.addWidget(QLabel("sharpness"), 3, 0)
        layout.addWidget(sharpness, 3, 1)
        layout.addWidget(QLabel("gain"), 4, 0)
        layout.addWidget(gain, 4, 1)

        self.setLayout(layout)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()    