#!/usr/bin/python3
from time import sleep
import RPi.GPIO as GPIO
pinred = 26
pinwhite = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinred, GPIO.OUT)
redpwm = GPIO.PWM(pinred, 60)
GPIO.setup(pinwhite, GPIO.OUT)
#whitepwm = GPIO.PWM(pinwhite, 100)


# LED lighting
dc=0
redpwm.start(dc)

try:
    while True:
        for dc in range(0, 101, 5):
            redpwm.ChangeDutyCycle(dc)
            sleep(0.3)
            print(dc)

except KeyboardInterrupt:
    GPIO.cleanup()
 