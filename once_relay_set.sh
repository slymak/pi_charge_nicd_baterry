#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

batdown = 13	#bat1
battop = 20	#bat2
in3 = 16	#vou
vin = 21	#vin

GPIO.setmode(GPIO.BCM)
GPIO.setup(batdown, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
#GPIO.setup(in3, GPIO.OUT)
#GPIO.setup(vin, GPIO.OUT)

#switch ON
#GPIO.output(batdown, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
#GPIO.output(in3, GPIO.LOW)
#GPIO.output(vin, GPIO.LOW)
#switch OFF 
GPIO.output(batdown, GPIO.HIGH)
#GPIO.output(in2, GPIO.HIGH)
#GPIO.output(in3, GPIO.HIGH)
#GPIO.output(vin, GPIO.HIGH)

#GPIO.cleanup()
