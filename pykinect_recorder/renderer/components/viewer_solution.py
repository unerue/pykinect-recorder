from PySide6.QtWidgets import QFrame


class ViewerSolution(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1200, 1000)
        self.setStyleSheet("background-color: black;")
        pass
