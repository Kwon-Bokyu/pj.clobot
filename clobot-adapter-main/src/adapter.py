import asyncio, os, json, logging, threading, math
from dotenv import load_dotenv

from dataclasses import asdict
from pydantic import ValidationError
from data_model.registration import Connection, InstantActions, Factsheet
from data_model.order_command import Order
from data_model.status_report import State
from mqtt_client import MQTTClient
from tcp_client import TCPClient

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Adapter")

mqtt_topic_prefix = os.getenv("MQTT_TOPIC_PREFIX")
tcp_server_host = os.getenv("TCP_SERVER_HOST")
tcp_server_port = int(os.getenv("TCP_SERVER_PORT"))

topic_handlers = {
  'connection': Connection,
  'factsheet': Factsheet,
  'state': State
}

def load_maps(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

maps = load_maps('src/map.json')

# Distance calculation function
def calc_distance(a, b):
    return math.sqrt((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2)

now_state = None

mqtt_client = MQTTClient()

def handle_message(model, message, topic):
  global now_state
  data = message.payload.decode()
  try:
    state_data = json.loads(data)
    pydantic_model = model.model_validate(state_data)
    if topic == 'state':
      now_state = pydantic_model
    # print(f"Validated state data: {pydantic_model.model_dump_json()}")
    # RCS 세팅 후 확인
    TCPClient().send_json(pydantic_model.model_dump_json())

  except json.JSONDecodeError:
    print(f"Failed to decode JSON: {data}")
  except ValidationError as e:
    print(f"Data validation failed: {e}")
  except Exception as e:
    print(f"Unexpected error occurred: {e}")

for topic, model in topic_handlers.items():
    handler = lambda message: handle_message(model, message, topic)
    mqtt_client.register_topic_handler(mqtt_topic_prefix + "+/" + topic, handler)

mqtt_thread = threading.Thread(target=mqtt_client.connect)
mqtt_thread.start()


def data_to_json(data):
  data_dict = asdict(data)  
  return json.dumps(data_dict)

def select_data_class(data_dict: dict):
  if 'actions' in data_dict:
    return InstantActions
  elif 'physicalParameters' in data_dict:
    return Factsheet
  elif 'connectionState' in data_dict:
    return Connection
  elif 'orderId' in data_dict:
    return Order
  else:
    return None

def convert_to_classname(class_instance):
    class_name = class_instance.__class__.__name__
    return class_name[0].lower() + class_name[1:]

async def handle_rcs_client(reader, writer):
  try:
    logger.info(now_state)
    message = await reader.read() # EOF가 있으면 이렇게 처리
    logger.info(f"Received TCP message: {message}")
    data_dict = json.loads(message)
    selected_class = select_data_class(data_dict)
    if selected_class is not None:
      pydantic_model = selected_class.model_validate(data_dict)
      subtopic = convert_to_classname(pydantic_model)      
      publish_topic = mqtt_topic_prefix+pydantic_model.serialNumber+'/'+subtopic
      logger.info(f"Publishing for {publish_topic}")

      # todo: mqtt_client 연결상태 체크 후 예외처리
      mqtt_client.conn.publish(publish_topic, pydantic_model.model_dump_json())
    else:
      logger.error("Unsupported data format")
  except json.JSONDecodeError:
    logger.error(f"Failed to decode JSON: {message}")
  except Exception as e:
    logger.error(f"Unexpected error: {e}")
  finally:
    logger.info("TCP Closing the connection")
    writer.close()

async def main():
  server = await asyncio.start_server(handle_rcs_client, '0.0.0.0', 8888)

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




asyncio.run(main())
