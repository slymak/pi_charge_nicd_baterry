#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 13	#bat1
in2 = 20	#bat2
in3 = 16	#vou
in4 = 21	#vin

GPIO.setmode(GPIO.BCM)
#GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
#GPIO.setup(in3, GPIO.OUT)
#GPIO.setup(in4, GPIO.OUT)

#switch ON
#GPIO.output(in1, GPIO.LOW)
#GPIO.output(in2, GPIO.LOW)
#GPIO.output(in3, GPIO.LOW)
#GPIO.output(in4, GPIO.LOW)
#switch OFF 
#GPIO.output(in1, GPIO.HIGH)
GPIO.output(in2, GPIO.HIGH)
#GPIO.output(in3, GPIO.HIGH)
#GPIO.output(in4, GPIO.HIGH)

GPIO.cleanup()
