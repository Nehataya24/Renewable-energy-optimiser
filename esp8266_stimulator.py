import json
import time
import random
import paho.mqtt.client as mqtt


# -------------------------------------------------
# MQTT Configuration
# -------------------------------------------------

BROKER = "broker.hivemq.com"
PORT = 1883

TOPIC = "renewable_energy_optimizer/neha/sensors"


# -------------------------------------------------
# MQTT Client
# -------------------------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="wind_simulator_neha"
)


print("Connecting to MQTT broker...")

client.connect(BROKER, PORT, 60)

client.loop_start()

print("Connected!")
print("Sending simulated ESP8266 sensor data...\n")


# -------------------------------------------------
# Sensor Simulation
# -------------------------------------------------

while True:

    wind_speed = round(
        random.uniform(3, 15),
        2
    )

    temperature = round(
        random.uniform(20, 45),
        2
    )

    battery_level = random.randint(
        20,
        95
    )

    data = {

        "wind_speed": wind_speed,

        "rpm": random.randint(
            150,
            800
        ),

        "voltage": 12.0,

        "current": round(
            random.uniform(1.0, 4.0),
            2
        ),

        "blade_angle": random.randint(
            5,
            40
        ),

        "temperature": temperature,

        "battery_level": battery_level
    }


    # Convert data to JSON

    message = json.dumps(data)


    # Send data to MQTT

    client.publish(
        TOPIC,
        message
    )


    print("ESP8266 SIMULATOR → MQTT")

    print(message)

    print()


    # Send every 3 seconds

    time.sleep(3)