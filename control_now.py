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

#  2 INAs 3221 and 219
import sys
import board
from barbudor_ina3221.lite import INA3221
i2c_bus = board.I2C()
ina3221 = INA3221(i2c_bus)

from ina219 import INA219

# PIN settings
import RPi.GPIO as GPIO
pinrelevout = 16           #vout
pinrelebattop = 20           #battop 13
pinrelebatdown = 13           #battdown  20
pinrelevin = 21           #vin 230v

############ using values from wetter.py
# batf = open("/home/sklep/digivoltjuta/vbattop_value","r")
# vbattop_value = float(batf.read())
# batf.close()

#reley
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinrelevout, GPIO.OUT)
GPIO.setup(pinrelebatdown, GPIO.OUT)
GPIO.setup(pinrelebattop, GPIO.OUT)
GPIO.setup(pinrelevin, GPIO.OUT)


# def read_ina():
ina3221.enable_channel(1)
ina3221.enable_channel(2)
ina3221.enable_channel(3)

vin = float("{:.2f}".format(ina3221.bus_voltage(1)))
ain = float("{:.2f}".format(ina3221.current(1) * 1000))
vbatdown = float("{:.2f}".format(ina3221.bus_voltage(2)))
vbattop = float("{:.2f}".format(ina3221.bus_voltage(3)))

ina2 = INA219(0.1, 3, address=0x44)
ina2.configure()

dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')

#display values    
vinoled = 'vin: ',vin
oled.text(vinoled, 1)
vbatdownoled = "vbatdown ",vbatdown
oled.text(vbatdownoled,2)
vbattopoled = "vbattop ",vbattop
oled.text(vbattopoled,3)
vout = float("{:.2f}".format(ina2.voltage()))
voutoled = 'vout ',vout
oled.text(voutoled, 4)
aout = float("{:.2f}".format(ina2.current()))
oled.text(dt, 5)
print(f"vbatdown {vbatdown} vbattop {vbattop} vin: {vin} vout: {vout} ain: {ain} aout: {aout}")


statusvin = GPIO.input(pinrelevin)
if statusvin:
    vin_on = False
    vin_off = True
    print(f"{dt}  vin_off {vin_off} ")
else:
    vin_on = True
    vin_off = False

statusbatdown = GPIO.input(pinrelebatdown)
if statusbatdown:
    batdown_on = False
    batdown_off = True
    print(f"{dt}   batdown on {batdown_on} _off {batdown_off} ")
else:
    batdown_on = True
    batdown_off = False

statusbattop = GPIO.input(pinrelebattop)
if statusbattop:
    battop_on = False
    battop_off = True
    print(f"{dt}   battop on {battop_on} _off {battop_off} ")
else:
    battop_on = True
    battop_off = False

statusvout = GPIO.input(pinrelevout)
if statusvout:
    vout_on = True
    vout_off = False
else:
    vout_on = True
    vout_off = False
    # print(f"{dt} vout on {vout_on} real {vout} baterka  {vbattop}")

#---------------- main -------------------------
maxv = 14.9
minv = 11

################# vin on ##############################################

if vin_on == True and vbatdown > maxv:
     GPIO.output(pinrelevin, GPIO.HIGH)
     print(f"{dt} VYPINAM vin {vin}, maxv {maxv}, vbatdown {vbatdown} vbattop  {vbattop} vout: {vout}")
     logging.warning(f" VYPINAM vin {vin}, maxv {maxv}, vbatdown {vbatdown} vbattop  {vbattop} vout: {vout}")

# ################# off vin ###############################################


if vin_on == False and vbatdown < minv:
     GPIO.output(pinrelevin, GPIO.LOW)
     print(f"{dt} ZAPINAM vin {vin}, maxv {maxv}, vbatdown {vbatdown} vbattop  {vbattop} vout: {vout}")
     logging.warning(f" ZAPINAM vin {vin}, maxv {maxv}, vbatdown {vbatdown} vbattop  {vbattop} vout: {vout}")
