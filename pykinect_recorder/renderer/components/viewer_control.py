from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QStackedLayout, QFrame

from .viewer_sensors import SensorViewer
from .viewer_playback import PlaybackViewer
from .viewer_solution import ViewerSolution


class StackedViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(2080)
        self.setMaximumWidth(2300)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QStackedLayout()
        self.main_viewer = SensorViewer()
        self.main_explorer = PlaybackViewer()
        self.main_solution = ViewerSolution()

        self.main_layout.addWidget(self.main_viewer)
        self.main_layout.addWidget(self.main_explorer)
        self.main_layout.addWidget(self.main_solution)

        # 현재 index
        self.main_layout.setCurrentIndex(0)
        self.setLayout(self.main_layout)

    @Slot(str)
    def setCurrentWidget(self, value):
        if value == "explorer":
            self.main_layout.setCurrentWidget(self.main_explorer)
        elif value == "solution":
            self.main_layout.setCurrentWidget(self.main_solution)
        else:
            self.main_layout.setCurrentWidget(self.main_viewer)
