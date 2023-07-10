import os
import sys
import ctypes
import datetime
from pathlib import Path

from . import _k4a
from .capture import Capture
from .imu_sample import ImuSample
from .calibration import Calibration
from .configuration import Configuration
from ..k4arecord.record import Record
from ..k4a._k4atypes import K4A_WAIT_INFINITE
from ..k4arecord._k4arecord import k4a_playback_get_next_capture, K4A_STREAM_RESULT_EOF


class Device:
    calibration = None
    capture = None
    imu_sample = None
    filename_video = None

    def __init__(self, index: int = 0) -> None:
        self._handle = None
        self._handle = self.open(index)
        self.recording = False
        self.record = False
        self.is_imu = True

    def __del__(self) -> None:
        self.close()

    def is_valid(self) -> None:
        return self._handle

    def is_capture_initialized(self) -> None:
        return Device.capture

    def is_imu_sample_initialized(self) -> None:
        return Device.imu_sample

    def handle(self) -> None:
        return self._handle

    def start(self, configuration: Configuration, record=False, record_filepath="output.mkv") -> None:
        self.configuration = configuration
        self.start_cameras(configuration)
        self.start_imu()

        if record:
            self.record = Record(self._handle, self.configuration.handle(), record_filepath)
            self.record.add_imu_track()
            self.recording = True

    def close(self) -> None:
        if self.is_valid():
            self.stop_cameras()
            self.stop_imu()
            _k4a.k4a_device_close(self._handle)

            # Clear members
            self._handle = None
            self.record = None
            self.recording = False

    def update(self, timeout_in_ms: int = K4A_WAIT_INFINITE) -> Capture:
        # Get cameras capture
        capture_handle = self.get_capture(timeout_in_ms)

        if self.is_capture_initialized():
            Device.capture._handle = capture_handle
        else:
            Device.capture = Capture(capture_handle, Device.calibration)

        # Write capture if recording
        if self.recording:
            self.record.write_capture(Device.capture.handle())

        return Device.capture

    def update_imu(self, timeout_in_ms: int = K4A_WAIT_INFINITE) -> ImuSample:
        # Get imu sample
        imu_sample = self.get_imu_sample(timeout_in_ms)

        if self.is_imu_sample_initialized():
            Device.imu_sample._struct = imu_sample
            Device.imu_sample.parse_data()
        else:
            Device.imu_sample = ImuSample(imu_sample)

        if self.recording:
            self.record.write_imu(imu_sample)

        return Device.imu_sample

    def get_capture(self, timeout_in_ms: int = K4A_WAIT_INFINITE) -> _k4a.ctypes.POINTER:
        # Release current handle
        if self.is_capture_initialized():
            Device.capture.release_handle()

        capture_handle = _k4a.k4a_capture_t()
        _k4a.VERIFY(
            _k4a.k4a_device_get_capture(self._handle, capture_handle, timeout_in_ms),
            "Get capture failed!",
        )

        return capture_handle

    def get_imu_sample(self, timeout_in_ms: int = K4A_WAIT_INFINITE) -> _k4a.k4a_imu_sample_t:
        imu_sample = _k4a.k4a_imu_sample_t()

        _k4a.VERIFY(
            _k4a.k4a_device_get_imu_sample(self._handle, imu_sample, timeout_in_ms),
            "Get IMU failed!",
        )

        return imu_sample

    def start_cameras(self, device_config: Configuration) -> None:
        Device.calibration = self.get_calibration(device_config.depth_mode, device_config.color_resolution)

        _k4a.VERIFY(
            _k4a.k4a_device_start_cameras(self._handle, device_config.handle()),
            "Start K4A cameras failed!",
        )

    def stop_cameras(self) -> None:
        _k4a.k4a_device_stop_cameras(self._handle)

    def start_imu(self) -> None:
        _k4a.VERIFY(_k4a.k4a_device_start_imu(self._handle), "Start K4A IMU failed!")

    def stop_imu(self) -> None:
        _k4a.k4a_device_stop_imu(self._handle)

    # get device serial number
    def get_serialnum(self) -> ctypes.c_int:
        serial_number_size = ctypes.c_size_t()
        result = _k4a.k4a_device_get_serialnum(self._handle, None, serial_number_size)

        if result == _k4a.K4A_BUFFER_RESULT_TOO_SMALL:
            serial_number = ctypes.create_string_buffer(serial_number_size.value)

        _k4a.VERIFY(
            _k4a.k4a_device_get_serialnum(self._handle, serial_number, serial_number_size),
            "Read serial number failed!",
        )

        return serial_number.value.decode("utf-8")

    # ctypes.c_int => Configuration에 있는 Enum type
    def get_calibration(self, depth_mode: ctypes.c_int, color_resolution: ctypes.c_int) -> Calibration:
        calibration_handle = _k4a.k4a_calibration_t()

        _k4a.VERIFY(
            _k4a.k4a_device_get_calibration(self._handle, depth_mode, color_resolution, calibration_handle),
            "Get calibration failed!",
        )

        return Calibration(calibration_handle)

    def get_version(self):
        version = _k4a.k4a_hardware_version_t()

        _k4a.VERIFY(_k4a.k4a_device_get_version(self._handle, version), "Get version failed!")

        return version

    @staticmethod
    def open(index=0):
        device_handle = _k4a.k4a_device_t()

        _k4a.VERIFY(_k4a.k4a_device_open(index, device_handle), "Open K4A Device failed!")

        return device_handle

    @staticmethod
    def device_get_installed_count():
        return int(_k4a.k4a_device_get_installed_count())

    def get_playback_capture(self, playback_handle):
        capture_handle = _k4a.k4a_capture_t()
        ret = k4a_playback_get_next_capture(playback_handle, capture_handle) != K4A_STREAM_RESULT_EOF
        if ret:
            return capture_handle
        else:
            return None

    def save_frame_for_clip(self, playback_handle, playback_calibration):
        capture_handle = self.get_playback_capture(playback_handle)

        if self.is_capture_initialized():
            Device.capture.release_handle()
            Device.capture._handle = capture_handle
        else:
            Device.capture = Capture(capture_handle, playback_calibration)

        if self.recording:
            self.record.write_capture(Device.capture.handle())
            

        return Device.capture
