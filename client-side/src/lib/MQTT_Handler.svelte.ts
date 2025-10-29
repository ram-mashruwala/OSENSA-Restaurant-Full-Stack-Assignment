import mqtt from 'mqtt';
import { tableState } from './state.svelte';

const BROKER_URL = 'wss://64a28646a5ce4627990d708b63f21208.s1.eu.hivemq.cloud:8884/mqtt';
const OPTIONS = {
  "protocolVersion": 5,
  "username": "testing",
  "password": "Test123456"
}


const client: mqtt.MqttClient = mqtt.connect(BROKER_URL, OPTIONS);

export let connection_state = $state({ connected: false })

client.on("close", () => {
  console.log("closed MQTT connection");
  connection_state.connected = false
})

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  connection_state.connected = true;
  client.subscribe('FOOD', { qos: 2 }, (err: Error | null) => {
    if (err) console.error('Subscription error:', err);
  });
  client.subscribe('ORDER', { qos: 2 }, (err: Error | null) => {
    if (err) console.error('Subscription error:', err);
  });
});

client.on('error', (err: Error) => {
  console.error('MQTT connection error:', err);
});

client.on('message', (topic: string, message: Buffer<ArrayBufferLike>) => {
  console.log(`${topic}: ${message.toString()}`);

  const messageJson = JSON.parse(message.toString())
  if (!("id" in messageJson) || !("order" in messageJson)) {
    return
  }
  const id: number = messageJson["id"]
  const orderName: string = messageJson["order"]
  if (topic === "ORDER") {
    tableState[id - 1]["arrived"] = false
    tableState[id - 1]["ordered"] = true
    return
  }

  tableState[id - 1]["arrived"] = true
  tableState[id - 1]["orderName"] = orderName
});

export function Order(table_id: number, order: string) {
  client.publish("ORDER", JSON.stringify({ "id": table_id, "order": order }))
  tableState[table_id - 1]["ordered"] = true
}

export default client;
