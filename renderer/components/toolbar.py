from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout, QFrame
)
from .custom_buttons import PushButton


class Toolbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.setObjectName("Toolbar")
        self.setStyleSheet("""
            QFrame#Toolbar {
                background-color: #3e4d59; padding: 0px; margin: 0px;
            }
        """)

        btn_option = PushButton("옵션", "Arial", 10)
        self.btn_ml = PushButton("ML Solution", "Arial", 10)
        btn_option.clicked.connect(self.option)

        layout_main = QHBoxLayout()
        layout_main.addWidget(btn_option)
        layout_main.addWidget(self.btn_ml)
        layout_main.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setLayout(layout_main)

    def option(self) -> None:
        pass
