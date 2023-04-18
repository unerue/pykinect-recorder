from PySide6.QtCore import Slot
from PySide6.QtWidgets import (
    QFrame
)

class Asidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: black;
        """)
        self.setFixedSize(320, 1000)