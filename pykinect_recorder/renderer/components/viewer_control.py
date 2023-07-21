from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QStackedLayout, QFrame, QHBoxLayout, QWidget

from .viewer_sensors import SensorViewer
from .viewer_playback import PlaybackViewer
from .viewer_solution import ViewerSolution
from .viewer_zoom_sensor import ViewerZoom
from .viewer_3dsensors import Viewer3DSensors
from ..signals import all_signals


class StackedViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setMaximumHeight(2080)
        self.setMaximumWidth(2300)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QStackedLayout()
        # self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.main_viewer = SensorViewer()
        self.main_explorer = PlaybackViewer()
        self.main_solution = ViewerSolution()
        self.zoom_viewer = ViewerZoom()
        self.reconstruction_viewer = Viewer3DSensors()

        self.main_layout.addWidget(self.main_viewer)
        self.main_layout.addWidget(self.main_explorer)
        self.main_layout.addWidget(self.main_solution)
        self.main_layout.addWidget(self.zoom_viewer)
        self.main_layout.addWidget(self.reconstruction_viewer)

        self.main_layout.setCurrentIndex(0)
        self.setLayout(self.main_layout)   
        
        all_signals.option_signals.stacked_sidebar_status.connect(self.set_current_widget)
        all_signals.option_signals.viewer_dimension_status.connect(self.dimension_changed)

    @Slot(str)
    def set_current_widget(self, value):
        if value == "explorer":
            self.main_layout.setCurrentWidget(self.main_explorer)
        elif value == "solution":
            self.main_layout.setCurrentWidget(self.main_solution)
        elif value == "zoom":
            self.main_layout.setCurrentWidget(self.zoom_viewer)
        else:
            self.main_layout.setCurrentWidget(self.main_viewer)
        all_signals.option_signals.clear_frame.emit(True)

    @Slot(list)
    def dimension_changed(self, value: list):
        if value[1] == '2D':
            if value[0] == "recorder":
                self.main_layout.setCurrentWidget(self.main_viewer)
            else:
                self.main_layout.setCurrentWidget(self.main_explorer)
        else:
            self.main_layout.setCurrentWidget(self.reconstruction_viewer)
            