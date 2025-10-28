import mqtt from 'mqtt';
import { tableState } from './state.svelte';

const BROKER_URL = 'ws://localhost:8084/mqtt';

const client: mqtt.MqttClient = mqtt.connect(BROKER_URL);

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
});

client.on('error', (err: Error) => {
  console.error('MQTT connection error:', err);
});

client.on('message', (topic: string, message: Buffer<ArrayBufferLike>) => {
  console.log(`${topic}: ${message.toString()}`);

  const messageJson = JSON.parse(message.toString())
  const id: number = messageJson["id"]
  tableState[id - 1]["arrived"] = true
});

export function Order(table_id: number) {
  client.publish("ORDER", JSON.stringify({ "id": table_id }))
  tableState[table_id - 1]["ordered"] = true
}

export default client;
