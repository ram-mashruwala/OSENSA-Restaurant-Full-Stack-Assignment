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


client = mqtt_client.Client(
    client_id=client_id,
    callback_api_version=CallbackAPIVersion.VERSION2,
    transport="websockets",
)
# client.tls_set(ca_certs='./server-ca.crt')
print("Connecting...")
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()

while connected != True:
    time.sleep(0.2)

client.publish(
    topic="test", payload=json.dumps({"test": "testing", "test2": "testing2"})
)

client.loop_stop()
