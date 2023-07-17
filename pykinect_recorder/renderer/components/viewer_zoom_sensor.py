from PySide6.QtCore import Qt, Slot, QEvent, QMimeData, QPointF, QSize
from PySide6.QtGui import QImage, QPixmap, QDrag
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QGridLayout
from ..signals import all_signals


class ViewerZoom(QFrame):
    def __init__(self):
        super().__init__()
        self.is_zoom = False
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(QSize(920, 670))
        self.setMaximumSize(QSize(1190, 1030))
        self.setStyleSheet("background-color: #1e1e1e;")
        
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)   

        all_signals.option_signals.zoomin_component.connect(self.set_main_layout)

    def set_main_layout(self, data: list) -> None:
        if self.is_zoom is False:
            self.main_layout.addWidget(data[1])
            all_signals.option_signals.stacked_sidebar_status.emit("zoom")
            self.is_zoom = True
        else:
            all_signals.option_signals.stacked_sidebar_status.emit(data[0])
            self.is_zoom = False
        