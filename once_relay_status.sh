#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

batdown = 13
battop = 20
in3 = 16
vin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(batdown, GPIO.OUT)
GPIO.setup(battop, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(vin, GPIO.OUT)


status = GPIO.input(batdown)
if status:
	rbatdown = 0
else:
	rbatdown = 1

status = GPIO.input(battop)
if status:
	rbattop = 0
else:
	rbattop = 1

status = GPIO.input(in3)
if status:
	rout = 0
else:
	rout = 1

status = GPIO.input(vin)
if status:
	rin = 0
else:
	rin = 1

print(f" rbatdown je {rbatdown}, rbattop je {rbattop}, rout je {rout}, rin je {rin} ")
print(f" 1 is off, 0 is on")
#GPIO.output(batdown, GPIO.LOW)
#GPIO.output(battop, GPIO.LOW)
#GPIO.output(in3, GPIO.LOW)
#GPIO.output(vin, GPIO.LOW)
#time.sleep(2)
#GPIO.output(batdown, GPIO.HIGH)
#GPIO.output(battop, GPIO.HIGH)
#GPIO.output(in3, GPIO.HIGH)
#GPIO.output(vin, GPIO.HIGH)

GPIO.cleanup()
