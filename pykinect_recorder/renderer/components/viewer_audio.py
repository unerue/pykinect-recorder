from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis

from ..common_widgets import Label

SAMPLE_COUNT = 10000


class AudioSensor(QFrame):
    def __init__(self, min_size: tuple[int, int], max_size: tuple[int, int]) -> None:
        super().__init__()
        self.setMinimumSize(QSize(min_size[0], min_size[1]))
        self.setMaximumSize(QSize(max_size[0], max_size[1]))
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("AudioSensor")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)

        self.label_title = Label("Audio Sensor", orientation=Qt.AlignCenter)
        self.label_title.setMinimumHeight(30)
        self.label_title.setMaximumHeight(50)

        self.series = QLineSeries()
        self.chart = QChart()
        self.chart.setTheme(QChart.ChartThemeDark)
        self.chart.addSeries(self.series)
        self.axis_x = QValueAxis()
        self.axis_x.setRange(0, SAMPLE_COUNT)
        self.axis_x.setLabelFormat("%g")
        self.axis_y = QValueAxis()
        self.axis_y.setRange(-1, 1)
        self.chart.setAxisX(self.axis_x, self.series)
        self.chart.setAxisY(self.axis_y, self.series)
        self.chart.legend().hide()

        self.chart_view = QChartView(self.chart)
        self.chart_view.setContentsMargins(0, 0, 0, 0)
        self.chart_view.setMinimumSize(QSize(min_size[0], min_size[1] - 30))
        self.chart_view.setMaximumSize(QSize(max_size[0], (max_size[1] - 50)))

        self.main_layout.addWidget(self.label_title)
        self.main_layout.addWidget(self.chart_view)
        self.setLayout(self.main_layout)
