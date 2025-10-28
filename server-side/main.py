import keyboard
import json
import random
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

connected = False
message_recieved = False
broker = "localhost"
port = 8084

client_id = f"python-mqtt-{random.randint(0, 1000)}"


def on_connect(client, userdata, flags, rc, *args):
    if rc == 0:
        print("Connected to MQTT Broker!")
        global connected
        connected = True
    else:
        print("Failed to connect, return code %d\n", rc)


def on_message(client, userdata, message):
    pass


client = mqtt_client.Client(
    client_id=client_id,
    callback_api_version=CallbackAPIVersion.VERSION2,
    transport="websockets",
)
print("Connecting...")
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.subscribe(topic="ORDER", qos=2)

client.loop_start()

while connected != True:
    time.sleep(0.2)

print("Connected to Broker")

print("Press q to quit out of program")
while True:
    time.sleep(0.2)
    if keyboard.is_pressed("q"):
        client.disconnect()
        print("Quitting out of program ...")
        break


client.loop_stop()
