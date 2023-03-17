from typing import Tuple
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QComboBox, QVBoxLayout, 
    QWidget, QGridLayout, QSlider, QPushButton, QFrame
)

from PySide6.QtCore import Qt, QRect


# 왜 꼭 addWidget할 때 Instance로 넘겨줘야 하는가?
class SidebarLayout(QWidget):
    # 타이틀 포함
    # 사이드바 레이아웃?
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(RgbCameraPanel())
        layout.addWidget(DepthCameraPanel())
        layout.addWidget(IRCameraPanel())
        layout.addWidget(AudioPanel())

        self.setLayout(layout)
        self.setFixedWidth(300)


class RgbCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        self.setObjectName("RgbCameraPanel")
        self.setStyleSheet("""
            QFrame#RgbCameraPanel {
                border-color: red; border-width: 2px;
            }
        """)
        layout_vbox = QVBoxLayout()
        layout_title_hbox = QHBoxLayout()
        layout_title_hbox.addWidget(QLabel("RGB Camera Option"))
        layout_title_hbox.addWidget(StateSwitchButton())
        # 세부레이아웃
        layout_grid = QGridLayout()
        
        # 해상도
        button_resolutions = QComboBox()
        button_resolutions.addItem("1280×720")
        button_resolutions.addItem("1920×1080")
        button_resolutions.addItem("2560×1440")
        button_resolutions.addItem("3840×2160")
        button_resolutions.setCurrentIndex(0)
        # combo_res.addItem("3070p")  # TODO: ten years later~ 이게 선택이되면 fps가 15로 변경되는 코드를 짜야함

        layout_grid.addWidget(QLabel("Resolution"), 0, 0,)
        layout_grid.addWidget(button_resolutions, 0, 1)

        button_rgbformat = QComboBox()
        button_rgbformat.addItem("BGRA")
        button_rgbformat.addItem("MJPG")
        button_rgbformat.addItem("NV12")
        button_rgbformat.addItem("YUV2")
        button_rgbformat.setCurrentIndex(0)

        layout_grid.addWidget(QLabel("Color Format"), 1, 0)
        layout_grid.addWidget(button_rgbformat, 1, 1)

        button_fps = QComboBox()
        button_fps.addItem("5")
        button_fps.addItem("15")
        button_fps.addItem("30")
        button_fps.setCurrentIndex(2)

        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        layout_grid.addWidget(button_fps, 2, 1)

        layout_vbox.addLayout(layout_title_hbox)
        layout_vbox.addLayout(layout_grid)
        layout_vbox.addWidget(ColorControlPanel())

        self.setLayout(layout_vbox)
        
    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()


class _ColorSlider(QSlider):
    def __init__(self, orientation, set_range_values: Tuple[int], set_value: int):
        super().__init__(orientation)
        self.setRange(*set_range_values)
        self.setValue(set_value)


class ColorControlPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인 레이아웃
        layout = QGridLayout()
        # exposure_time = QSlider(Qt.Orientation.Horizontal)
        exposure_time = _ColorSlider(Qt.Orientation.Horizontal, (0, 100), 50)
        white_balance = QSlider(Qt.Orientation.Horizontal)
        brightness = QSlider(Qt.Orientation.Horizontal)
        contrast = QSlider(Qt.Orientation.Horizontal)
        saturation = QSlider(Qt.Orientation.Horizontal)
        sharpness = QSlider(Qt.Orientation.Horizontal)
        gain = QSlider(Qt.Orientation.Horizontal)
        backlight = QPushButton() # TODO Checkbox로 바꾸기
        backlight.setCheckable(True)
        # power_freq = 

        layout.addWidget(QLabel("Exposure Time"), 0, 0)
        layout.addWidget(exposure_time, 0, 1)
        layout.addWidget(QLabel("White Balance"), 1, 0)
        layout.addWidget(white_balance, 1, 1)
        layout.addWidget(QLabel("Brightness"), 2, 0)
        layout.addWidget(brightness, 2, 1)
        layout.addWidget(QLabel("Contrast"), 3, 0)
        layout.addWidget(contrast, 3, 1)
        layout.addWidget(QLabel("Saturation"), 4, 0)
        layout.addWidget(saturation, 4, 1)
        layout.addWidget(QLabel("Sharpness"), 5, 0)
        layout.addWidget(sharpness, 5, 1)
        layout.addWidget(QLabel("Gain"), 6, 0)
        layout.addWidget(gain, 6, 1)
        layout.addWidget(QLabel("Backlight comp"), 7, 0)
        layout.addWidget(backlight, 7, 1)
        # layout.addWidget(QLabel("Power Freq"), 8, 0)
        # layout.addWidget(power_freq, 8, 1)
        
        self.setLayout(layout)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()    


class DepthCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        self.setObjectName("DepthCameraPanel")
        self.setStyleSheet("""
            QFrame#DepthCameraPanel {border-color: yellow; border-width: 2px;}
        """)
        layout_grid = QGridLayout()
        layout_grid.addWidget(QLabel("Depth Camera Option"), 0, 0)
        layout_grid.addWidget(StateSwitchButton(), 0, 1)

        button_depth = QComboBox()
        button_depth.addItem("NFOV_Binned")
        button_depth.addItem("NFOV_Unbinned")
        button_depth.addItem("WFOV_Binned")
        button_depth.addItem("WFOV_UnBinned")
        button_depth.addItem("PASSIVE_IR")
        button_depth.setCurrentIndex(1)

        layout_grid.addWidget(QLabel("Depth mode"), 1, 0)
        layout_grid.addWidget(button_depth, 1, 1)

        button_fps = QComboBox()
        button_fps.addItem("5")
        button_fps.addItem("15")
        button_fps.addItem("30")
        button_fps.setCurrentIndex(2)
        # button_fps.setDisabled(True)

        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        layout_grid.addWidget(button_fps, 2, 1)

        self.setLayout(layout_grid)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()


class IRCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("IRCameraPanel")
        self.setStyleSheet("""
            QFrame#IRCameraPanel {border-color: white; border-width: 2px;}
        """)

        layout_vbox = QVBoxLayout()
        layout_title_hbox = QHBoxLayout()
        layout_title_hbox.addWidget(QLabel("IR Camera Option"))
        layout_title_hbox.addWidget(StateSwitchButton())
        layout_vbox.addLayout(layout_title_hbox)

        self.setLayout(layout_vbox)



class AudioPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AudioPanel")
        self.setStyleSheet("""
            QFrame#AudioPanel {border-color: green; border-width: 2px;}
        """)

        layout_vbox = QGridLayout()
        layout_vbox.addWidget(QLabel("Audio Option"), 0, 0, 1, 2)

        button_samplerate = QComboBox()
        button_samplerate.addItem("22050")
        button_samplerate.addItem("44100")
        button_samplerate.setCurrentIndex(1)

        button_audiochannel = QComboBox()
        button_audiochannel.addItem("1")
        button_audiochannel.addItem("2")
        button_audiochannel.addItem("3")
        button_audiochannel.addItem("4")
        button_audiochannel.addItem("5")
        button_audiochannel.addItem("6")
        button_audiochannel.addItem("7")
        button_audiochannel.setCurrentIndex(0)

        button_audiosubtype = QComboBox()
        button_audiosubtype.addItem("PCM_S8")
        button_audiosubtype.addItem("PCM_16")
        button_audiosubtype.addItem("PCM_24")
        button_audiosubtype.setCurrentIndex(2)

        layout_vbox.addWidget(QLabel("Samplerate"), 1, 0)
        layout_vbox.addWidget(button_samplerate, 1, 1)
        layout_vbox.addWidget(QLabel("Audio Channels"), 2, 0)
        layout_vbox.addWidget(button_audiochannel, 2, 1)
        layout_vbox.addWidget(QLabel("Subtype"), 3, 0)
        layout_vbox.addWidget(button_audiosubtype, 3, 1)

        self.setLayout(layout_vbox)


class MotionModule(QWidget):
    """TODO: ten years later~~~"""


class StateSwitchButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.label = "OFF"
        self.bg_color = Qt.red

        self.setCheckable(True)
        self.setMinimumWidth(55)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        self.label = "ON" if self.isChecked() else "OFF"
        self.bg_color = Qt.green if self.isChecked() else Qt.red

        radius, width = 8, 35
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0,0,0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(self.bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, self.label)
