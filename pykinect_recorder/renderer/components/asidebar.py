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
        self.setFixedSize(360, 1000)
        self.hide()

    @Slot(bool)
    def toggle_hide(self, value) -> None:
        if value == True:
            self.show()
        else:
            self.hide()