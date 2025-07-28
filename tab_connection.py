from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from connect_db import get_connection_value, get_device_ping_value


class PingGraphWidget(QFrame):
    def __init__(self, title, color="blue", width=300):
        super().__init__()
        self.ping_data = []
        self.max_points = 30

        self.graph = pg.PlotWidget()
        self.graph.setBackground("w")
        self.graph.setTitle(title, color="black", size="10pt")
        self.graph.showGrid(x=True, y=True)
        self.graph.setLabel('left', 'Ping (ms)')
        self.graph.setLabel('bottom', 'Time')

        pen = pg.mkPen(color=color, width=2)
        self.plot = self.graph.plot([], [], pen=pen)

        self.avg_line = pg.InfiniteLine(angle=0, pen=pg.mkPen('red', style=pg.QtCore.Qt.DashLine))
        self.graph.addItem(self.avg_line)

        self.avg_label = pg.TextItem("", anchor=(1, 1), color='red')
        self.graph.addItem(self.avg_label)

        layout = QVBoxLayout()
        layout.addWidget(self.graph)
        self.setLayout(layout)
        self.setFixedWidth(width)

    def update_ping(self, value):
        self.ping_data.append(value)
        if len(self.ping_data) > self.max_points:
            self.ping_data.pop(0)

        self.plot.setData(list(range(len(self.ping_data))), self.ping_data)

        if self.ping_data:
            avg = sum(self.ping_data) / len(self.ping_data)
            self.avg_line.setValue(avg)
            self.avg_label.setText(f"Avg: {avg:.1f} ms")
            self.avg_label.setPos(self.max_points - 1, avg)


class ConnectionTab(QWidget):
    def __init__(self):
        super().__init__()

        self.server_ping_widget = PingGraphWidget("Ping To Server", color="blue", width=550)
        self.device_ping_widget = PingGraphWidget("Ping To Device", color="green", width=550)

        layout = QVBoxLayout()
        frame_layout = QHBoxLayout()
        frame_layout.addWidget(self.server_ping_widget)
        frame_layout.addWidget(self.device_ping_widget)
        layout.addLayout(frame_layout)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_pings)
        self.timer.start(1000)

    def update_pings(self):
        server_ping = get_connection_value()
        device_ping = get_device_ping_value()

        self.server_ping_widget.update_ping(server_ping)
        self.device_ping_widget.update_ping(device_ping)
