from dotenv import load_dotenv
import os
import json
import logging
import random
import time
import threading
import ssl

from paho.mqtt import client as mqtt_client
from paho.mqtt.enums import CallbackAPIVersion
from paho import mqtt

# Initialize global variables
load_dotenv()
running = True
broker = os.getenv("BROKER_URL")
port = int(os.getenv("PORT"))
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
length = int(os.getenv("LENGTH"))
processing = [False for _ in range(length)]
client_id = f"python-mqtt-{random.randint(0, 1000)}"
logger = logging.getLogger(__name__)


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
        logger.info("Connected to Broker")
        client.subscribe(topic="ORDER", qos=2)
        return True
    else:
        print("Failed to connect, return code", rc)
        logger.info("Failed to connect to Broker")
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
    logger.info("Shutting down backend")
    global running
    running = False
    return running


def on_message(client, userdata, message):
    """
    Callback function triggered when the MQTT client receives a message from broker

    This function is called automatically by the Paho MQTT client when the
    client recieves a message. This function then starts a background
    thread to process a food order if the given input is valid.

    Parameters
    ----------
    client
        The MQTT client instance that initiated the connection.
    userdata
        The private user data.
    message
        The MQTT message object
    """
    message_json = json.loads(str(message.payload.decode("utf-8")))

    logger.info(f"Got {str(message_json)} message from broker")
    print(f"Got {str(message_json)} message from broker")

    global processing

    if "id" not in message_json or "order" not in message_json:
        logger.info("Malformed message: id or order not in message")
        print("Malformed message: id or order not in message")
        return False

    try:
        id = int(message_json["id"])
    except ValueError:
        logger.info("Malformed message: id is not an int")
        print("Malformed message: id is not an int")
        return False

    order = message_json["order"]

    if id >= len(processing) or processing[id - 1]:
        logger.info("Malformed message: id out of bounds")
        print("Malformed message: id out of bounds")
        return False

    logger.info(f"Processing order on table #{id}")
    print(f"Processing order on table #{id}")
    processing[id - 1] = True
    thread = threading.Thread(target=waitThenSendFood, args=(id, client, order))
    thread.start()
    return True


def waitThenSendFood(id, client, order):
    """
    This function waits for a random amount of time (between 1 second
    and 20 seconds) and then publishes the completed order in "FOOD" topic

    Parameters
    ----------
    id
        the id of the table that the food is meant to go to.
    client
        The MQTT client instance that initiated the connection.
    order
        The name of the order.
    """
    time.sleep(random.randint(1, 20))
    message = json.dumps({"id": id, "order": order})
    client.publish("FOOD", message, qos=2)
    logger.info(f"Published {str(message)} to FOOD topic.")
    print(f"Published {str(message)} to FOOD topic.")
    global processing
    logger.info(f"Done processing table #{id}")
    print(f"Done processing table #{id}")
    processing[id - 1] = False


if __name__ == "__main__":
    logging.basicConfig(filename="backend.log", level=logging.INFO)
    client = mqtt_client.Client(
        client_id=client_id,
        callback_api_version=CallbackAPIVersion.VERSION2,
        transport="websockets",
    )

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set(username=username, password=password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    logger.info("Connecting to Broker")
    print("Connecting...")
    try:
        client.connect(broker, port)
    except ConnectionRefusedError:
        logger.info("Broker refused to connect")
        print("Broker refused to connect")
        print("Exiting ...")
        running = False

    client.loop_start()

    if running:
        print("To Quit, press <C-c>")

    try:
        while running:
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Quitting ...")
        logger.info("User stopped backend")

        client.loop_stop()
    client.disconnect()
