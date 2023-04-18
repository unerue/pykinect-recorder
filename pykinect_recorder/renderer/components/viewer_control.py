from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QImage
from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QFrame
)

from .sidebar_solutions import SolutionSidebar
from .sidebar_record_control import ViewerSidebar
from .sidebar_explorer import ExplorerSidebar
from .asidebar import Asidebar
from .viewer_sensors import SensorViewer

class StackedViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QStackedWidget()
        
        self.viewer_layout = QHBoxLayout()
        self.sidebar_viewer = ViewerSidebar()
        self.sensor_viewer = SensorViewer()
        self.viewer_layout.addWidget(self.sidebar_viewer)
        self.viewer_layout.addWidget(self.sensor_viewer)
        main_layout.addWidget(self.viewer_layout)

        self.explorer_layout = QHBoxLayout()
        self.sidebar_explorer = ExplorerSidebar()
        self.sensor_explorer = SensorViewer()
        self.asidebar = Asidebar()
        self.explorer_layout.addWidget(self.sidebar_explorer)
        self.explorer_layout.addWidget(self.sensor_explorer)
        self.explorer_layout.addWidget(self.asidebar)
        main_layout.addWidget(self.explorer_layout)

        self.solution_layout = QHBoxLayout()
        self.sidebar_solution = SolutionSidebar()
        self.sensor_solution = SensorViewer()
        self.solution_layout.addWidget(self.sidebar_solution)
        self.solution_layout.addWidget(self.sensor_solution)
              
        main_layout.addWidget(self.viewer_layout)
        main_layout.addWidget(self.explorer_layout)
        main_layout.addWidget(self.solution_layout)

        # 현재 
        main_layout.setCurrentIndex(1)




    @Slot(str)
    def setCurrentWiget(self, value):
        if value == "explorer":
            main


