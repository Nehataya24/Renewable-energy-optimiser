import json
import threading

from fastapi import FastAPI
import paho.mqtt.client as mqtt

app = FastAPI()

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "renewable_energy_optimizer/neha/sensors"


def optimize_energy(data):
    wind_speed = data.get("wind_speed", 0)
    generated_power = data.get("generated_power", 0)
    battery_level = data.get("battery_level", 0)
    temperature = data.get("temperature", 0)

    if generated_power <= 0:
        load_status = "OFF"
        efficiency = 0
        recommendation = "No power generated. Turn OFF non-essential loads."

    elif battery_level < 20:
        load_status = "REDUCED"
        efficiency = 55
        recommendation = "Battery is critically low. Reduce unnecessary loads."

    elif temperature > 45:
        load_status = "REDUCED"
        efficiency = 60
        recommendation = "High temperature detected. Reduce system load."

    else:
        load_status = "ON"
        efficiency = 85
        recommendation = "System is operating efficiently."

    return {
        "wind_speed": wind_speed,
        "generated_power": generated_power,
        "battery_level": battery_level,
        "temperature": temperature,
        "efficiency": efficiency,
        "recommendation": recommendation,
        "load_status": load_status
    }


@app.get("/")
def home():
    return {"message": "Wind Energy Optimizer Backend is Working"}


@app.post("/optimize")
def optimize_api(data: dict):
    return optimize_energy(data)


def on_connect(client, userdata, flags, reason_code, properties):
    print("FastAPI connected to MQTT!")
    client.subscribe(TOPIC)
    print(f"Subscribed to: {TOPIC}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print("\nMQTT DATA RECEIVED:")
        print(data)

        result = optimize_energy(data)

        print("OPTIMIZATION RESULT:")
        print(result)

    except Exception as e:
        print("MQTT processing error:", e)


mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="fastapi_backend_neha"
)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


def start_mqtt():
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.loop_forever()


threading.Thread(target=start_mqtt, daemon=True).start()