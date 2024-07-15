import time
import datetime
import RPi.GPIO as GPIO
import logging


class pi:
    def __init__(self):
        self.openPin = 17
        self.keyPin = 27

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.openPin, GPIO.OUT)
        GPIO.setup(self.keyPin, GPIO.IN)
        GPIO.output(self.openPin, False)

    def doorOpen(self):
        logging.debug(f"{datetime.datetime.now()} - Open Door")
        GPIO.output(self.openPin, True)
        time.sleep(1)
        GPIO.output(self.openPin, False)
