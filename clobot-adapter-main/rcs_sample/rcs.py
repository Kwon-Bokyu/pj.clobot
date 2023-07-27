import json, asyncio, logging
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from asyncqt import QEventLoop

# from PyQt5.QtCore import QEventLoop, QTimer
# from quamash import QEventLoop, QThreadExecutor

from controll_widget import ControlWidget
from map_widget import MapWidget
import math, sys
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("RCS")

positions = [
    {"name": 'Node1', "x": 0.6, "y": 1.15},
    {"name": 'Node2', "x": 1.15, "y": 1.15},
    {"name": 'Node3', "x": 1.7, "y": 1.15},
    {"name": 'Node4', "x": 2.25, "y": 1.15},
    {"name": 'Node5', "x": 0.6, "y": 0.6},
    {"name": 'Node6', "x": 1.15, "y": 0.6},
    {"name": 'Node7', "x": 1.7, "y": 0.6},
    {"name": 'Node8', "x": 2.25, "y": 0.6}
]

# Robot initial position
robot_pos = {"x":1.13, "y":0.59, "theta":3.14}

# Distance calculation function
def calc_distance(a, b):
    return math.sqrt((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2)

# Find nearest node to robot's initial position
nearest_node = min(positions, key=lambda node: calc_distance(node, robot_pos))

class RCS(QWidget):
    robot_pos_changed = pyqtSignal(dict, dict)  # signal

    def __init__(self, positions, robot_pos, nearest_node):
        super().__init__()
        self.robot_pos = robot_pos
        self.nearest_node = min(positions, key=lambda node: calc_distance(node, robot_pos))
        self.map_widget = MapWidget(positions, robot_pos, nearest_node)
        self.control_widget = ControlWidget(positions, robot_pos, nearest_node)
        self.initUI()

        # self.map_widget = MapWidget(positions, robot_pos, nearest_node)
        # self.control_widget = ControlWidget(positions, robot_pos, nearest_node)
        self.robot_pos_changed.connect(self.map_widget.handle_robot_pos_changed)
        self.robot_pos_changed.connect(self.control_widget.handle_robot_pos_changed)

        
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.map_widget)
        hbox.addWidget(self.control_widget)

        self.setLayout(hbox)
        self.setWindowTitle('RCS Test')
        self.setGeometry(300, 300, 1000, 900)

    def update_robot_pos(self, new_robot_pos):
        self.robot_pos = new_robot_pos
        self.nearest_node = min(positions, key=lambda node: calc_distance(node, new_robot_pos))
        self.robot_pos_changed.emit(self.robot_pos, self.nearest_node)
        logger.info(self.robot_pos)

async def handle_rcs_client(reader, writer, ex):
  try:
    message = await reader.read() # EOF가 있으면 이렇게 처리
    logger.info(f"Received TCP message: {message}")
    data_dict = json.loads(message)
    data = json.loads(data_dict)
    ex.update_robot_pos(data['agvPosition'])
  except json.JSONDecodeError:
    logger.error(f"Failed to decode JSON: {message}")
  except Exception as e:
    logger.error(f"Unexpected error: {e}")
  finally:
    logger.info("TCP Closing the connection")
    writer.close()

async def main(ex):
  server = await asyncio.start_server(partial(handle_rcs_client, ex=ex), '0.0.0.0', 9999)
  addr = server.sockets[0].getsockname()
  logger.info(f"Serving on {addr}")
  try:
    async with server:
      await server.serve_forever()
  except asyncio.CancelledError:
      logger.info('Server is shutting down.')
      server.close()
      await server.wait_closed()
      logger.info('Server is closed.')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RCS(positions, robot_pos, nearest_node)
    ex.show()

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)  # NEW must set the event loop

    with loop:
        loop.run_until_complete(main(ex))
    sys.exit(app.exec_())