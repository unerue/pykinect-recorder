import os
from typing import Tuple, Union
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QFont
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QComboBox, QVBoxLayout, 
    QWidget, QGridLayout, QSlider, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QRect


class SidebarLayout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(RgbCameraPanel())
        layout.addWidget(DepthCameraPanel())
        layout.addWidget(IRCameraPanel())
        layout.addWidget(AudioPanel())
        self.vision_solution_panel = VisionSolutionPanel()
        layout.addWidget(self.vision_solution_panel)

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
        
        # toggle btn
        self.state = True
        self.btn_switch = StateSwitchButton()
        self.btn_switch.clicked.connect(self.visible_option)
        self.label_switch = QLabel("On")
        self.label_switch.setFont(QFont("Arial", 7))
        self.label_switch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout_switch_vbox = QVBoxLayout()
        layout_switch_vbox.addWidget(self.btn_switch)
        layout_switch_vbox.addWidget(self.label_switch)
        layout_title_hbox.addWidget(QLabel("RGB Camera Option"))
        layout_title_hbox.addWidget(QLabel(""))
        layout_title_hbox.addLayout(layout_switch_vbox)
        # 세부레이아웃
        layout_grid = QGridLayout()
        
        # 해상도
        self.btn_resolutions = QComboBox()
        self.btn_resolutions.addItem("1280×720")
        self.btn_resolutions.addItem("1920×1080")
        self.btn_resolutions.addItem("2560×1440")
        self.btn_resolutions.addItem("3840×2160")
        self.btn_resolutions.setCurrentIndex(0)
        # combo_res.addItem("3070p")  # TODO: ten years later~ 이게 선택이되면 fps가 15로 변경되는 코드를 짜야함

        layout_grid.addWidget(QLabel("Resolution"), 0, 0)
        layout_grid.addWidget(self.btn_resolutions, 0, 1)

        self.btn_rgbformat = QComboBox()
        self.btn_rgbformat.addItem("BGRA")
        self.btn_rgbformat.addItem("MJPG")
        self.btn_rgbformat.addItem("NV12")
        self.btn_rgbformat.addItem("YUV2")
        self.btn_rgbformat.setCurrentIndex(0)

        layout_grid.addWidget(QLabel("Color Format"), 1, 0)
        layout_grid.addWidget(self.btn_rgbformat, 1, 1)

        self.btn_fps = QComboBox()
        self.btn_fps.addItem("5")
        self.btn_fps.addItem("15")
        self.btn_fps.addItem("30")
        self.btn_fps.setCurrentIndex(2)
        
        self.panel_control = ColorControlPanel()
        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        layout_grid.addWidget(self.btn_fps, 2, 1)

        layout_vbox.addLayout(layout_title_hbox)
        layout_vbox.addLayout(layout_grid)
        layout_vbox.addWidget(self.panel_control)

        self.setLayout(layout_vbox)
        
    def visible_option(self):
        if self.state:
            self.btn_resolutions.setDisabled(True)
            self.btn_rgbformat.setDisabled(True)
            self.btn_fps.setDisabled(True)
            self.panel_control.setDisabled(True)
            self.state = False
            self.label_switch.setText("Off")
        else:
            self.btn_resolutions.setDisabled(False)
            self.btn_rgbformat.setDisabled(False)
            self.btn_fps.setDisabled(False)
            self.panel_control.setDisabled(False)
            self.state = True
            self.label_switch.setText("On")
            

class _ColorSlider(QSlider):
    def __init__(self, orientation, set_range_values: Tuple[int], set_value: int, stylesheet: Union[str, os.PathLike] = None):
        super().__init__(orientation)
        self.setRange(*set_range_values)
        self.setValue(set_value)

        # TODO: 외부 함수화 또는 PySide6에서 이런 함수 있는지 찾아보셈
        if stylesheet is not None:
            with open(os.path.join(os.path.split(__file__)[0], stylesheet), "r", encoding="utf-8") as f:
                stylesheet = f.read()
                print(stylesheet)
            self.setStyleSheet(str(stylesheet))


class ColorControlPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인 레이아웃
        layout = QGridLayout()
        exposure_time = QSlider(Qt.Orientation.Horizontal)
        # TODO: stylesheet 넣어둔거 빼셈 예시를 보여드린거
        # exposure_time = _ColorSlider(Qt.Orientation.Horizontal, (0, 100), 50, "slider.stylesheet")
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
        
        
class DepthCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        self.setObjectName("DepthCameraPanel")
        self.setStyleSheet("""
            QFrame#DepthCameraPanel {border-color: yellow; border-width: 2px;}
        """)
        layout_grid = QGridLayout()
        layout_tophbox = QHBoxLayout()
        
        self.btn_switch = StateSwitchButton()
        self.btn_switch.clicked.connect(self.visible_option)
        self.label_switch = QLabel("On")
        self.label_switch.setFont(QFont("Arial", 7))
        self.label_switch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout_switch_vbox = QVBoxLayout()
        layout_switch_vbox.addWidget(self.btn_switch)
        layout_switch_vbox.addWidget(self.label_switch)
        
        layout_tophbox.addWidget(QLabel(""))
        layout_tophbox.addLayout(layout_switch_vbox)
        layout_grid.addWidget(QLabel("Depth Camera Option"), 0, 0)
        layout_grid.addLayout(layout_tophbox, 0, 1)

        self.state = True
        self.btn_depth = QComboBox()
        self.btn_depth.addItem("NFOV_Binned")
        self.btn_depth.addItem("NFOV_Unbinned")
        self.btn_depth.addItem("WFOV_Binned")
        self.btn_depth.addItem("WFOV_UnBinned")
        self.btn_depth.addItem("PASSIVE_IR")
        self.btn_depth.setCurrentIndex(1)

        layout_grid.addWidget(QLabel("Depth mode"), 1, 0)
        layout_grid.addWidget(self.btn_depth, 1, 1)

        self.btn_fps = QComboBox()
        self.btn_fps.addItem("5")
        self.btn_fps.addItem("15")
        self.btn_fps.addItem("30")
        self.btn_fps.setCurrentIndex(2)

        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        layout_grid.addWidget(self.btn_fps, 2, 1)

        self.setLayout(layout_grid)

    def visible_option(self):
        if self.state:
            self.btn_depth.setDisabled(True)
            self.btn_fps.setDisabled(True)
            self.state = False
            self.label_switch.setText("Off")
        else:
            self.btn_depth.setDisabled(False)
            self.btn_fps.setDisabled(False)
            self.state = True
            self.label_switch.setText("On")


class IRCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("IRCameraPanel")
        self.setStyleSheet("""
            QFrame#IRCameraPanel {border-color: white; border-width: 2px;}
        """)

        layout_grid = QGridLayout()
        layout_tophbox = QHBoxLayout()
        self.state = True
        
        self.btn_switch = StateSwitchButton()
        self.btn_switch.clicked.connect(self.visible_option)
        self.label_switch = QLabel("On")
        self.label_switch.setFont(QFont("Arial", 7))
        self.label_switch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout_switch_vbox = QVBoxLayout()
        layout_switch_vbox.addWidget(self.btn_switch)
        layout_switch_vbox.addWidget(self.label_switch)
        
        layout_tophbox = QHBoxLayout()
        layout_tophbox.addWidget(QLabel(""))
        layout_tophbox.addLayout(layout_switch_vbox)
        layout_grid.addWidget(QLabel("IR Camera Option"), 0, 0)
        layout_grid.addLayout(layout_tophbox, 0, 1)
        

        self.setLayout(layout_grid)

    def visible_option(self):
        if self.state:
            self.label_switch.setText("Off")
        else:
            self.label_switch.setText("On")

class AudioPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AudioPanel")
        self.setStyleSheet("""
            QFrame#AudioPanel {border-color: green; border-width: 2px;}
        """)
        
        layout_vbox = QGridLayout()
        layout_tophbox = QHBoxLayout()
        
        self.state = True
        
        self.btn_switch = StateSwitchButton()
        self.btn_switch.clicked.connect(self.visible_option)
        self.label_switch = QLabel("On")
        self.label_switch.setFont(QFont("Arial", 7))
        self.label_switch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout_switch_vbox = QVBoxLayout()
        layout_switch_vbox.addWidget(self.btn_switch)
        layout_switch_vbox.addWidget(self.label_switch)
        
        layout_tophbox = QHBoxLayout()
        layout_tophbox.addWidget(QLabel(""))
        layout_tophbox.addLayout(layout_switch_vbox)
        
        layout_vbox.addWidget(QLabel("Audio Option"), 0, 0)
        layout_vbox.addLayout(layout_tophbox, 0, 1)

        self.btn_samplerate = QComboBox()
        self.btn_samplerate.addItem("22050")
        self.btn_samplerate.addItem("44100")
        self.btn_samplerate.setCurrentIndex(1)

        self.btn_channel = QComboBox()
        self.btn_channel.addItem("1")
        self.btn_channel.addItem("2")
        self.btn_channel.addItem("3")
        self.btn_channel.addItem("4")
        self.btn_channel.addItem("5")
        self.btn_channel.addItem("6")
        self.btn_channel.addItem("7")
        self.btn_channel.setCurrentIndex(0)

        self.btn_subtype = QComboBox()
        self.btn_subtype.addItem("PCM_S8")
        self.btn_subtype.addItem("PCM_16")
        self.btn_subtype.addItem("PCM_24")
        self.btn_subtype.setCurrentIndex(2)

        layout_vbox.addWidget(QLabel("Samplerate"), 1, 0)
        layout_vbox.addWidget(self.btn_samplerate, 1, 1)
        layout_vbox.addWidget(QLabel("Audio Channels"), 2, 0)
        layout_vbox.addWidget(self.btn_channel, 2, 1)
        layout_vbox.addWidget(QLabel("Subtype"), 3, 0)
        layout_vbox.addWidget(self.btn_subtype, 3, 1)

        self.setLayout(layout_vbox)
        
    def visible_option(self):
        if self.state:
            self.btn_samplerate.setDisabled(True)
            self.btn_channel.setDisabled(True)
            self.btn_subtype.setDisabled(True)
            self.state = False
        else:
            self.btn_samplerate.setDisabled(False)
            self.btn_channel.setDisabled(False)
            self.btn_subtype.setDisabled(False)
            self.state = True



class VisionSolutionPanel(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("VisionSolutionPanel")
        self.setStyleSheet("""
            QFrame#VisionSolutionPanel {border-color: green; border-width: 2px;}
        """)
        layout_vbox = QGridLayout()
        layout_vbox.addWidget(QLabel("Vision Solutions"), 0, 0, 1, 2)
        self.setLayout(layout_vbox)
        # self.setVisible(True)
        
        self.is_hide = True
        self.hide()

    def hide_panel(self):
        if self.is_hide:
            self.show()
            self.is_hide = False
        else:
            self.hide()
            self.is_hide = True


class StateSwitchButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.bg_color = QColor(0, 188, 248)

        self.setCheckable(True)
        self.setMinimumWidth(55)  # 55
        self.setMinimumHeight(22)  # 22

    def paintEvent(self, event):
        self.bg_color = QColor(255, 40, 40) if self.isChecked() else QColor(0, 188, 248)

        radius = 7
        width = 2*radius+2
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0, 0, 0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.MPenStyle)
        painter.setPen(pen)

        painter.setBrush(QColor(20, 21, 24))
        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        
        painter.setBrush(self.bg_color)
        sw_rect = QRect(-width+2, -radius+1, 2*radius-2, 2*radius-2)
        if not self.isChecked():
            sw_rect.moveLeft(width-radius*2)
        painter.drawRoundedRect(sw_rect, radius, radius)
