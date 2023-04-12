from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from ..common_widgets import Label


SAMPLE_COUNT = 10000


class AudioSensor(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedWidth(270)
        self.setStyleSheet(
            "border-color: white;"
        )
        
        self.layout_main = QVBoxLayout()
        self.title = Label("Audio Sensor", orientation=Qt.AlignmentFlag.AlignCenter)
        self.title.setFixedHeight(60)
        self.title.setStyleSheet(
            "border-color: white;"
        )

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

        self.layout_main.addWidget(self.title)
        self.layout_main.addWidget(self.chart_view)
        self.setLayout(self.layout_main)