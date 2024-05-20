import time
import RPi.GPIO as GPIO


class pi:
    def __init__(self):
        self.openPin = 17

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.openPin, GPIO.OUT)
        GPIO.output(self.openPin, False)

    def doorOpen(self):
        GPIO.output(self.openPin, True)
        time.sleep(1)
        GPIO.output(self.openPin, False)
