
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