import sys
import time
from typing import Tuple, List
from PySide6.QtCore import QPointF, Slot, QThread, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, 
    QLabel, QPushButton, QWidget
)
from PySide6.QtCharts import QChart, QChartView, QSplineSeries, QValueAxis
from pykinect_recorder.main._pyk4a import pykinect as pykinect


SAMPLE_COUNT = 1000
RESOLUTION = 4


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(500, 300)
        pykinect.initialize_libraries()

        self.layout_main = QVBoxLayout()
        self.title = QLabel('Accelerometer')
        self.title.setFixedHeight(20)
        self.time = QLabel("Time (us) : --- ")
        self.time.setFixedHeight(20)
        
        self.series_x = QSplineSeries()
        self.series_x.setUseOpenGL(True)
        self.chart_x = QChart()
        self.chart_x.legend().hide()       
        self.chart_x.addSeries(self.series_x)

        self.axis_x_x = QValueAxis()
        self.axis_x_x.setRange(0, SAMPLE_COUNT)
        self.axis_x_x.setGridLineVisible(False)
        self.axis_x_x.hide()
        self.axis_x_y = QValueAxis()
        self.axis_x_y.setRange(-5, 5)
        self.axis_x_y.setGridLineVisible(False)
        self.axis_x_y.hide()
        self.chart_x.setAxisX(self.axis_x_x, self.series_x)
        self.chart_x.setAxisY(self.axis_x_y, self.series_x)
        self.chart_x_view = QChartView(self.chart_x)

        self.series_y = QSplineSeries()
        self.series_y.setUseOpenGL(True)
        self.chart_y = QChart()
        self.chart_y.legend().hide()
        self.chart_y.addSeries(self.series_y)

        self.axis_y_x = QValueAxis()
        self.axis_y_x.setRange(0, SAMPLE_COUNT)
        self.axis_y_x.setGridLineVisible(False)
        self.axis_y_x.hide()
        self.axis_y_y = QValueAxis()
        self.axis_y_y.setRange(-5, 5)
        self.axis_y_y.setGridLineVisible(False)
        self.axis_y_y.hide()
        self.chart_y.setAxisX(self.axis_y_x, self.series_y)
        self.chart_y.setAxisY(self.axis_y_y, self.series_y)
        self.chart_y_view = QChartView(self.chart_y)

        self.series_z = QSplineSeries()
        self.series_z.setUseOpenGL(True)
        self.chart_z = QChart()
        self.chart_z.legend().hide()
        self.chart_z.addSeries(self.series_z)

        self.axis_z_x = QValueAxis()
        self.axis_z_x.setRange(0, SAMPLE_COUNT)
        self.axis_z_x.setGridLineVisible(False)
        self.axis_z_x.hide()
        self.axis_z_y = QValueAxis()
        self.axis_z_y.setRange(-5, 5)
        self.axis_z_y.setGridLineVisible(False)
        self.axis_z_y.hide()
        self.chart_z.setAxisX(self.axis_z_x, self.series_z)
        self.chart_z.setAxisY(self.axis_z_y, self.series_z)
        self.chart_z_view = QChartView(self.chart_z)

        self.buffer_x = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.buffer_y = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.buffer_z = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.series_x.append(self.buffer_x)
        self.series_y.append(self.buffer_y)
        self.series_z.append(self.buffer_z)
        self.chart_x_view.setFixedHeight(80)
        self.chart_y_view.setFixedHeight(80)
        self.chart_z_view.setFixedHeight(80)

        self.th = Thread()
        self.th.time.connect(self._set_time)
        self.th.buffer_x.connect(self._change_x)
        # self.th.buffer_y.connect(self._change_y)
        # self.th.buffer_z.connect(self._change_z)

        self.is_run = True
        self.btn = QPushButton("시작")
        self.btn.clicked.connect(self.updateChart)

        self.layout_main.addWidget(self.title)
        self.layout_main.addWidget(self.time)
        self.layout_main.addWidget(self.chart_x_view)
        # self.layout_main.addWidget(self.chart_y_view)
        # self.layout_main.addWidget(self.chart_z_view)
        self.layout_main.addWidget(self.btn)

        widget_main = QWidget(self)
        widget_main.setLayout(self.layout_main)
        self.setCentralWidget(widget_main)

    def updateChart(self) -> None:
        if self.is_run:
            self.th.is_run = True
            self.th.start()
            self.btn.setText("중지")
            self.is_run = False
        else:
            self.th.is_run = False
            self.btn.setText("시작")
            self.is_run = True

    @Slot(float)
    def _set_time(self, text) -> None:
        self.time.setText(f"Time (us) : {text}")

    @Slot(float)
    def _change_x(self, buffer):
        available_samples = 500
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for s in range(start):
                self.buffer_x[s].setY(self.buffer_x[s + available_samples].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            self.buffer_x[s].setY(buffer/2)
            data_index = data_index + RESOLUTION

        self.series_x.replace(self.buffer_x)

    # @Slot(float)
    # def _change_y(self, buffer):
    #     available_samples = 500
    #     start = 0
    #     if (available_samples < SAMPLE_COUNT):
    #         start = SAMPLE_COUNT - available_samples
    #         for s in range(start):
    #             self.buffer_y[s].setY(self.buffer_y[s + available_samples].y())

    #     data_index = 0
    #     for s in range(start, SAMPLE_COUNT):
    #         self.buffer_y[s].setY(buffer/2)
    #         data_index = data_index + RESOLUTION

    #     self.series_y.replace(self.buffer_y)

    # @Slot(float)
    # def _change_z(self, buffer):
    #     available_samples = 500
    #     start = 0
    #     if (available_samples < SAMPLE_COUNT):
    #         start = SAMPLE_COUNT - available_samples
    #         for s in range(start):
    #             self.buffer_z[s].setY(self.buffer_z[s + available_samples].y())

    #     data_index = 0
    #     for s in range(start, SAMPLE_COUNT):
    #         self.buffer_z[s].setY(buffer/2)
    #         data_index = data_index + RESOLUTION

    #     self.series_z.replace(self.buffer_z)


class Thread(QThread):
    time = Signal(float)
    buffer_x = Signal(float)
    buffer_y = Signal(float)
    buffer_z = Signal(float)

    def __init__(self):
        super().__init__()
        self.device = pykinect.start_device()
        self.is_run = None

    def run(self) -> None:
        while self.is_run:
            imu_sample = self.device.update_imu()
            _time = imu_sample.acc_time
            _x, _y, _z = imu_sample.acc
            self.time.emit(_time/1e6)
            self.buffer_x.emit(_x)
            self.buffer_y.emit(_y)
            self.buffer_z.emit(_z)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec()