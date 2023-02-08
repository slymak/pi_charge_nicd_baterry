#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 13
in2 = 20
in3 = 16
in4 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)


status = GPIO.input(in1)
if status:
	rbatdown = 0
else:
	rbatdown = 1

status = GPIO.input(in2)
if status:
	rbattop = 0
else:
	rbattop = 1

status = GPIO.input(in3)
if status:
	rout = 0
else:
	rout = 1

status = GPIO.input(in4)
if status:
	rin = 0
else:
	rin = 1

print(f" rbatdown je {rbatdown}, rbattop je {rbattop}, rout je {rout}, rin je {rin} ")
print(f" 1 is off, 0 is on")
#GPIO.output(in1, GPIO.LOW)
#GPIO.output(in2, GPIO.LOW)
#GPIO.output(in3, GPIO.LOW)
#GPIO.output(in4, GPIO.LOW)
#time.sleep(2)
#GPIO.output(in1, GPIO.HIGH)
#GPIO.output(in2, GPIO.HIGH)
#GPIO.output(in3, GPIO.HIGH)
#GPIO.output(in4, GPIO.HIGH)

GPIO.cleanup()
