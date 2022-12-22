import argparse
import tempfile
import queue
import sys
import os
import datetime

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

from argparse import ArgumentParser
from pydub import AudioSegment
from pyk4a import Config, ImageFormat, PyK4A, PyK4ARecord
import numpy as np
import pyk4a

import os
import sys
import time

import cv2
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtGui import QAction, QImage, QKeySequence, QPixmap
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QMainWindow, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)


if not os.path.exists('./tools/pyk4a/example/outputs/'):
    os.mkdir('./tools/pyk4a/example/outputs')


def callback(indata, frames, time, status):
    global q
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


class Thread(QThread):
    updateFrame = Signal(QImage)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.trained_file = None
        self.status = True
        self.cap = True
        # self.args = args

        self.set_filename()

    def set_filename(self):
        filename = datetime.datetime.now()
        filename = filename.strftime("%Y_%m_%d_%H_%M_%S")
        base_path = 'C:\\Program Files\\Azure Kinect SDK v1.4.1\\tools\\pyk4a\\example\\outputs'
        
        self.filename_video = f'{base_path}\\{filename}.mkv'
        self.filename_audio = f'{base_path}\\{filename}.wav'
        print(filename)

    def run(self):
        global q
        # pyk4a
        config = Config(
            color_format=ImageFormat.COLOR_BGRA32, 
            depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,
            color_resolution=pyk4a.ColorResolution.RES_720P,
            synchronized_images_only=True
        )
        azure_device = PyK4A(config=config, device_id=0)
        azure_device.start()
        record = PyK4ARecord(device=azure_device, config=config, path=self.filename_video)
        record.create()

        with sf.SoundFile(
            self.filename_audio, mode='x', samplerate=44100,
            channels=2, subtype='PCM_24') as file:
            with sd.InputStream(
                samplerate=44100, device='Azure Kinect Microphone , MME',
                channels=2, callback=callback
            ):
                while self.status:
                    capture = azure_device.get_capture()
                    record.write_capture(capture)
                    file.write(q.get())

                    # print(capture.color[:, :, :3])
                    if np.any(capture.color):
                        frame = capture.color[:, :, :3].copy()
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        h, w, ch = capture.color[:, :, :3].shape
                        img = QImage(frame, w, h, ch * w, QImage.Format_RGB888)
                        scaled_img = img.scaled(640, 480, Qt.KeepAspectRatio)
                        # Emit signal
                        self.updateFrame.emit(scaled_img)
        
        record.flush()
        record.close()
        print(f"{record.captures_count} frames written.")

        src = self.filename_audio
        dst = f'{self.filename_audio[:-4]}.mp3'

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format='wav')

        os.remove(self.filename_audio)
        print('finish to save')


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Title and dimensions
        self.setWindowTitle("Patterns detection")
        self.setGeometry(0, 0, 800, 500)

        # Create a label for the display camera
        self.label = QLabel(self)
        self.label.setFixedSize(640, 480)

        # Thread in charge of updating the image
        self.th = Thread(self)
        # self.th.finished.connect(self.close)
        self.th.updateFrame.connect(self.setImage)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.button1 = QPushButton("Start")
        self.button2 = QPushButton("Stop/Close")
        self.button1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        buttons_layout.addWidget(self.button2)
        buttons_layout.addWidget(self.button1)

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(buttons_layout)
        # layout.addLayout(right_layout)

        # Central widget
        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connections
        self.button1.clicked.connect(self.start)
        self.button2.clicked.connect(self.kill_thread)
        self.button2.setEnabled(False)

    @Slot()
    def kill_thread(self):
        print("Finishing...")
        self.button2.setEnabled(False)
        self.button1.setEnabled(True)
        # cv2.destroyAllWindows()
        self.th.status = False
        # Give time for the thread to finish
        time.sleep(1)

    @Slot()
    def start(self):
        print("Starting...")
        self.button2.setEnabled(True)
        self.button1.setEnabled(False)
        self.th.set_filename()
        self.th.status = True
        self.th.start()

    @Slot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    q = queue.Queue()
    app = QApplication()
    w = Window()
    w.show()
    sys.exit(app.exec())

    # main(args)

    

    

    

    