from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QTabWidget
)
from .dl_sidebar import DLSidebar
from .viewer_sidebar import ViewerSidebar
from .explorer_sidebar import ExplorerSidebar

class SideBar(QTabWidget):
    ToggleSign = Signal(bool)
    def __init__(self) -> None:
        super().__init__()
        self.sidebar_viewer = ViewerSidebar()
        self.sidebar_dl = DLSidebar()
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