from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage


class AllSignals(QObject):
    """
    This class manages all signals used throughout this project
    """

    # Sidebar stacked widget signals
    stacked_sidebar_status = Signal(str)
    camera_connect_status = Signal(bool)

    # Sidebar button signals
    sidebar_toggle = Signal(bool)
    camera_option = Signal(dict)
    device_option = Signal(str)

    # Sensor viewer signals
    captured_rgb = Signal(QImage)
    captured_depth = Signal(QImage)
    captured_ir = Signal(QImage)
    captured_time = Signal(float)
    captured_acc_data = Signal(list)
    captured_gyro_data = Signal(list)
    captured_fps = Signal(float)
    captured_audio = Signal(list)

    # Playback signals
    playback_filepath = Signal(str)
    save_filepath = Signal(str)
    time_control = Signal(int)
    time_value = Signal(int)
    clear_frame = Signal(bool)

    # Video clipping signals
    clip_option = Signal(str)
    video_total_frame = Signal(int)
    current_frame_cnt = Signal(int)

    def __init__(self):
        super().__init__()
        pass


all_signals = AllSignals()
