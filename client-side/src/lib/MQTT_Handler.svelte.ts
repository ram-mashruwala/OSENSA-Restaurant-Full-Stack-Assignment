import mqtt from 'mqtt';

const BROKER_URL = 'ws://localhost:8084/mqtt';

const client: mqtt.MqttClient = mqtt.connect(BROKER_URL);

export let connection_state = $state({ connected: false })

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  connection_state.connected = true;
  client.subscribe('test', { qos: 2 }, (err: Error | null) => {
    if (err) console.error('Subscription error:', err);
  });
});

client.on('error', (err: Error) => {
  console.error('MQTT connection error:', err);
});

client.on('message', (topic: string, message: Buffer<ArrayBufferLike>) => {
  console.log(`${topic}: ${message.toString()}`);
});


export default client;
