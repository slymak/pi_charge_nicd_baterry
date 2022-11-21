#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

red = 26
white = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red,GPIO.OUT)
GPIO.setup(white,GPIO.OUT)


def ledkaon(color):
    print("sviti", color)
    GPIO.output(color,GPIO.HIGH)

def ledkaoff(color):
    print("sviti", color)
    GPIO.output(color,GPIO.LOW)


for x in range(6):
     ledkaon(white)
     ledkaon(red)
     time.sleep(2)
     ledkaoff(red)
     ledkaoff(white)