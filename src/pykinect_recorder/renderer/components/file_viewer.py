from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFileDialog, QFrame, QVBoxLayout, QGridLayout, 
    QLineEdit, QScrollArea, QWidget, QHBoxLayout, 
)
from .custom_buttons import Label, PushButton


class _FileInfo(QWidget):
    def __init__(
            self,
            filename: str,
            time: str,
            storage: str    
        ) -> None:
        super().__init__()

        layout_main = QHBoxLayout()
        label_info = Label("시발", "Arial", 10, Qt.AlignmentFlag.AlignCenter)
        layout_info = QGridLayout()

        layout_info.addWidget(Label("파일 이름", "Arial", 10, Qt.AlignmentFlag.AlignCenter), 0, 0)
        layout_info.addWidget(Label(filename, "Arial", 10, Qt.AlignmentFlag.AlignCenter), 0, 1, 1, 2)
        layout_info.addWidget(Label("파일 이름", "Arial", 10, Qt.AlignmentFlag.AlignCenter), 1, 0)
        layout_info.addWidget(Label(time, "Arial", 10, Qt.AlignmentFlag.AlignCenter), 1, 1, 1, 2)
        layout_info.addWidget(Label("파일 이름", "Arial", 10, Qt.AlignmentFlag.AlignCenter), 2, 0)
        layout_info.addWidget(Label(storage, "Arial", 10, Qt.AlignmentFlag.AlignCenter), 2, 1, 1, 2)
        
        layout_main.addWidget(label_info)
        layout_main.addLayout(layout_info)

        self.setLayout(layout_main)


class FileViewer(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet("""
            background-color: black;
        """)

        layout_main = QVBoxLayout()
        layout_title = QGridLayout()
        
        self.label_name = Label("파일 경로", orientation=Qt.AlignmentFlag.AlignCenter)
        self.label_name.setFixedHeight(50)
        self.label_name.setStyleSheet("""
            border-color: white;
        """)
        self.label_filepath = Label("asdasd")
        self.label_filepath.setFixedHeight(50)
        self.label_filepath.setStyleSheet("""
            border-color: white;
        """)
        layout_title.addWidget(self.label_name, 0, 0)
        layout_title.addWidget(self.label_filepath, 0, 1)
        layout_title.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout_scroll = QScrollArea()
        self.layout_file = QVBoxLayout()
        self.layout_scroll.setLayout(self.layout_file)
        
        self.layout_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.layout_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout_main.addLayout(layout_title)
        layout_title.addWidget(self.layout_scroll)

        self.setLayout(layout_main)

    def search_file(self) -> None:

        _dirNames = QFileDialog.getExistingDirectory(
            self, 
            "Open Data Files", 
            self.filepath.text(), 
            QFileDialog.ShowDirsOnly
        )
        print(_dirNames)
        

    




