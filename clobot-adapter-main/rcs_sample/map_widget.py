from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint, pyqtSignal, pyqtSlot

import math

class NodeWidget(QWidget):
    # Signal emitted when a node is clicked
    nodeClicked = pyqtSignal(dict)

    def __init__(self, node_data):
        super().__init__()
        self.node_data = node_data
        self.setFixedSize(40,40)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawEllipse(0, 0, 10, 10)
        painter.drawText(0, 20, str(self.node_data['x']))
        painter.drawText(0, 30, str(self.node_data['y']))

    def mousePressEvent(self, event):
        self.nodeClicked.emit(self.node_data)

class MapWidget(QWidget):
    def __init__(self, positions, robot_pos, nearest_node):
        super().__init__()
        self.positions = positions
        self.robot_pos = robot_pos
        self.nearest_node = nearest_node
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Map Visualization')
        self.setGeometry(10, 10, 500, 400)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create node widgets
        for pos in self.positions:
            node_widget = NodeWidget(pos)
            node_widget.move(int(pos['x']*100), int(pos['y']*100))
            node_widget.nodeClicked.connect(self.on_node_clicked)
            node_widget.setParent(self)

    def on_node_clicked(self, node_data):
        print(f"Node {node_data['name']} clicked. X: {node_data['x']}, Y: {node_data['y']}")
    
    @pyqtSlot(dict, dict)
    def handle_robot_pos_changed(self, new_robot_pos, new_nearest_node):
        self.robot_pos = new_robot_pos
        self.new_nearest_node = new_nearest_node
        self.update() 

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp)
        qp.end()

    def drawMap(self, qp):
        pen = QPen(QColor(0, 0, 0), 2, Qt.SolidLine)
        qp.setPen(pen)

        for pos in self.positions:
          qp.drawPoint(int(pos['x']*100), int(pos['y']*100))

        # Drawing robot
        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(QColor(255, 0, 0))
        qp.drawEllipse(int(self.robot_pos['x']*100)-4, int(self.robot_pos['y']*100)-4, 20, 20)

        # Drawing robot direction
        theta = self.robot_pos['theta']
        arrow_length = 20

        arrow_x = arrow_length * math.cos(theta) + self.robot_pos['x']*100
        arrow_y = arrow_length * math.sin(theta) + self.robot_pos['y']*100

        points = [QPoint(int(self.robot_pos['x']*100), int(self.robot_pos['y']*100)),
                  QPoint(int(arrow_x), int(arrow_y))]
                
        qp.setPen(QColor(255, 0, 0))
        qp.drawPolyline(*points)
