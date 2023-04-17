from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QTabWidget, QFrame
)

class SidebarMenus(QFrame):
    ToggleSign = Signal(bool)
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(60)
        self.setStyleSheet("background-color: #2d2d2d;")
