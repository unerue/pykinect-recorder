from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QRadioButton,
    QWidget,
    QGridLayout,
    QCheckBox,
    QPushButton,
    QFrame,
    QSizePolicy,
    QScrollArea,
    QDialog,
    QFileDialog,
    QLineEdit
)
from PySide6.QtCore import Qt, QSize, Slot
import qtawesome as qta

from ..signals import all_signals
from ..common_widgets import ComboBox, Slider, HLine, ToggleButton, Label, LineEdit
from ...pyk4a.k4a.configuration import Configuration
from ...pyk4a.pykinect import start_device, initialize_libraries


class ViewerSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: #252526;
            border-radius: 0px;                   
        """)
        self.setMinimumSize(QSize(200, 670))
        self.setMaximumSize(QSize(330, 1340))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.is_run = False
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setAlignment(Qt.AlignTop)

        widget_scroll = QScrollArea()
        widget_scroll.setWidgetResizable(True)
        widget_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        widget_option = QWidget()
        option_layout = QVBoxLayout(widget_option)
        option_layout.setSpacing(5)
        option_layout.setContentsMargins(0, 0, 0, 0)
        option_layout.setAlignment(Qt.AlignTop)
        
        self.btn_panel = BtnPanel()
        self.rgb_camera_panel = RgbCameraPanel()
        self.depth_camera_panel = DepthCameraPanel()
        self.ir_camera_panel = IRCameraPanel()
        self.audio_panel = AudioPanel()

        option_layout.addWidget(self.btn_panel)
        option_layout.addWidget(self.rgb_camera_panel)
        option_layout.addWidget(self.depth_camera_panel)
        option_layout.addWidget(self.ir_camera_panel)
        option_layout.addWidget(self.audio_panel)

        widget_scroll.setWidget(widget_option)
        main_layout.addWidget(widget_scroll)
        self.setLayout(main_layout)

        all_signals.option_signals.sidebar_toggle.connect(self.toggle_button)
        all_signals.record_signals.is_sidebar_enable.connect(self.enable_button)

    def toggle_button(self):
        self.rgb_camera_panel._toggle()
        self.depth_camera_panel._toggle()
        self.ir_camera_panel._toggle()

    def enable_button(self):
        if self.is_run is False:
            self.rgb_camera_panel.setDisabled(True)
            self.depth_camera_panel.setDisabled(True)
            self.ir_camera_panel.setDisabled(True)
            self.is_run = True
        else:
            self.rgb_camera_panel.setEnabled(True)
            self.depth_camera_panel.setEnabled(True)
            self.ir_camera_panel.setEnabled(True)
            self.is_run = False


class BtnPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(130)
        self.setMaximumHeight(130)
        self.setObjectName("BtnPanel")
        self.setStyleSheet("""
            QFrame#BtnPanel {
                border-color: gray; border-width: 2px; border-radius: 0px;
            }
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
       
        # toggle btn
        self.is_run = False
        self.is_device = False

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        title_layout = QHBoxLayout()
        self.btn_switch = ToggleButton()
        title_layout.addWidget(QLabel("<b>Open Device<b>"))
        title_layout.addStretch()
        title_layout.addWidget(self.btn_switch)
        main_layout.addLayout(title_layout)
        main_layout.addWidget(HLine())

        device_status_layout = QHBoxLayout()
        self.label_device = Label("Device S/N: ")
        self.label_device_sn = Label()
        self.label_device_sn.setStyleSheet(" border-color: white; border-radius: 0px; ")
        self.label_device_sn.setFixedSize(150, 20)
        device_status_layout.addWidget(self.label_device)
        device_status_layout.addStretch()
        device_status_layout.addWidget(self.label_device_sn)
        main_layout.addLayout(device_status_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(5)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)

        self.btn_finddir = self.make_icons(qta.icon("ri.search-line"), "Searching save path", scale=0.7)
        self.btn_finddir.setStyleSheet("""
            QPushButton:hover {
                border-color: white;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)
        self.btn_viewer = self.make_icons(qta.icon("fa.play"),"Streaming Button", scale=0.7)
        self.btn_viewer.setStyleSheet("""
            QPushButton:hover {
                border-color: white;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)
        self.btn_record = self.make_icons(qta.icon("mdi.record"),"Recording Button", scale=0.7)
        self.btn_record.setStyleSheet(""" 
            QPushButton {
                background-color: red; 
            }
            QPushButton:hover {
                border-color: white;
            }
            QToolTip {
                font:"Arial"; font-size: 15px; color: #ffffff; border: 1px solid #ffffff; 
            }
        """)
        self.btn_viewer.setObjectName("viewer")
        self.btn_record.setObjectName("recorder")
        self.btn_finddir.setEnabled(False)
        self.btn_viewer.setEnabled(False)
        self.btn_record.setEnabled(False)
        
        btn_layout.addWidget(self.btn_finddir)
        btn_layout.addWidget(self.btn_viewer)
        btn_layout.addWidget(self.btn_record)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)
        self.btn_switch.clicked.connect(self.toggle_button)
        self.btn_finddir.clicked.connect(self.search_file)
        self.btn_viewer.clicked.connect(self.emit_option)
        self.btn_record.clicked.connect(self.emit_option)
        all_signals.option_signals.device_serial_number.connect(self.set_device_serial_number)

    def make_icons(self, icon: qta, tooltip: str, scale: float = 0.8) -> QPushButton:
        w, h = int(35 * scale), int(35 * scale)
        btn = QPushButton(icon, "")
        btn.setFixedSize(40, 40)
        btn.setIconSize(QSize(w, h))
        btn.setToolTip(f"<b>{tooltip}<b>")
        return btn
    
    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(self, "Open Data Files", ".", QFileDialog.ShowDirsOnly)
        all_signals.option_signals.save_filepath.emit(_dirNames)
    
    def check_device(self) -> bool:
        try:
            self.config = Configuration()
            initialize_libraries()
            _device = start_device(config=self.config)
            all_signals.option_signals.device_serial_number.emit(str(_device.get_serialnum()))
            _device.close()
        except:
            modal = QDialog()
            layout_modal = QVBoxLayout()
            e_message = Label("<b>Fail to connect camera <br> Please retry connection.</b>", "Arial", 20, Qt.AlignmentFlag.AlignCenter)
            layout_modal.addWidget(e_message)
            modal.setLayout(layout_modal)
            modal.setWindowTitle("Error Message")
            modal.resize(400, 200)
            modal.exec()
            return False

    def emit_option(self):
        name = self.sender().objectName()
        if self.is_run is False:
            if name == 'viewer':
                self.btn_record.setEnabled(False)
                self.btn_viewer.setIcon(qta.icon("mdi.stop"))
            else:
                self.btn_viewer.setEnabled(False)
                self.btn_record.setIcon(qta.icon("mdi.stop"))
            self.is_run = True
        else:
            if name == 'viewer':
                self.btn_record.setEnabled(True)
                self.btn_viewer.setIcon(qta.icon("fa.play"))
            else:
                self.btn_viewer.setEnabled(True)
                self.btn_record.setIcon(qta.icon("mdi.record"))
            self.is_run = False

        all_signals.option_signals.sidebar_toggle.emit(True)
        all_signals.record_signals.is_sidebar_enable.emit(True)
        all_signals.option_signals.camera_option.emit(config_sidebar)
        all_signals.option_signals.device_option.emit(name)
    
    def toggle_button(self) -> None:
        if self.is_device is False:
            if self.check_device() is False:
                return
            else:
                self.btn_finddir.setEnabled(True)
                self.btn_viewer.setEnabled(True)
                self.btn_record.setEnabled(True)
                self.is_device = True
                self.btn_switch.toggle()
                all_signals.option_signals.sidebar_toggle.emit(True)
        else:
            self.btn_finddir.setDisabled(True)
            self.btn_viewer.setDisabled(True)
            self.btn_record.setDisabled(True)
            self.is_device = False
            self.btn_switch.toggle()
            all_signals.option_signals.sidebar_toggle.emit(True)
            all_signals.option_signals.clear_frame.emit(True)
    
    @Slot(str)
    def set_device_serial_number(self, value: str):
        self.label_device_sn.setText(value)


class RgbCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumHeight(420)
        self.setMaximumHeight(420)
        self.setObjectName("RgbCameraPanel")
        self.setStyleSheet("""
            QFrame#RgbCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 0px;
            }
        """
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # toggle btn
        self.is_change = True
        self.btn_switch = ToggleButton()
        title_layout.addWidget(QLabel("<b>RGB Camera Option<b>"))
        title_layout.addStretch()
        title_layout.addWidget(self.btn_switch)
        top_layout.addLayout(title_layout)
        top_layout.addWidget(HLine())

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Resolution"), 0, 0)
        self.btn_resolutions = ComboBox(["720p", "1080p", "1440p", "1536p", "2160p", "3072p"], 0)
        grid_layout.addWidget(self.btn_resolutions, 0, 1)
        self.btn_resolutions.currentIndexChanged.connect(self.set_config)

        grid_layout.addWidget(QLabel("Color Format"), 1, 0)
        self.btn_rgbformat = ComboBox(["MJPG", "NV12", "YUV2", "BGRA"], 3)
        grid_layout.addWidget(self.btn_rgbformat, 1, 1)
        self.btn_rgbformat.currentIndexChanged.connect(self.set_config)

        grid_layout.addWidget(QLabel("FPS"), 2, 0)
        self.btn_fps = ComboBox(["5", "15", "30"], 2)
        grid_layout.addWidget(self.btn_fps, 2, 1)
        self.btn_fps.currentIndexChanged.connect(self.set_config)

        self.control_panel = ColorControlPanel()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.control_panel)

        self.set_config()
        self.setLayout(main_layout)

        self.btn_resolutions.setDisabled(True)
        self.btn_rgbformat.setDisabled(True)
        self.btn_fps.setDisabled(True)
        self.control_panel.setDisabled(True)
        self.btn_switch.clicked.connect(self._toggle)

    def _toggle(self) -> None:
        self.btn_switch.toggle()
        if self.is_change:
            self.btn_resolutions.setDisabled(False)
            self.btn_rgbformat.setDisabled(False)
            self.btn_fps.setDisabled(False)
            self.control_panel.setDisabled(False)
            self.is_change = False
        else:
            self.btn_resolutions.setDisabled(True)
            self.btn_rgbformat.setDisabled(True)
            self.btn_fps.setDisabled(True)
            self.control_panel.setDisabled(True)
            self.is_change = True

    def set_config(self) -> None:
        color = {
            "color_resolution": self.btn_resolutions.currentIndex() + 1,
            "color_format": self.btn_rgbformat.currentIndex(),
            "camera_fps": self.btn_fps.currentIndex(),
        }
        config_sidebar["color"] = color
        all_signals.option_signals.camera_option.emit(config_sidebar)


class ColorControlPanel(QFrame):
    """
    exposure_time (int):
        - This option controls exposure time for color image.
        - The valid range is 500 to 1000000 in microseconds. The default value is 33300.
        - The exposure time cannot be larger than the equivelent FPS.
    white_balance (int):
        - This option controls white balance of the image in degrees Kelvin.
        - The valid range is 2500 to 12500. The default value is 4500.
        - The setting must be set to a value evenly divisible by 10 degrees.
    brightness (int): 
        - This option controls brightness in camera.
        - The valid range is 0 to 255. The default value is 128.
    contrast (int):
        - This option controls contrast in camera.
        - The valid range is 0 to 10. The default value is 5.
    saturation (int):
        - This option controls saturation in camera.
        - The valid range is 0 to 63. The default value is 32.
    sharpness (int):
        - This option controls sharpness in camera.
        - The valid range is 0 to 4. The default value is 2.
    gain (int):
        - This option needs for images correction.
        - It amplifies input signals more high value like (x1.2), (x1.4).
        - See more details in https://visionblog.vieworks.com/camera/faq/image-processing/what-is-gain/
    backlight compensation
        - This option controls backlight compensation in camera.
        - Value of 0 means backlight compensation is disabled. 
        - Value of 1 means backlight compensation is enabled.
    power prequency
        - This option controls power-line frequency setting in camera.
        - Value of 0 means set power-line compensation to 50Hz. 
        - Value of 1 means set power-line compensation to 60Hz.
    """
    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.grid_layout = QGridLayout()
        self.grid_layout.setAlignment(Qt.AlignLeft)
        self.grid_layout.setSpacing(4)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        self.grid_layout.addWidget(QLabel("Exposure Time"), 0, 0, 1, 2)
        self.exposure_time = Slider(Qt.Orientation.Horizontal, (500, 133330), 33300)  #TODO FPS에 맞게 조절
        self.grid_layout.addWidget(self.exposure_time, 0, 2)
        # self.edit_exposure = LineEdit(width=60, name="exposure")
        # self.grid_layout.addWidget(self.edit_exposure, 0, 3)
        self.exposure_time.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("White Balance"), 1, 0, 1, 2)
        self.white_balance = Slider(Qt.Orientation.Horizontal, (2500, 12500), 4500)
        self.grid_layout.addWidget(self.white_balance, 1, 2)
        # self.edit_white = LineEdit(width=60, name="whitebalance")
        # self.grid_layout.addWidget(self.edit_white, 1, 3)
        self.white_balance.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Brightness"), 2, 0, 1, 2)
        self.brightness = Slider(Qt.Orientation.Horizontal, (0, 255), 128)
        self.grid_layout.addWidget(self.brightness, 2, 2)
        # self.edit_brightness = LineEdit(width=60, name="brightness")
        # self.grid_layout.addWidget(self.edit_brightness, 2, 3)
        self.brightness.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Contrast"), 3, 0, 1, 2)
        self.contrast = Slider(Qt.Orientation.Horizontal, (0, 10), 5)
        self.grid_layout.addWidget(self.contrast, 3, 2)
        # self.edit_contrast = LineEdit(width=60, name="contrast")
        # self.grid_layout.addWidget(self.edit_contrast, 3, 3)
        self.contrast.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Saturation"), 4, 0, 1, 2)
        self.saturation = Slider(Qt.Orientation.Horizontal, (0, 63), 32)
        self.grid_layout.addWidget(self.saturation, 4, 2)
        # self.edit_saturation = LineEdit(width=60, name="saturation")
        # self.grid_layout.addWidget(self.edit_saturation, 4, 3)
        self.saturation.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Sharpness"), 5, 0, 1, 2)
        self.sharpness = Slider(Qt.Orientation.Horizontal, (0, 4), 2)
        self.grid_layout.addWidget(self.sharpness, 5, 2)
        # self.edit_sharpness = LineEdit(width=60, name="sharpness")
        # self.grid_layout.addWidget(self.edit_sharpness, 5, 3)
        self.sharpness.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Gain"), 6, 0, 1, 2)
        self.gain = Slider(Qt.Orientation.Horizontal, (0, 255), 128)
        self.grid_layout.addWidget(self.gain, 6, 2)
        # self.edit_gain = LineEdit(width=60, name="gain")
        # self.grid_layout.addWidget(self.edit_gain, 6, 3)
        self.gain.sliderReleased.connect(self.set_config)

        self.grid_layout.addWidget(QLabel("Backlight Compensation"), 7, 0, 1, 2)
        self.backlight = QCheckBox("")
        self.backlight.setLayoutDirection(Qt.RightToLeft)
        self.backlight.stateChanged.connect(self.set_config)
        self.grid_layout.addWidget(self.backlight, 7, 2)

        self.grid_layout.addWidget(QLabel("Power Freqency"), 8, 0, 1, 2)
        power_freq_layout = QHBoxLayout()
        power_freq_layout.setAlignment(Qt.AlignRight)
        self.power_freq1 = QRadioButton("50hz")
        self.power_freq2 = QRadioButton("60hz")
        self.power_freq2.setChecked(True)
        self.power_freq1.clicked.connect(self.set_config)
        self.power_freq2.clicked.connect(self.set_config)
        power_freq_layout.addWidget(self.power_freq1)
        power_freq_layout.addWidget(self.power_freq2)
        self.grid_layout.addLayout(power_freq_layout, 8, 2, 1, 2)

        self.set_config()
        self.setLayout(self.grid_layout)
        # all_signals.option_signals.color_option.connect(self.set_color_option)

    def set_config(self) -> None:
        color_option = {
            "K4A_COLOR_CONTROL_EXPOSURE_TIME_ABSOLUTE": self.exposure_time.value(),
            "K4A_COLOR_CONTROL_WHITEBALANCE": self.white_balance.value(),
            "K4A_COLOR_CONTROL_CONTRAST": self.contrast.value(),
            "K4A_COLOR_CONTROL_SATURATION": self.saturation.value(),
            "K4A_COLOR_CONTROL_SHARPNESS": self.sharpness.value(),
            "K4A_COLOR_CONTROL_BRIGHTNESS": self.brightness.value(),
            "K4A_COLOR_CONTROL_GAIN": self.gain.value(),
            "K4A_COLOR_CONTROL_BACKLIGHT_COMPENSATION": self.backlight.isChecked(),
            "K4A_COLOR_CONTROL_POWERLINE_FREQUENCY": "1" if self.power_freq1.isChecked() else "2",
        }
        config_sidebar["color_option"] = color_option
        all_signals.option_signals.camera_option.emit(config_sidebar)

    # def set_color_option(self, name: str) -> None:
    #     if name == "exposure": 
    #         self.exposure_time.setValue(int(self.edit_exposure.text()))
    #         self.edit_exposure.clear()
    #     elif name == "whitebalance": 
    #         self.white_balance.setValue(int(self.edit_white.text()))
    #         self.edit_white.clear()
    #     elif name == "contrast": 
    #         self.contrast.setValue(int(self.edit_contrast.text()))
    #         self.edit_contrast.clear()
    #     elif name == "saturation": 
    #         self.saturation.setValue(int(self.edit_saturation.text()))
    #         self.edit_saturation.clear()
    #     elif name == "sharpness": 
    #         self.sharpness.setValue(int(self.edit_sharpness.text()))
    #         self.edit_sharpness.clear()
    #     elif name == "brightness": 
    #         self.brightness.setValue(int(self.edit_brightness.text()))
    #         self.edit_brightness.clear()
    #     elif name == "gain": 
    #         self.gain.setValue(int(self.edit_gain.text()))
    #         self.edit_gain.clear()
    #     self.set_config()

class DepthCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("DepthCameraPanel")
        self.setMinimumHeight(90)
        self.setMaximumHeight(90)
        self.setStyleSheet(
            """
            QFrame#DepthCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 0px;
            }
        """
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.is_change = True
        self.btn_switch = ToggleButton()
        title_layout.addWidget(QLabel("<b>Depth Camera Option<b>"))
        title_layout.addStretch()
        title_layout.addWidget(self.btn_switch)
        top_layout.addLayout(title_layout)
        top_layout.addWidget(HLine())

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Depth mode"), 1, 0)
        self.btn_depth = ComboBox(["NFOV_Binned", "NFOV_Unbinned", "WFOV_Binned", "WFOV_UnBinned", "PASSIVE_IR"], 1)
        grid_layout.addWidget(self.btn_depth, 1, 1)
        self.btn_depth.currentIndexChanged.connect(self.set_config)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        self.set_config()
        self.setLayout(main_layout)

        self.btn_depth.setDisabled(True)
        self.btn_switch.clicked.connect(self._toggle)

    def _toggle(self) -> None:
        self.btn_switch.toggle()
        if self.is_change:
            self.btn_depth.setDisabled(False)
            self.is_change = False
        else:
            self.btn_depth.setDisabled(True)
            self.is_change = True

    def set_config(self) -> None:
        config_sidebar["depth_mode"] = self.btn_depth.currentIndex() + 1
        all_signals.option_signals.camera_option.emit(config_sidebar)


class IRCameraPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("IRCameraPanel")
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self.setStyleSheet(
            """
            QFrame#IRCameraPanel {
                border-color: gray; border-width: 2px; border-radius: 0px;
            }
        """
        )
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.is_change = True
        self.btn_switch = ToggleButton()
        title_layout.addWidget(QLabel("<b>IR Camera Option<b>"))
        title_layout.addStretch()
        title_layout.addWidget(self.btn_switch)
        main_layout.addLayout(title_layout)
        self.setLayout(main_layout)

        self.btn_switch.clicked.connect(self._toggle)

    def _toggle(self) -> None:
        self.btn_switch.toggle()
        if self.is_change:
            self.is_change = False
        else:
            self.is_change = True


class AudioPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("AudioPanel")
        self.setMinimumHeight(140)
        self.setMaximumHeight(140)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(
            """
            QFrame#AudioPanel {
                border-color: gray; border-width: 2px; border-radius: 0px;
            }
        """
        )

        main_layout = QVBoxLayout()
        top_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        self.is_change = True
        self.btn_switch = ToggleButton()
        self.btn_switch.setDisabled(True)
        title_layout.addWidget(QLabel("<b>Audio Option<b>"))
        title_layout.addStretch()
        title_layout.addWidget(self.btn_switch)
        top_layout.addLayout(title_layout)
        top_layout.addWidget(HLine())

        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Samplerate"), 1, 0)
        self.btn_samplerate = ComboBox(["22050", "44100"], 1)
        grid_layout.addWidget(self.btn_samplerate, 1, 1)
        self.btn_samplerate.currentIndexChanged.connect(self.set_config)

        grid_layout.addWidget(QLabel("Audio Channels"), 2, 0)
        self.btn_channel = ComboBox(["1", "2", "3", "4", "5", "6", "7"], 1)
        grid_layout.addWidget(self.btn_channel, 2, 1)
        self.btn_channel.currentIndexChanged.connect(self.set_config)

        grid_layout.addWidget(QLabel("Subtype"), 3, 0)
        self.btn_subtype = ComboBox(["PCM_S8", "PCM_16", "PCM_24"], 2)
        grid_layout.addWidget(self.btn_subtype, 3, 1)
        self.btn_subtype.currentIndexChanged.connect(self.set_config)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        self.set_config()
        self.setLayout(main_layout)

        self.btn_samplerate.setDisabled(True)
        self.btn_channel.setDisabled(True)
        self.btn_subtype.setDisabled(True)
        self.btn_switch.clicked.connect(self._toggle)

    def _toggle(self) -> None:
        self.btn_switch.toggle()
        if self.is_change:
            self.btn_samplerate.setDisabled(False)
            self.btn_channel.setDisabled(False)
            self.btn_subtype.setDisabled(False)
            self.is_change = False
        else:
            self.btn_samplerate.setDisabled(True)
            self.btn_channel.setDisabled(True)
            self.btn_subtype.setDisabled(True)
            self.is_change = True

    def set_config(self) -> None:
        audio = {
            "samplerate": self.btn_samplerate.currentText(),
            "channel": self.btn_channel.currentText(),
            "subtype": self.btn_subtype.currentText(),
        }
        config_sidebar["audio"] = audio
        all_signals.option_signals.camera_option.emit(config_sidebar)


config_sidebar = {
    "color": {"color_resolution": 1, "color_format": 0, "camera_fps": 2},
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
