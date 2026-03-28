import sqlite3
from datetime import datetime

DB_NAME = 'predictions.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS predictions(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT NOT NULL,
                   car_model TEXT NOT NULL,
                   vehicle_age INTEGER,
                   km_driven INTEGER,
                   fuel_type TEXT,
                   transmission_type TEXT,
                   predicted_price REAL,
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                   ''')
    
    conn.commit()
    conn.close()

def save_prediction(brand, car_model, vehicle_age, km_driven, 
                    fuel_type, transmission_type, predicted_price):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO predictions
            (brand, car_model, vehicle_age, km_driven, fuel_type, transmission_type, predicted_price)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            ''', (brand, car_model, vehicle_age, km_driven, 
          fuel_type, transmission_type, predicted_price))

    conn.commit()
    conn.close()

def get_predictions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
                   SELECT * FROM predictions
                   ORDER BY timestamp DESC
                   ''')
    rows = cursor.fetchall()
    conn.close()
    return rows