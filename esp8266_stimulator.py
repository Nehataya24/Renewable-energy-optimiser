import json
import time
import random
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "renewable_energy_optimizer/neha/sensors"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="wind_simulator_neha"
)

print("Connecting to MQTT broker...")

client.connect(BROKER, PORT, 60)
client.loop_start()

print("Connected!")
print("Sending simulated ESP8266 sensor data...\n")

while True:

    data = {
        "wind_speed": round(random.uniform(3, 15), 2),
        "rpm": random.randint(150, 800),
        "voltage": round(random.uniform(11.5, 13.0), 2),
        "current": round(random.uniform(1.0, 4.0), 2),
        "blade_angle": random.randint(5, 40),
        "temperature": round(random.uniform(20, 40), 2)
    }

    message = json.dumps(data)

    client.publish(TOPIC, message)

    print("ESP8266 SIMULATOR → MQTT")
    print(message)
    print()

    time.sleep(3)