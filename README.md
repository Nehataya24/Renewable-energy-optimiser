# 🌬️ Wind Energy Optimizer

Smart Wind Energy Monitoring & Optimization System using FastAPI, MQTT, SQLite, and Machine Learning.

## 📌 Project Overview

The Wind Energy Optimizer is a software-based renewable energy monitoring and optimization system designed to monitor wind turbine conditions, calculate generated power, optimize three flap angles according to wind speed, and predict future power generation using a Random Forest Regression model.

The system receives simulated ESP8266 sensor data through MQTT, processes it using a FastAPI backend, stores energy readings in SQLite, and displays real-time information through a web dashboard.

## ✨ Features

- Real-time wind speed monitoring
- Generated power calculation
- Battery level monitoring
- Temperature monitoring
- Automatic 3-flap angle optimization
- Smart load management
- System alerts
- Energy performance history
- AI-based power prediction
- Random Forest Regression model
- AI model performance evaluation
- MQTT communication
- SQLite data storage
- FastAPI REST API
- Interactive web dashboard
- Automatic dashboard updates

## 🧠 AI Model

The project uses **Random Forest Regression** to predict generated wind power based on:

- Wind speed
- Temperature
- Battery level

Latest model performance:

- Model: Random Forest Regression
- R² Score: 1.00
- Mean Absolute Error: approximately 4 W

The model is trained using the energy data collected by the system.

## 🏗️ System Architecture

ESP8266 Simulator
        ↓
      MQTT
        ↓
   FastAPI Backend
        ↓
 ┌──────┴───────┐
 ↓              ↓
SQLite       AI Model
Database     Prediction
 ↓              ↓
 └──────┬───────┘
        ↓
 Web Dashboard

## 🛠️ Technologies Used

- Python
- FastAPI
- Uvicorn
- MQTT
- Paho MQTT
- SQLite
- Scikit-learn
- NumPy
- HTML
- CSS
- JavaScript
- Chart.js

## 📁 Project Structure

```text
Renewable energy optimizer/
│
├── main.py
├── ai_model.py
├── database.py
├── esp8266_stimulator.py
├── requirements.txt
├── energy_data.db
│
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
