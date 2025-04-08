#!/usr/bin/env python3
import Adafruit_DHT


SENSOR = Adafruit_DHT.DHT11
PIN = 4
LOG_FILE = "greenhouse_data.csv"
INTERVAL = 300  # seconds between readings

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
