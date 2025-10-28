import json
import random
import time

from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion

running = True
message_recieved = False
broker = "localhost"
port = 8084

client_id = f"python-mqtt-{random.randint(0, 1000)}"


def on_connect(client, userdata, flags, rc, properties):
    """
    Callback function triggered when the MQTT client connects to the broker.

    This function is called automatically by the Paho MQTT client when a
    connection attempt to the MQTT broker completes—either successfully or
    unsuccessfully. It sets the global `connected` flag to True if the connection
    was successful, or prints an error message if the connection failed.

    Parameters
    ----------
    client
        The MQTT client instance that initiated the connection.
    userdata
        The private user data.
    flags
        Response flags sent by the broker, typically containing session information.
    rc
        The connection result. A value of 0 indicates success. Non-zero values
        indicate different connection errors.
    properties
        MQTT v5.0 properties returned by the broker on connection.
    """

    if rc == 0:
        print("Connected to MQTT Broker!")
        return True
    else:
        print("Failed to connect, return code %d\n", rc)
        return False


def on_disconnect(client, userdata, flags, reason_code, properties):
    """
    Callback function triggered when the MQTT client disconnects from broker.

    This function is called automatically by the Paho MQTT client
    when it disconnects from the MQTT broker. It sets the global
    `running` flag to False
    """
    print("Server Disconnected ...")
    print("Shutting Down ...")
    global running
    running = False


def on_message(client, userdata, message):
    pass


client = mqtt_client.Client(
    client_id=client_id,
    callback_api_version=CallbackAPIVersion.VERSION2,
    transport="websockets",
)

if __name__ == "__main__":
    print("Connecting...")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    client.subscribe(topic="ORDER", qos=2)

    client.loop_start()

    print("Connected to Broker")

    while running:
        time.sleep(0.2)

    client.loop_stop()
