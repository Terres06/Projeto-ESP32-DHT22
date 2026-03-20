import paho.mqtt.client as mqtt
import os 
import json 
from db.schema import ReadDHT22, Session
from dotenv import load_dotenv

load_dotenv()

# MQTT Broker settings
broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")
client_id = os.getenv("MQTT_CLIENT_ID")

#on_connect and on_message callbacks functions
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker")
        client.subscribe("sensors/dht22")
    else:
        print("Failed to connect, return code %d\n", reason_code)

def on_message(client , userdata, msg):
    db = Session()
    try:
        data = json.loads(msg.payload.decode('utf-8'))
        Read = ReadDHT22(temperature=data['temperature'], humidity=data['humidity'], device_id=data['device_id'])
        db.add(Read)
        db.commit()
        print(f"Received message: {data} on topic {msg.topic}")
    except Exception as e:
        print(f"Error processing message: {e}")
    finally:
        db.close()

#client configuration and connection to the broker
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id)
client.username_pw_set(username=username, password=password)

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, keepalive=60)

client.loop_forever()