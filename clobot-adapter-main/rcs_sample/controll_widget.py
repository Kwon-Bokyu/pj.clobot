from functools import partial
import socket, json, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit
from commands.moving import create_update_forward_dict, create_update_turn_dict, create_update_angle_dict
from PyQt5.QtCore import pyqtSlot
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

robot_server_host = '192.168.103.48'
robot_server_port = 8888

class ControlWidget(QWidget):
    def __init__(self, positions, robot_pos, nearest_node):
        super().__init__()
        self.positions = positions
        self.robot_pos = robot_pos
        self.nearest_node = nearest_node
        self.x_line_edit = QLineEdit(self)
        self.y_line_edit = QLineEdit(self)
        self.angle_edit = QLineEdit(self)
        self.initUI()

    def initUI(self):

        btn1 = QPushButton('북', self)
        btn1.clicked.connect(partial(self.on_direction_click, direction=0))

        btn2 = QPushButton('동', self)
        btn2.clicked.connect(partial(self.on_direction_click, direction=90))

        btn3 = QPushButton('남', self)
        btn3.clicked.connect(partial(self.on_direction_click, direction=180))

        btn4 = QPushButton('서', self)
        btn4.clicked.connect(partial(self.on_direction_click, direction=270))

        btn_forward = QPushButton('이동', self)
        btn_forward.clicked.connect(self.on_forward_click)

        btn_tilt = QPushButton('틸트', self)
        btn_tilt.clicked.connect(self.on_tilt_click)

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)

        vbox.addWidget(self.x_line_edit)
        vbox.addWidget(self.y_line_edit)
        vbox.addWidget(btn_forward)

        vbox.addWidget(self.angle_edit)
        vbox.addWidget(btn_tilt)

        self.setGeometry(400, 10, 100, 600)

        self.setLayout(vbox)




    @pyqtSlot(dict, dict)
    def handle_robot_pos_changed(self, new_robot_pos, new_nearest_node):
        self.robot_pos = new_robot_pos
        self.nearest_node = new_nearest_node
        self.update() 

    def on_direction_click(self, direction):
        data = create_update_turn_dict(self.robot_pos, self.nearest_node, direction)
        print(data)
        json_data = json.dumps(data)
        # TCP/IP 소켓 생성
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
          # 서버에 연결
          sock.connect((robot_server_host, robot_server_port))

          # 데이터 전송
          sock.sendall(json_data.encode())

    def on_forward_click(self):
        x = self.x_line_edit.text()
        y = self.y_line_edit.text()
        data = create_update_forward_dict(self.robot_pos, self.nearest_node, {"x": float(x), "y": float(y)})
        print(data)
        json_data = json.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
          # 서버에 연결
          sock.connect((robot_server_host, robot_server_port))

          # 데이터 전송
          sock.sendall(json_data.encode())

    def on_tilt_click(self):
        angle = self.angle_edit.text()
        data = create_update_angle_dict(self.robot_pos, self.nearest_node, int(angle))
        print(data)
        json_data = json.dumps(data)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
          # 서버에 연결
          sock.connect((robot_server_host, robot_server_port))

          # 데이터 전송
          sock.sendall(json_data.encode())


# 북 = 0
# 동 = 90
# 남 = 180
# 서 = 270