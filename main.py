import os
import qdarktheme
from pykinect_recorder.main_window import MainWindow
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
 

if __name__ == "__main__":
    app = QApplication()
    qdarktheme.setup_theme()
    tray_icon = QSystemTrayIcon(QIcon(os.path.abspath("./renderer/public/kinect-sensor.ico")))
    tray_icon.setToolTip("")
    main_window = MainWindow()
    main_window.show()
    app.exec()