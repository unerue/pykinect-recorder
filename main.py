import os
import sys
import qdarktheme
from pykinect_recorder.main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    # tray_icon = QSystemTrayIcon(QIcon("pykinect_recorder/renderer/public/kinect-sensor.ico"))
    # tray_icon.setToolTip("Pykinect Recorder")
    # tray_icon.show()

    screen_size = app.primaryScreen().size()
    width, height = screen_size.width(), screen_size.height()
    main_window = MainWindow(width, height)
    main_window.show()
    app.exec()
