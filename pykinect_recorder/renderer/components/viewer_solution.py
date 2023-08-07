from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QPointF, QSize
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QGridLayout, QLabel

from ..signals import all_signals


class ViewerSolution(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(1190, 1030))
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: #1e1e1e; border-radius: 0px;")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.label = QLabel()
        self.label.setMinimumSize(QSize(920, 660))
        self.label.setMaximumSize(QSize(1190, 1020))
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setStyleSheet("""
            background-color: #1e1e1e; 
            border-color: white;
        """)
        self.main_layout.addWidget(self.label)
        self.setLayout(self.main_layout)

        all_signals.mediapipe_signals.model_result.connect(self.set_rgb_image)

    @Slot(QImage)
    def set_rgb_image(self, image: QImage) -> None:
        w, h = self.label.width(), self.label.height()
        image = image.scaled(w-5, h-5, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(image))                                                           