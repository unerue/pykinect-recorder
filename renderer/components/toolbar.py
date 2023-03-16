from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QWidget, QStyle
)


class ToolbarLayout(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.sourceAddBtn = QPushButton("Add Source")
        self.sourceAddBtn.setFont(QFont("Arial", 15))
        self.sourceAddBtn.setFixedSize(250, 50)

        self.uploadBtn = QPushButton("업로드")
        self.uploadBtn.setFont(QFont("Arial", 10))
        self.uploadBtn.setFixedSize(70, 50)

        self.optionBtn = QPushButton("옵션")
        self.optionBtn.setFont(QFont("Arial", 10))
        self.optionBtn.setFixedSize(50, 50)
    
        sidebarlayout = QHBoxLayout()
        sidebarlayout.addWidget(self.sourceAddBtn)
        sidebarlayout.addWidget(self.uploadBtn)
        sidebarlayout.addWidget(self.optionBtn)
        sidebarlayout

        self.setLayout(sidebarlayout)


