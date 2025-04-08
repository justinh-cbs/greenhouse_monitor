import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_PIN = 4

GPIO.setup(GPIO_PIN, GPIO.OUT)


def read_dht11():
    GPIO.output(GPIO_PIN, GPIO.LOW)
    time.sleep(0.018)
    GPIO.output(GPIO_PIN, GPIO.HIGH)

    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    data = []
    for i in range(40):
        counter = 0
        while GPIO.input(GPIO_PIN) == GPIO.LOW:
            counter += 1
            if counter > 100000:
                break

        counter = 0
        while GPIO.input(GPIO_PIN) == GPIO.HIGH:
            counter += 1
            if counter > 100000:
                break

        if counter > 3:
            data.append(1)
        else:
            data.append(0)

    print("raw bit stream:", data)

    GPIO.cleanup()


read_dht11()
