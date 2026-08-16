import sqlite3

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


DATABASE = "energy_data.db"


# =================================================
# Load Training Data
# =================================================

def load_training_data():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            wind_speed,
            temperature,
            battery_level,
            generated_power
        FROM energy_readings
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# =================================================
# Train Random Forest Model
# =================================================

def train_model():

    rows = load_training_data()

    if len(rows) < 20:
        raise ValueError(
            "Not enough data for AI training. "
            "Need at least 20 readings."
        )

    X = []
    y = []

    for row in rows:

        wind_speed = row[0]
        temperature = row[1]
        battery_level = row[2]
        generated_power = row[3]

        X.append([
            wind_speed,
            temperature,
            battery_level
        ])

        y.append(generated_power)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10,
        min_samples_leaf=2
    )

    model.fit(
        X_train,
        y_train
    )

    return model, X_test, y_test


# =================================================
# Predict Generated Power
# =================================================

def predict_power(
    wind_speed,
    temperature,
    battery_level
):

    model, _, _ = train_model()

    prediction = model.predict([
        [
            wind_speed,
            temperature,
            battery_level
        ]
    ])

    predicted_power = max(
        0,
        float(prediction[0])
    )

    return round(
        predicted_power,
        2
    )


# =================================================
# Evaluate AI Model
# =================================================

def evaluate_model():

    model, X_test, y_test = train_model()

    predictions = model.predict(X_test)

    predictions = [
        max(0, float(value))
        for value in predictions
    ]

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    return {
        "mae": round(float(mae), 2),
        "r2_score": round(float(r2), 4),
        "test_samples": len(y_test)
    }


# =================================================
# Test AI Model
# =================================================

if __name__ == "__main__":

    rows = load_training_data()

    print()
    print("========================================")
    print("   WIND ENERGY AI MODEL")
    print("========================================")

    print(
        "Training samples:",
        len(rows)
    )

    # Train model

    model, X_test, y_test = train_model()

    print(
        "AI model trained successfully!"
    )

    print(
        "Test samples:",
        len(y_test)
    )

    # Example prediction

    predicted_power = predict_power(
        wind_speed=8,
        temperature=30,
        battery_level=70
    )

    print(
        "Predicted generated power:",
        predicted_power,
        "W"
    )

    # Evaluate model

    performance = evaluate_model()

    print(
        "Mean Absolute Error:",
        performance["mae"],
        "W"
    )

    print(
        "R² Score:",
        performance["r2_score"]
    )

    print("========================================")