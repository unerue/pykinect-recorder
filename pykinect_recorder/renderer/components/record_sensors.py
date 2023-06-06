import cv2
import sys
import time
import queue
import sounddevice as sd
import soundfile as sf

from numpy.typing import NDArray
from typing import Optional, Tuple
from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QImage
from pykinect_recorder.main._pyk4a.k4a import Device
from PySide6.QtMultimedia import (
    QAudioFormat,
    QAudioSource,
    QMediaDevices,
)

from ..signals import all_signals


RESOLUTION = 4
q = queue.Queue()


def callback(indata, frames, time, status):
    global q
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


class RecordSensors(QThread):
    global queue

    def __init__(self, device: Device, audio_record=None, parent=None) -> None:
        QThread.__init__(self, parent)
        self.device = device
        self.is_run = None

        self.input_devices = QMediaDevices.audioInputs()
        self.audio_input = None
        self.audio_file = None
        self.audio_record = audio_record  # verb -> noun

    def run(self):
        self.readyAudio()  # snake_case
        self.io_device = self.audio_input.start()

        with sf.SoundFile(
            self.audio_file,
            mode="x",
            samplerate=44100,
            channels=2,
        ) as file:
            with sd.InputStream(samplerate=44100, device=0, channels=2, callback=callback):
                while self.is_run:
                    start_t = time.time()  # start_time
                    current_frame = self.device.update()  # current_frame
                    file.write(q.get())

                    current_rgb_frame = current_frame.get_color_image()
                    current_depth_frame = current_frame.get_depth_image()
                    current_ir_frame = current_frame.get_ir_image()
                    current_imu_data = self.device.update_imu()

                    if current_rgb_frame[0]:
                        rgb_frame = current_rgb_frame[1]
                        rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)

                        h, w, ch = rgb_frame.shape
                        rgb_frame = QImage(rgb_frame, w, h, ch * w, QImage.Format_RGB888)
                        scaled_rgb_frame = rgb_frame.scaled(640, 480, Qt.KeepAspectRatio)
                        all_signals.captured_rgb.emit(scaled_rgb_frame)

                    if current_depth_frame[0]:
                        depth_frame = self._colorize(current_depth_frame[1], (None, 5000), cv2.COLORMAP_HSV)
                        h, w, ch = depth_frame.shape

                        depth_frame = QImage(depth_frame, w, h, w * ch, QImage.Format_RGB888)
                        scaled_depth_frame = depth_frame.scaled(500, 500, Qt.KeepAspectRatio)
                        all_signals.captured_depth.emit(scaled_depth_frame)

                    if current_ir_frame[0]:
                        ir_frame = self._colorize(current_ir_frame[1], (None, 5000), cv2.COLORMAP_BONE)
                        h, w, ch = ir_frame.shape

                        ir_frame = QImage(ir_frame, w, h, w * ch, QImage.Format_RGB888)
                        scaled_ir_frame = ir_frame.scaled(500, 500, Qt.KeepAspectRatio)
                        all_signals.captured_ir.emit(scaled_ir_frame)

                    end_time = time.time()
                    acc_time = current_imu_data.acc_time
                    acc_data = current_imu_data.acc
                    gyro_data = current_imu_data.gyro

                    try:
                        fps = 1 / (end_time - start_t)
                        all_signals.captured_fps.emit(fps)
                    except:
                        pass

                    all_signals.captured_time.emit(acc_time / 1e6)
                    all_signals.captured_acc_data.emit(acc_data)
                    all_signals.captured_gyro_data.emit(gyro_data)

                    # audio
                    data = self.io_device.readAll()
                    available_samples = data.size() // RESOLUTION
                    all_signals.captured_audio.emit([data, available_samples])

        if self.audio_record is None:
            import os

            os.remove(self.audio_file)

        self.audio_input.stop()
        self.io_device = None

    def _colorize(
        self,
        image: NDArray,
        clipping_range: Tuple[Optional[int], Optional[int]] = (None, None),
        colormap: int = cv2.COLORMAP_HSV,
    ) -> NDArray:
        if clipping_range[0] or clipping_range[1]:
            img = image.clip(clipping_range[0], clipping_range[1])  # type: ignore
        else:
            img = image.copy()
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        img = cv2.applyColorMap(img, colormap)
        return img

    def readyAudio(self) -> None:
        format_audio = QAudioFormat()
        format_audio.setSampleRate(44200)
        format_audio.setChannelCount(3)
        format_audio.setSampleFormat(QAudioFormat.SampleFormat.UInt8)

        self.audio_input = QAudioSource(self.input_devices[0], format_audio, self)
