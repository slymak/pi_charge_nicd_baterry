#!/usr/bin/python3 -u
import time
from datetime import datetime
import matplotlib.pyplot as plt
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='/home/sklep/digivoltjuta/logs/controlpin')

# DISPLAY settings
from board import SCL, SDA
import busio
from oled_text import OledText
i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 64)

import sys
import board
from barbudor_ina3221.lite import INA3221
i2c_bus = board.I2C()
ina3221 = INA3221(i2c_bus)


import RPi.GPIO as GPIO
pinrelevout = 16           #vout
pinrelebat1 = 13           #bat1 h4 bulb 4A
pinrelebat2 = 20           #not use
pinrelevin = 25           #vin 230v

############ using values from wetter.py
# batf = open("/home/sklep/digivoltjuta/vbat2_value","r")
# vbat2_value = float(batf.read())
# batf.close()

#reley
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinrelevout, GPIO.OUT)
GPIO.setup(pinrelebat1, GPIO.OUT)
GPIO.setup(pinrelebat2, GPIO.OUT)
GPIO.setup(pinrelevin, GPIO.OUT)


# def read_ina():
ina3221.enable_channel(1)
ina3221.enable_channel(2)
ina3221.enable_channel(3)

vin = float("{:.2f}".format(ina3221.bus_voltage(1)))
vout = float("{:.2f}".format(ina3221.bus_voltage(2)))
vbat2 = float("{:.2f}".format(ina3221.bus_voltage(3)))

time.sleep(1)
dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')


statusvin = GPIO.input(pinrelevin)
if statusvin:
    vin_on = True
    vin_off = False
else:
    vin_on = False
    vin_off = True
    print(f"{dt}  vin_off {vin_off} ")

statusbat1 = GPIO.input(pinrelebat1)
if statusbat1:
    bat1_on = False
    bat1_off = True
    print(f"{dt}   bat1 ma on {bat1_on} _off {bat1_off} ")
else:
    bat1_on = True
    bat1_off = False

statusbat2 = GPIO.input(pinrelebat2)
if statusbat2:
    bat2_on = False
    bat2_off = True
    print(f"{dt}   bat1 ma on {bat2_on} _off {bat2_off} ")
else:
    bat2_on = True
    bat2_off = False

statusvout = GPIO.input(pinrelevout)
if statusvout:
    vout_on = True
    vout_off = False
else:
    vout_on = True
    vout_off = False
    print(f"{dt} vout on {vout_on} volty set {vout_value} real {vout} baterka set {vbat2_value} real {vbat2}")

#---------------- main -------------------------


################# vin on ##############################################

# if vin_on == True and vout > vbat2 and vout > vout_value:
#     # GPIO.output(pinrelevin, GPIO.LOW)
#     print(f"{dt} 230V off, prave se sit vypla {vbat2}")
#     logging.warning(f" 230V switch off, vout set {vout_value} real {vout} vbat2 set {vbat2_value} real {vbat2}")
    
# ################# off vin ###############################################


# if vin_on == False and vbat2 < vbat2_value:
#     GPIO.output(pinrelevin, GPIO.HIGH)
#     print(f"{dt} zapiname 230V zacina vin_on")
#     logging.warning(f" vin switch ON now, vout {vout} vbat2 {vbat2}")
