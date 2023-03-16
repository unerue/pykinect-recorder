from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import (
    QHBoxLayout, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget,
)

from PySide6.QtCore import Qt, QRect


class SidebarLayout(QWidget):
    # 타이틀 포함
    # 사이드바 레이아웃?
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Azure Kinect Camera DK"))
        layout.addWidget(RgbCameraOption)
        # layout.addWidget(DepthCameraOptions)
        # layout.addWidget(~~~~)

        self.setLayout(layout)


class RgbCameraOption(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # 메인레이아웃
        layout = QVBoxLayout()
        
        titlelayout = QHBoxLayout()
        titlelayout.addWidget(QLabel("RGB Camera Options"))
        titlelayout.addWidget(StateSwitchButton)

        
        # 해상도레이아웃
        layout_res = QHBoxLayout()
        layout_res.addWidget(QLabel("해상도"), 0, 0)
        
        
        
        
        
        
        
        
        
        combo_box = QComboBox()

        combo_box.addItem("1280x720")
        combo_box.addItem("1920x1080")
        combo_box.addItem("2560x1440")
        combo_box.addItem("3840x2160")
        combo_box.addItem("x")
        layout_res.addWidget(combo_box)
        # 또는 그룹박스?

        self.setLayout(layout)

    def toggle_menu(self, state):
        if state:
            self.show()
        else:
            self.hide()


class DepthCameraOptions(QWidget):
    pass


class IRCameraOptions(QWidget):
    pass


class AudioOptions(QWidget):
    pass


class MotionModule(QWidget):
    """TODO: ten years later~~~"""


class StateSwitchButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.label = "OFF"
        self.bg_color = Qt.red

        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)

    def paintEvent(self, event):
        if self.isChecked:
            self.label, self.bg_color = "ON", Qt.green
        else:
            self.label, self.bg_color = "OFF", Qt.red

        radius, width = 10, 32
        center = self.rect().center()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QColor(0,0,0))

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QBrush(self.bg_color))
        sw_rect = QRect(-radius, -radius, width + radius, 2*radius)
        if not self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)
        painter.drawText(sw_rect, Qt.AlignCenter, self.label)




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