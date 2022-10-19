#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 16
in2 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
time.sleep(2)
GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.HIGH)

GPIO.cleanup()
