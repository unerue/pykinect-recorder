from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QVBoxLayout, QRadioButton,
    QWidget, QGridLayout, QCheckBox, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QRect

from .custom_buttons import Label, ComboBox, Slider


class Sidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("background-color: #242c33;")
        layout_main = QVBoxLayout()
        layout_main.addWidget(RgbCameraPanel())
        layout_main.addWidget(DepthCameraPanel())
        layout_main.addWidget(IRCameraPanel())
        layout_main.addWidget(AudioPanel())
        self.vision_solution_panel = VisionSolutionPanel()
        layout_main.addWidget(self.vision_solution_panel)
        self.setLayout(layout_main)
        
        # self.setFixedHeight(1550)
        self.setMaximumHeight(1900)
        self.setFixedWidth(300)


class RgbCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        self.setObjectName("RgbCameraPanel")
        self.setStyleSheet("""
            QFrame#RgbCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 5px;
            }
        """)

        layout_main = QVBoxLayout()
        layout_title = QHBoxLayout()
        
        # toggle btn
        self.is_change = True
        self.btn_switch = ToggleButton()
        self.btn_switch.clicked.connect(self._toggle)
        self.label_switch = Label("On", "Arial", 8, Qt.AlignmentFlag.AlignCenter)
       
        layout_switch = QVBoxLayout()
        layout_switch.addWidget(self.btn_switch)
        layout_switch.addWidget(self.label_switch)
        layout_title.addWidget(QLabel("RGB Camera Option"))
        layout_title.addWidget(QLabel(""))
        layout_title.addLayout(layout_switch)
        # 세부레이아웃

        layout_grid = QGridLayout()

        layout_grid.addWidget(QLabel("Resolution"), 0, 0)
        self.btn_resolutions = ComboBox(
            ["720p", "1080p", "1440p", "2160p", "3072p"], 0
        )
        layout_grid.addWidget(self.btn_resolutions, 0, 1)

        layout_grid.addWidget(QLabel("Color Format"), 1, 0)
        self.btn_rgbformat = ComboBox(
            ["MJPG", "NV12", "YUV2", "BGRA"], 3
        )
        layout_grid.addWidget(self.btn_rgbformat, 1, 1)

        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        self.btn_fps = ComboBox(
            ["5", "15", "30"], 2
        )
        layout_grid.addWidget(self.btn_fps, 2, 1)

        self.control_panel = ColorControlPanel()
        layout_main.addLayout(layout_title)
        layout_main.addLayout(layout_grid)
        layout_main.addWidget(self.control_panel)

        self.setLayout(layout_main)
        
    def _toggle(self) -> None:
        if self.is_change:
            self.btn_resolutions.setDisabled(True)
            self.btn_rgbformat.setDisabled(True)
            self.btn_fps.setDisabled(True)
            self.control_panel.setDisabled(True)
            self.is_change = False
            self.label_switch.setText("Off")
        else:
            self.btn_resolutions.setDisabled(False)
            self.btn_rgbformat.setDisabled(False)
            self.btn_fps.setDisabled(False)
            self.control_panel.setDisabled(False)
            self.is_change = True
            self.label_switch.setText("On")
            

class ColorControlPanel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인 레이아웃
        layout = QGridLayout()

        layout.addWidget(QLabel("Exposure Time"), 0, 0)
        exposure_time = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(exposure_time, 0, 1)

        layout.addWidget(QLabel("White Balance"), 1, 0)
        white_balance = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(white_balance, 1, 1)

        layout.addWidget(QLabel("Brightness"), 2, 0)
        brightness = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(brightness, 2, 1)

        layout.addWidget(QLabel("Contrast"), 3, 0)
        contrast = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(contrast, 3, 1)

        layout.addWidget(QLabel("Saturation"), 4, 0)
        saturation = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(saturation, 4, 1)

        layout.addWidget(QLabel("Sharpness"), 5, 0)
        sharpness = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(sharpness, 5, 1)

        layout.addWidget(QLabel("Gain"), 6, 0)
        gain = Slider(Qt.Orientation.Horizontal, (0, 100), 50)
        layout.addWidget(gain, 6, 1)

        backlight = QCheckBox("Backlight compensation")
        backlight.setCheckable(True)
        layout.addWidget(backlight, 7, 0, 1, 2)

        layout.addWidget(QLabel("Power Freq"), 8, 0)
        layout_power_freq = QHBoxLayout()
        self.power_freq1 = QRadioButton("50hz")
        self.power_freq2 = QRadioButton("60hz")
        layout_power_freq.addWidget(self.power_freq1)
        layout_power_freq.addWidget(self.power_freq2)
        layout.addLayout(layout_power_freq, 8, 1)

        self.setLayout(layout)
        
        
class DepthCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        self.setObjectName("DepthCameraPanel")
        self.setStyleSheet("""
            QFrame#DepthCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 5px;
            }
        """)

        layout_grid = QGridLayout()
        layout_title = QHBoxLayout()
        self.is_change = True

        layout_grid.addWidget(QLabel("Depth Camera Option"), 0, 0)
        self.btn_switch = ToggleButton()
        self.btn_switch.clicked.connect(self._toggle)
        self.label_switch = Label("On", "Arial", 8, Qt.AlignmentFlag.AlignCenter)
        layout_switch = QVBoxLayout()
        layout_switch.addWidget(self.btn_switch)
        layout_switch.addWidget(self.label_switch)
        layout_title.addWidget(QLabel(""))
        layout_title.addLayout(layout_switch)
        layout_grid.addLayout(layout_title, 0, 1)

        layout_grid.addWidget(QLabel("Depth mode"), 1, 0)
        self.btn_depth = ComboBox(
            ["NFOV_Binned", "NFOV_Unbinned", "WFOV_Binned", "WFOV_UnBinned", "PASSIVE_IR"], 1
        )
        layout_grid.addWidget(self.btn_depth, 1, 1)

        layout_grid.addWidget(QLabel("FPS"), 2, 0)
        self.btn_fps = ComboBox(
            ["5", "15", "30"], 2
        )
        layout_grid.addWidget(self.btn_fps, 2, 1)

        self.setLayout(layout_grid)

    def _toggle(self) -> None:
        if self.is_change:
            self.btn_depth.setDisabled(True)
            self.btn_fps.setDisabled(True)
            self.is_change = False
            self.label_switch.setText("Off")
        else:
            self.btn_depth.setDisabled(False)
            self.btn_fps.setDisabled(False)
            self.is_change = True
            self.label_switch.setText("On")


class IRCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("IRCameraPanel")
        self.setStyleSheet("""
            QFrame#IRCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 5px;
            }
        """)

        layout_grid = QGridLayout()
        layout_title = QHBoxLayout()
        self.is_change = True

        layout_grid.addWidget(QLabel("Depth Camera Option"), 0, 0)
        self.btn_switch = ToggleButton()
        self.btn_switch.clicked.connect(self._toggle)
        self.label_switch = Label("On", "Arial", 8, Qt.AlignmentFlag.AlignCenter)
        layout_switch = QVBoxLayout()
        layout_switch.addWidget(self.btn_switch)
        layout_switch.addWidget(self.label_switch)
        layout_title.addWidget(QLabel(""))
        layout_title.addLayout(layout_switch)
        layout_grid.addLayout(layout_title, 0, 1)       

        self.setLayout(layout_grid)

    def _toggle(self) -> None:
        if self.is_change:
            self.label_switch.setText("Off")
            self.is_change = False
        else:
            self.label_switch.setText("On")
            self.is_change = True


class AudioPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AudioPanel")
        self.setStyleSheet("""
            QFrame#AudioPanel {
                border-color: gray; border-width: 2px; border-radius: 5px;
            }
        """)
        
        layout_grid = QGridLayout()
        layout_title = QHBoxLayout()
        self.is_change = True

        layout_grid.addWidget(QLabel("Depth Camera Option"), 0, 0)
        self.btn_switch = ToggleButton()
        self.btn_switch.clicked.connect(self._toggle)
        self.label_switch = Label("On", "Arial", 8, Qt.AlignmentFlag.AlignCenter)
        layout_switch = QVBoxLayout()
        layout_switch.addWidget(self.btn_switch)
        layout_switch.addWidget(self.label_switch)
        layout_title.addWidget(QLabel(""))
        layout_title.addLayout(layout_switch)
        layout_grid.addLayout(layout_title, 0, 1) 
        
        layout_grid.addWidget(QLabel("Samplerate"), 1, 0)
        self.btn_samplerate = ComboBox(
            ["22050", "44100"], 1
        )
        layout_grid.addWidget(self.btn_samplerate, 1, 1)

        layout_grid.addWidget(QLabel("Audio Channels"), 2, 0)
        self.btn_channel = ComboBox(
            ["1", "2", "3", "4", "5", "6", "7"], 1
        ) 
        layout_grid.addWidget(self.btn_channel, 2, 1)

        layout_grid.addWidget(QLabel("Subtype"), 3, 0)
        self.btn_subtype = ComboBox(
            ["PCM_S8", "PCM_16", "PCM_24"], 2
        )
        layout_grid.addWidget(self.btn_subtype, 3, 1)

        self.setLayout(layout_grid)
        
    def _toggle(self) -> None:
        if self.is_change:
            self.btn_samplerate.setDisabled(True)
            self.btn_channel.setDisabled(True)
            self.btn_subtype.setDisabled(True)
            self.label_switch.setText("Off")
            self.is_change = False
        else:
            self.btn_samplerate.setDisabled(False)
            self.btn_channel.setDisabled(False)
            self.btn_subtype.setDisabled(False)
            self.label_switch.setText("On")
            self.is_change = True


class VisionSolutionPanel(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("VisionSolutionPanel")
        self.setStyleSheet("""
            QFrame#VisionSolutionPanel {
                border-color: green; border-width: 2px; border-radius: 5px;
            }
        """)
        layout_vbox = QGridLayout()
        layout_vbox.addWidget(QLabel("Vision Solutions"), 0, 0, 1, 2)
        self.setLayout(layout_vbox)
        
        self.is_hide = True
        self.hide()

    def hide_panel(self) -> None:
        if self.is_hide:
            self.show()
            self.is_hide = False
        else:
            self.hide()
            self.is_hide = True


class ToggleButton(QPushButton):
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.bg_color = QColor(0, 188, 248)

        self.setCheckable(True)
        self.setMinimumWidth(55)  # 55
        self.setMinimumHeight(22)  # 22

    def paintEvent(self, event) -> None:
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

        painter.setBrush(QColor(63, 64,66))
        painter.drawRoundedRect(QRect(-width-1, -radius-1, 2*width+2, 2*radius+2), 3, 3)
        
        painter.setBrush(self.bg_color)
        sw_rect = QRect(-width+2, -radius+1, 2*radius-2, 2*radius-2)
        if not self.isChecked():
            sw_rect.moveLeft(width-radius*2)
        painter.drawRoundedRect(sw_rect, 3, 3)
