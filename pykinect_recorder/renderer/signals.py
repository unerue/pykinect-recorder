from PySide6.QtCore import Signal, QObject
from PySide6.QtGui import QImage


class OptionSignals(QObject):
    # Sidebar stacked widget signals
    stacked_sidebar_status = Signal(str)
    camera_connect_status = Signal(bool)

    # Sidebar button signals
    sidebar_toggle = Signal(bool)
    camera_option = Signal(dict)
    device_option = Signal(str)
    color_option = Signal(str)

    device_serial_number = Signal(str)
    save_filepath = Signal(str)
    clear_frame = Signal(bool)


class RecorderSignals(QObject):
    rgb_image = Signal(QImage)
    depth_image = Signal(QImage)
    ir_image = Signal(QImage)
    record_time = Signal(float)
    video_fps = Signal(int)
    imu_acc_data = Signal(list)
    imu_gyro_data = Signal(list)
    audio_data = Signal(list)
    is_sidebar_enable = Signal(bool)


class PlaybackSignals(QObject):
    rgb_image = Signal(QImage)
    depth_image = Signal(QImage)
    ir_image = Signal(QImage)
    record_time = Signal(float)
    video_fps = Signal(int)
    imu_acc_data = Signal(list)
    imu_gyro_data = Signal(list)

    playback_filepath = Signal(str)
    time_control = Signal(int)
    time_value = Signal(int)
    
    # Video clipping signals
    clip_option = Signal(str)
    video_total_frame = Signal(int)
    current_frame_cnt = Signal(int)


class AllSignals(QObject):
    """
    This class manages all signals used throughout this project
    """
    window_control = Signal(str)
    option_signals = OptionSignals()
    record_signals = RecorderSignals()
    playback_signals = PlaybackSignals()


all_signals = AllSignals()
