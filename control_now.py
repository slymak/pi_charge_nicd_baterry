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
pinrelebat1 = 13           #bat1 h4 bulb 4A
pinrelebat2 = 20           #not use
pinrelevin = 21           #vin 230v

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
ain = float("{:.2f}".format(ina3221.current(1) * 1000))
vbat1 = float("{:.2f}".format(ina3221.bus_voltage(2)))
vbat2 = float("{:.2f}".format(ina3221.bus_voltage(3)))

ina2 = INA219(0.1, 3, address=0x44)
ina2.configure()

#time.sleep(1)

#display values    
vinoled = 'vin: ',vin
oled.text(vinoled, 1)
vbat1oled = "vbat1 ",vbat1
oled.text(vbat1oled,2)
vbat2oled = "vbat2 ",vbat2
oled.text(vbat2oled,3)
vout = float("{:.2f}".format(ina2.voltage()))
voutoled = 'vout ',vout
oled.text(voutoled, 4)
aout = float("{:.2f}".format(ina2.current()))
aoutoled = "aout: ", aout
oled.text(aoutoled, 5)
print(f"vbat1 bat_down {vbat1} vbat2 bat_top {vbat2} vin: {vin} vout: {vout} ain: {ain} aout: {aout}")



dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')


statusvin = GPIO.input(pinrelevin)
if statusvin:
    vin_on = False
    vin_off = True
    print(f"{dt}  vin_off {vin_off} ")
else:
    vin_on = True
    vin_off = False

statusbat1 = GPIO.input(pinrelebat1)
if statusbat1:
    bat1_on = False
    bat1_off = True
    print(f"{dt}   bat1 on {bat1_on} _off {bat1_off} ")
else:
    bat1_on = True
    bat1_off = False

statusbat2 = GPIO.input(pinrelebat2)
if statusbat2:
    bat2_on = False
    bat2_off = True
    print(f"{dt}   bat2 on {bat2_on} _off {bat2_off} ")
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
    print(f"{dt} vout on {vout_on} real {vout} baterka  {vbat2}")

#---------------- main -------------------------
maxv = 12
minv = 10

################# vin on ##############################################

if vin_on == True and vbat2 > maxv:
     GPIO.output(pinrelevin, GPIO.HIGH)
     print(f"{dt} VYPINAM vin, maxv {maxv} vbat2 {vbat2}")
     logging.warning(f" VYPINAM vin {vin}, vbat2 {vbat2} vbat1 {vbat1}")

# ################# off vin ###############################################


if vin_on == False and vbat2 < minv:
     GPIO.output(pinrelevin, GPIO.LOW)
     print(f"{dt} ZAPINAM vin")
     logging.warning(f" ZAPINAM vin {vin} vbat2 {vbat2}, vbat1 {vbat1}")

