import json
import threading

import paho.mqtt.client as mqtt
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from database import create_database, save_energy_reading, get_energy_readings
from ai_model import predict_power, evaluate_model


# -------------------------------------------------
# FastAPI
# -------------------------------------------------

app = FastAPI(title="Wind Energy Optimizer")

create_database()


# -------------------------------------------------
# Serve Frontend
# -------------------------------------------------

app.mount(
    "/frontend",
    StaticFiles(directory="frontend"),
    name="frontend"
)


# -------------------------------------------------
# CORS
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# MQTT Configuration
# -------------------------------------------------

BROKER = "broker.hivemq.com"
PORT = 1883

TOPIC = "renewable_energy_optimizer/neha/sensors"
OPTIMIZATION_TOPIC = "renewable_energy_optimizer/neha/optimization"


# -------------------------------------------------
# Flap Angle Optimization
# -------------------------------------------------

def calculate_flap_angles(wind_speed):

    if wind_speed < 3:
        return {
            "flap_1_angle": 0,
            "flap_2_angle": 0,
            "flap_3_angle": 0
        }

    elif wind_speed < 6:
        return {
            "flap_1_angle": 10,
            "flap_2_angle": 15,
            "flap_3_angle": 20
        }

    elif wind_speed < 10:
        return {
            "flap_1_angle": 20,
            "flap_2_angle": 25,
            "flap_3_angle": 30
        }

    else:
        return {
            "flap_1_angle": 30,
            "flap_2_angle": 35,
            "flap_3_angle": 40
        }


# -------------------------------------------------
# Energy Optimization
# -------------------------------------------------

def optimize_energy(data):

    wind_speed = data.get("wind_speed", 0)

    # Wind turbine power calculation
    air_density = 1.225
    swept_area = 10
    power_coefficient = 0.35

    generated_power = (
        0.5
        * air_density
        * swept_area
        * (wind_speed ** 3)
        * power_coefficient
    )

    battery_level = data.get("battery_level", 0)
    temperature = data.get("temperature", 0)

    flap_angles = calculate_flap_angles(wind_speed)


    # -------------------------------------------------
    # Energy Management Logic
    # -------------------------------------------------

    if generated_power <= 0:

        load_status = "OFF"
        efficiency = 0

        recommendation = (
            "No power generated. Turn OFF non-essential loads."
        )

    elif battery_level < 20:

        load_status = "REDUCED"
        efficiency = 55

        recommendation = (
            "Battery is critically low. Reduce unnecessary loads."
        )

    elif temperature > 45:

        load_status = "REDUCED"
        efficiency = 60

        recommendation = (
            "High temperature detected. Reduce system load."
        )

    else:

        load_status = "ON"
        efficiency = 85

        recommendation = (
            "System is operating efficiently."
        )


    # -------------------------------------------------
    # Optimization Result
    # -------------------------------------------------

    return {

        "wind_speed": wind_speed,

        "generated_power": generated_power,

        "battery_level": battery_level,

        "temperature": temperature,

        "flap_1_angle": flap_angles["flap_1_angle"],

        "flap_2_angle": flap_angles["flap_2_angle"],

        "flap_3_angle": flap_angles["flap_3_angle"],

        "efficiency": efficiency,

        "recommendation": recommendation,

        "load_status": load_status
    }


# -------------------------------------------------
# FastAPI Routes
# -------------------------------------------------

@app.get("/")
def home():

    return FileResponse(
        "frontend/index.html"
    )


@app.post("/optimize")
def optimize_api(data: dict):

    result = optimize_energy(data)

    save_energy_reading(result)

    return result


@app.get("/readings")
def get_readings():

    return get_energy_readings()
# -------------------------------------------------
# AI Power Prediction
# -------------------------------------------------

# -------------------------------------------------
# AI Power Prediction
# -------------------------------------------------

@app.get("/ai-prediction")
def ai_prediction():

    readings = get_energy_readings()

    if not readings:

        return {
            "error": "No energy data available"
        }

    latest = readings[0]

    predicted_power = predict_power(
        wind_speed=latest["wind_speed"],
        temperature=latest["temperature"],
        battery_level=latest["battery_level"]
    )

    actual_power = float(
        latest["generated_power"]
    )

    prediction_error = abs(
        actual_power - predicted_power
    )

    return {
        "wind_speed": latest["wind_speed"],
        "temperature": latest["temperature"],
        "battery_level": latest["battery_level"],
        "actual_power": round(actual_power, 2),
        "predicted_power": predicted_power,
        "prediction_error": round(prediction_error, 2)
    }


# -------------------------------------------------
# AI Model Performance
# -------------------------------------------------

@app.get("/ai-performance")
def ai_performance():

    try:

        performance = evaluate_model()

        return {
            "model": "Random Forest Regression",
            "training_samples": len(
                get_energy_readings()
            ),
            "test_samples": performance["test_samples"],
            "mean_absolute_error": performance["mae"],
            "r2_score": performance["r2_score"]
        }

    except Exception as e:

        return {
            "error": str(e)
        }

# -------------------------------------------------
# MQTT Client
# -------------------------------------------------

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="fastapi_backend_neha"
)


# -------------------------------------------------
# MQTT Connected
# -------------------------------------------------

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    print("FastAPI connected to MQTT!")

    client.subscribe(TOPIC)

    print(
        f"Subscribed to: {TOPIC}"
    )


# -------------------------------------------------
# MQTT Message Received
# -------------------------------------------------

def on_message(
    client,
    userdata,
    msg
):

    try:

        # Convert MQTT message to Python dictionary

        data = json.loads(
            msg.payload.decode()
        )


        print("\nMQTT DATA RECEIVED:")

        print(data)


        # -------------------------------------------------
        # Run Optimization
        # -------------------------------------------------

        result = optimize_energy(data)


        print(
            "OPTIMIZATION RESULT:"
        )

        print(result)


        # -------------------------------------------------
        # Save Result to SQLite
        # -------------------------------------------------

        save_energy_reading(result)


        print(
            "Energy reading saved to database."
        )


        # -------------------------------------------------
        # Publish Optimization Result
        # -------------------------------------------------

        info = mqtt_client.publish(

            OPTIMIZATION_TOPIC,

            json.dumps(result)

        )


        print(
            "Optimization result published to:"
        )

        print(
            OPTIMIZATION_TOPIC
        )

        print(
            f"Publish status: {info.rc}"
        )


    except Exception as e:

        print(
            "MQTT processing error:",
            e
        )


# -------------------------------------------------
# MQTT Callbacks
# -------------------------------------------------

mqtt_client.on_connect = on_connect

mqtt_client.on_message = on_message


# -------------------------------------------------
# Start MQTT
# -------------------------------------------------

def start_mqtt():

    try:

        mqtt_client.connect(
            BROKER,
            PORT,
            60
        )

        mqtt_client.loop_forever()

    except Exception as e:

        print(
            "MQTT connection error:",
            e
        )


# -------------------------------------------------
# Background MQTT Thread
# -------------------------------------------------

threading.Thread(
    target=start_mqtt,
    daemon=True
).start()