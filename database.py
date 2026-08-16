import sqlite3


DATABASE = "energy_data.db"


# -------------------------------------------------
# Create Database
# -------------------------------------------------

def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_readings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            wind_speed REAL,

            generated_power REAL,

            battery_level REAL,

            temperature REAL,

            flap_1_angle REAL,

            flap_2_angle REAL,

            flap_3_angle REAL,

            efficiency REAL,

            load_status TEXT,

            recommendation TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    connection.close()


# -------------------------------------------------
# Save Energy Reading
# -------------------------------------------------

def save_energy_reading(data):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO energy_readings (

            wind_speed,
            generated_power,
            battery_level,
            temperature,
            flap_1_angle,
            flap_2_angle,
            flap_3_angle,
            efficiency,
            load_status,
            recommendation

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        data.get("wind_speed", 0),

        data.get("generated_power", 0),

        data.get("battery_level", 0),

        data.get("temperature", 0),

        data.get("flap_1_angle", 0),

        data.get("flap_2_angle", 0),

        data.get("flap_3_angle", 0),

        data.get("efficiency", 0),

        data.get("load_status", "UNKNOWN"),

        data.get("recommendation", "")

    ))

    connection.commit()

    connection.close()


# -------------------------------------------------
# Get Energy Readings
# -------------------------------------------------

def get_energy_readings():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *

        FROM energy_readings

        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]