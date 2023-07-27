import os, socket, json, logging
from dotenv import load_dotenv
load_dotenv()

class TCPClient:
  def __init__(self):
    self.server_host = os.getenv("TCP_SERVER_HOST")
    self.server_port = int(os.getenv("TCP_SERVER_PORT"))
    self.logger = logging.getLogger(self.__class__.__name__)

  def send_json(self, data: dict):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
      sock.connect((self.server_host, self.server_port))
      message = json.dumps(data)
      sock.sendall(message.encode())
      # self.logger.info(f"Message sent: {message}")
    except Exception as e:
      self.logger.error(f"Unexpected error: {e}")
    finally:
      sock.close()
      self.logger.info("Socket closed.")
