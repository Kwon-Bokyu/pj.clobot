import paho.mqtt.client as mqtt
import time, os, logging, re
from dotenv import load_dotenv
load_dotenv()

class MQTTClient:
  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.host = os.getenv("MQTT_BROKER_HOST")
    self.port = int(os.getenv("MQTT_BROKER_PORT"))
    self.mqtt_topic_prefix = os.getenv("MQTT_TOPIC_PREFIX")
    self.keepalive = int(os.getenv("MQTT_KEEPALIVE"))
    self.retry_interval = int(os.getenv("MQTT_RETRY_INTERVAL"))
    self.conn = mqtt.Client()
    self.topic_handlers = {}


    self.conn.on_connect = self.on_connect
    self.conn.on_disconnect = self.on_disconnect
    self.conn.on_message = self.on_message

  def on_connect(self, client, userdata, flags, rc):
    if rc == 0:
      for topic in self.topic_handlers:
        self.logger.info(topic)
        self.conn.subscribe(topic, qos=0)
      self.logger.info("Connected successfully.")
    else:
      self.logger.info("Connection failed with code %s." % rc)

  def on_disconnect(self, client, userdata, rc):
    self.logger.info("Client got disconnected.")
    while True:
      try:
        self.logger.info("Trying to reconnect.")
        time.sleep(self.retry_interval)
        self.conn.reconnect()
        break
      except ConnectionRefusedError:
        self.logger.info(f"Connection refused, will try again in {self.retry_interval} second.")
        time.sleep(1)

  def match_topic(self, topic_pattern, topic):
    pattern = topic_pattern.replace('+', '[^/]+').replace('#', '.*')
    matcher = re.compile(pattern+'$')
    match = matcher.match(topic) is not None
    if match:
        self.logger.debug(f"'{topic}' matches pattern '{topic_pattern}'")
    else:
        self.logger.debug(f"'{topic}' does not match pattern '{topic_pattern}'")
    return match

  def on_message(self, client, userdata, message):
    topic = message.topic
    self.logger.info(topic)
    for topic_pattern, handler in self.topic_handlers.items():
      if self.match_topic(topic_pattern, topic):
        handler(message)
        break

  def register_topic_handler(self, topic, handler):
    self.topic_handlers[topic] = handler
    self.conn.subscribe(topic)

  # todo: 최초 connenct 시점에 broker 연결 안될시 재시도 하는 코드 추가
  def connect(self):
    try:
      self.conn.connect(self.host, self.port, self.keepalive)
      self.conn.loop_start()
    except Exception as e:
      self.logger.error("Exception: %s" % e)