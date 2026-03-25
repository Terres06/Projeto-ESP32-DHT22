import paho.mqtt.client as mqtt
import json 
import os 
import random 
import time 
import dotenv


dotenv.load_dotenv()

broker = os.getenv("MQTT_BROKER")
port = int(os.getenv("MQTT_PORT"))
username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")
client_id = "SIM_ESP32_1"

def random_data():
    temperature = round(random.uniform(20.0, 35.0), 2)
    humidity = round(random.uniform(40.0, 80.0), 2)
    device_id = "ESP32_01"
    return {"temperature": temperature, "humidity": humidity, "device_id": device_id}

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT Broker")
    else:
        print("Failed to connect, return code %d\n", reason_code)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)

client.on_connect = on_connect

client.username_pw_set(username=username, password=password)
client.connect(broker, port, keepalive=60)

client.loop_start()

while True:
    data = random_data()
    client.publish("sensors/dht22", json.dumps(data))
    print(f"[Simulator]Published: {data} to topic sensors/dht22")
    time.sleep(random.uniform(5, 10))
    