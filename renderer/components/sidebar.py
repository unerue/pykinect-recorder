from PySide6.QtGui import QFont, QImage, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SidebarWidget(QWidget):
    def __init__(self):
        super().__init__()


        # option bar
        self.recordBtn = QPushButton("녹화")
        self.syncBtn = QPushButton("싱크")
        self.menuBtn = QPushButton("더보기")

        self.optionbar = QHBoxLayout()
        self.optionbar.addWidget(self.recordBtn)
        self.optionbar.addWidget(self.syncBtn)
        self.optionbar.addWidget(self.closeBtn)



class SideBarTitle(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.nameLabel = QLabel("Azure Kinect Camera DK", self)
        self.versionLabel = QLabel("USB C type", self)
        self.closeBtn = QPushButton("닫기")

        self.titlebar = QHBoxLayout()
        self.titlebar.addWidget(self.nameLabel)
        self.titlebar.addWidget(self.versionLabel)
        self.titlebar.addWidget(self.closeBtn)

        self.setLayout(self.titlebar)


class SideBarOption(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.recordBtn = QPushButton("녹화")
        self.syncBtn = QPushButton("싱크")
        self.menuBtn = QPushButton("더보기")

        self.optionbar = QHBoxLayout()
        self.optionbar.addWidget(self.recordBtn)
        self.optionbar.addWidget(self.syncBtn)
        self.optionbar.addWidget(self.menuBtn)

        self.setLayout(self.optionbar)


# class SideBar