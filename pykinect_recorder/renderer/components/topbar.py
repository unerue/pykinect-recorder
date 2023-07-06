import os
import platform

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QHBoxLayout, QFrame, QFileDialog, QPushButton
import qtawesome as qta

from ..signals import all_signals
from ..common_widgets import PushButton, Label, VLine


class Topbar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(50)
        self.setMaximumWidth(4000)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.user_name = os.getenv("USERNAME")

        # check execution environment.
        if platform.system().startswith("Windows"):
            self.base_path = os.path.join("C", "Users", self.user_name, "Videos\\")
        else:
            self.base_path = os.path.join("home", self.user_name, "Videos\\")

        self.setObjectName("Toolbar")
        self.setStyleSheet("""
            QFrame#Toolbar {
                background-color: #323233; padding: 0px; margin: 0px;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.left_layout = QHBoxLayout()
        self.left_layout.setSpacing(0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.label_device_status = Label("Azure Kinect Camera", orientation=Qt.AlignCenter)
        self.label_device_status.setFixedSize(170, 50)
        self.btn_finddir = PushButton("select save path", "Arial", 10)
        self.btn_finddir.setFixedSize(170, 50)
        self.label_dirpath = Label(f"  save path: {self.base_path}", orientation=Qt.AlignVCenter)

        self.left_layout.addWidget(self.label_device_status)
        self.left_layout.addWidget(VLine())
        self.left_layout.addWidget(self.btn_finddir)
        self.left_layout.addWidget(VLine())
        self.left_layout.addWidget(self.label_dirpath)

        self.right_btn_layout = QHBoxLayout()
        self.right_btn_layout.setSpacing(0)
        self.right_btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = self.make_icons(qta.icon("msc.chrome-minimize"), "minimize")
        self.btn_maximize = self.make_icons(qta.icon("msc.chrome-maximize"), "maximize")
        self.btn_close = self.make_icons(qta.icon("msc.chrome-close"), "close")
        self.right_btn_layout.addWidget(self.btn_minimize)
        self.right_btn_layout.addWidget(self.btn_maximize)
        self.right_btn_layout.addWidget(self.btn_close)

        main_layout.addLayout(self.left_layout)
        main_layout.addLayout(self.right_btn_layout)
        self.setLayout(main_layout)

        self.btn_finddir.clicked.connect(self.search_file)
        self.btn_minimize.clicked.connect(self.right_btn_clicked)
        self.btn_maximize.clicked.connect(self.right_btn_clicked)
        self.btn_close.clicked.connect(self.right_btn_clicked)

    def search_file(self) -> None:
        _dirNames = QFileDialog.getExistingDirectory(self, "Open Data Files", self.base_path, QFileDialog.ShowDirsOnly)
        self.label_dirpath.setText(" save path: %s"% _dirNames+"\\")
        self.base_path = _dirNames
        all_signals.option_signals.save_filepath.emit(self.base_path)
    
    def make_icons(self, icon: qta, tooltip: str, scale: float = 0.8) -> QPushButton:
        w, h = int(35 * scale), int(35 * scale)
        btn = QPushButton(icon, "")
        btn.setObjectName(tooltip)
        btn.setFixedSize(40, 40)
        btn.setIconSize(QSize(w, h))
        btn.setToolTip(f"<b>{tooltip}<b>")
        return btn
    
    def right_btn_clicked(self):
        all_signals.window_control.emit(self.sender().objectName())
