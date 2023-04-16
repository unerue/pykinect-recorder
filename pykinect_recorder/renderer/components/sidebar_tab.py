from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QTabWidget
)
from .sidebar_solutions import SolutionSidebar
from .sidebar_record_control import ViewerSidebar
from .sidebar_explorer import ExplorerSidebar

class Sidebar(QTabWidget):
    ToggleSign = Signal(bool)
    def __init__(self) -> None:
        super().__init__()
        self.sidebar_viewer = ViewerSidebar()
        self.sidebar_dl = SolutionSidebar()
        self.sidebar_explorer = ExplorerSidebar()
        self.addTab(self.sidebar_viewer, "Viewer")
        self.addTab(self.sidebar_dl, "Deep Learning")
        self.addTab(self.sidebar_explorer, "Explorer")
        self.setMovable(True)
        self.setFixedWidth(320)
        self.currentChanged.connect(self.tabChanged)

    def tabChanged(self, idx):
        if idx == 2:
            self.ToggleSign.emit(True)
        else:
            self.ToggleSign.emit(False)
