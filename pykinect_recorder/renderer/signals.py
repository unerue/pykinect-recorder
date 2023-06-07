from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage

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
    time_control = Signal(int)
    time_value = Signal(int)

    # config Signals
    config_viewer = Signal(dict)

    def __init__(self):
        super().__init__()
        pass
        

all_signals = AllSignals()