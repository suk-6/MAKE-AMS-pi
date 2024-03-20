import RPi.GPIO as GPIO
import time


class pi:
    def __init__(self):
        self.openPin = 17
        self.buttonPin = 27

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.openPin, GPIO.OUT)
        GPIO.setup(self.buttonPin, GPIO.IN)
        GPIO.output(self.openPin, False)

        self.tmp = []
        self.conf = 100
        self.correct = [1 for i in range(self.conf)]

    def __call__(self):
        self.tmp.append(GPIO.input(self.buttonPin))
        try:
            if self.tmp == self.correct:
                GPIO.output(self.openPin, True)
                time.sleep(0.3)
                GPIO.output(self.openPin, False)
        except:
            pass

        if len(self.tmp) > self.conf:
            del self.tmp
            self.tmp = []
