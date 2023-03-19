from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QHBoxLayout, QPushButton, QFrame
)


class ToolbarLayout(QFrame):
    def __init__(self) -> None:
        super().__init__()
        
        self.setObjectName("ToolbarLayout")
        self.setStyleSheet("""
            QFrame#ToolbarLayout {
                background-color: #3e4d59;
                padding: 0px;
                margin: 0px;
            }
        """)

        self.sourceAddBtn = QPushButton("Add Source")
        self.sourceAddBtn.setFont(QFont("Arial", 15))
        self.sourceAddBtn.setFixedWidth(300)

        self.uploadBtn = QPushButton("업로드")
        self.uploadBtn.setFont(QFont("Arial", 10))

        self.optionBtn = QPushButton("옵션")
        self.optionBtn.setFont(QFont("Arial", 10))
        self.button_ml = QPushButton("ML Solution")
        self.button_ml.setFont(QFont("Arial", 10))
        # self.hide_panel = self.findChild(QFrame, "VisionSolutionPanel")

        sidebarlayout = QHBoxLayout()
        sidebarlayout.addWidget(self.sourceAddBtn)
        sidebarlayout.addWidget(self.uploadBtn)
        sidebarlayout.addWidget(self.optionBtn)
        sidebarlayout.addWidget(self.button_ml)
        sidebarlayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(sidebarlayout)


