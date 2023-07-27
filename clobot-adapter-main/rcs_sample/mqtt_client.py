import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
load_dotenv()

mqtt_broker_host = os.getenv("MQTT_BROKER_HOST")
mqtt_broker_port = int(os.getenv("MQTT_BROKER_PORT"))
mqtt_topic_prefix = os.getenv("MQTT_TOPIC_PREFIX")
mqtt_keepalive = int(os.getenv("MQTT_KEEPALIVE"))

def on_connect(client, userdata, flags, rc):
  print(f"Connected with result code {str(rc)}")
  client.subscribe(mqtt_topic_prefix+"factsheet")
  print(mqtt_topic_prefix+"factsheet")

def on_message(client, userdata, msg):
  print(f"{msg.topic} {str(msg.payload)}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker_host, mqtt_broker_port, mqtt_keepalive)
client.loop_forever()