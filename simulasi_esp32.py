import paho.mqtt.client as mqtt
import json, time, random
from datetime import datetime

BROKER = "localhost"
TOPIC_SENSOR = "iot/sensor"
TOPIC_KONTROL = "iot/kontrol"
TOPIC_ALERT = "iot/alert"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Terhubung ke MQTT Broker!")
        client.subscribe([(TOPIC_KONTROL, 0), (TOPIC_ALERT, 0)])
    else:
        print(f"Gagal terhubung, kode: {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == TOPIC_KONTROL:
        print(f"\n[KONTROL DITERIMA] -> {payload}")
    elif topic == TOPIC_ALERT:
        data = json.loads(payload)
        print(f"\n🚨 [NOTIFIKASI ALERT] -> {data['message']}")

client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
    client_id="ESP32-Simulator"
)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_start()
print("ESP32 Simulator berjalan... Ctrl+C untuk stop")

try:
    while True:
        # Sesekali hasilkan suhu tinggi (> 30°C) untuk memicu alert
        data = {
            "suhu": round(random.uniform(26.0, 33.5), 1),
            "kelembaban": round(random.uniform(55.0, 80.0), 1),
            "timestamp": datetime.now().isoformat()
        }
        
        client.publish(TOPIC_SENSOR, json.dumps(data))
        print(f"→ Publish Sensor: {data}")
        time.sleep(3)

except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()