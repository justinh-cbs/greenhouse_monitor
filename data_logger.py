#!/usr/bin/env python3
import Adafruit_DHT
import time
import csv
import os
from datetime import datetime

SENSOR = Adafruit_DHT.DHT11
PIN = 4
LOG_FILE = "greenhouse_data.csv"
INTERVAL = 300  # seconds between readings


if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_c", "temperature_f", "humidity"])
    print(f"Created new log file: {LOG_FILE}")


def read_sensor():
    """Read data from DHT11 sensor"""
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)

    if humidity is not None and temperature is not None:
        temp_f = temperature * 9 / 5 + 32
        return {
            "temp_c": round(temperature, 1),
            "temp_f": round(temp_f, 1),
            "humidity": round(humidity, 1),
            "valid": True,
        }
    return {"valid": False}


def log_data(data):
    """Log data to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, data["temp_c"], data["temp_f"], data["humidity"]])
    print(f"Logged data at {timestamp}: {data['temp_c']}°C, {data['humidity']}%")


print(f"Starting greenhouse monitoring. Logging every {INTERVAL} seconds.")
print(f"Data is being saved to {LOG_FILE}")

try:
    while True:
        result = read_sensor()

        if result["valid"]:
            log_data(result)
        else:
            print("Failed to get valid reading from sensor")

        time.sleep(INTERVAL)

except KeyboardInterrupt:
    print("\nMonitoring stopped by user")
except Exception as e:
    print(f"Error: {e}")
