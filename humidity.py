import Adafruit_DHT
import time

SENSOR = Adafruit_DHT.DHT11
PIN = 4  # GPIO pin number (not physical pin number), change if different


def read_sensor():
    for _ in range(5):
        humidity, temperature = Adafruit_DHT.read_retry(SENSOR, PIN)

        if humidity is not None and temperature is not None:
            temp_f = temperature * 9 / 5.0 + 32  # convert C to F

            print("Temp: {:.1f}°C / {:.1f}°F".format(temperature, temp_f))
            print("Humidity: {:.1f}%".format(humidity))

            return {
                "temp_c": temperature,
                "temp_f": temp_f,
                "humidity": humidity,
                "valid": True,
            }

        time.sleep(2)

    print("Failed to get reading after multiple attempts")
    return {"valid": False}


try:
    while True:
        result = read_sensor()
        if result["valid"]:
            print("Valid reading obtained")
        else:
            print("Reading failed")

        print("-" * 30)
        time.sleep(5)

except KeyboardInterrupt:
    print("Program stopped by user")
except Exception as e:
    print(f"Error: {e}")
