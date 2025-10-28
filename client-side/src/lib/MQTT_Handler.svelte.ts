import mqtt from 'mqtt';

const BROKER_URL = 'ws://localhost:8084/mqtt';

const client: mqtt.MqttClient = mqtt.connect(BROKER_URL);

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.subscribe('test', (err) => {
    if (err) console.error('Subscription error:', err);
  });
});

client.on('error', (err) => {
  console.error('MQTT connection error:', err);
});

client.on('message', (topic, message) => {
  console.log(`${topic}: ${message.toString()}`);
});

export default client;
