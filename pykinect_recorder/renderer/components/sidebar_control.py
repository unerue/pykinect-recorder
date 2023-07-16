from PySide6.QtCore import Slot
from PySide6.QtWidgets import QStackedLayout, QFrame

from .sidebar_solutions import SolutionSidebar
from .sidebar_record_control import ViewerSidebar
from .sidebar_explorer import ExplorerSidebar
from ..signals import all_signals


class StackedSidebar(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setMaximumWidth(330)
        self.setContentsMargins(0, 0, 0, 0)
        self.main_layout = QStackedLayout()
        self.sidebar_viewer = ViewerSidebar()
        self.sidebar_explorer = ExplorerSidebar()
        self.sidebar_solution = SolutionSidebar()

        self.main_layout.addWidget(self.sidebar_viewer)
        self.main_layout.addWidget(self.sidebar_explorer)
        self.main_layout.addWidget(self.sidebar_solution)

        self.main_layout.setCurrentIndex(0)
        self.setLayout(self.main_layout)

        all_signals.option_signals.stacked_sidebar_status.connect(self.set_current_widget)

    @Slot(str)
    def set_current_widget(self, value):
        if value == "explorer":
            self.main_layout.setCurrentWidget(self.sidebar_explorer)
        elif value == "solution":
            self.main_layout.setCurrentWidget(self.sidebar_solution)
        else:
            self.main_layout.setCurrentWidget(self.sidebar_viewer)
