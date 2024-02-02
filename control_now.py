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
pinrelebatbottom = 16           #batbottom
pinrelebattop = 20           #battop 13
pinrelebatdown = 13           #battdown  20
pinrelevin = 21           #vin 230v

#reley
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinrelebatbottom, GPIO.OUT)
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
vbatbottom = float("{:.2f}".format(ina2.voltage()))
batbottomoled = 'bottom ',vbatbottom
oled.text(batbottomoled, 4)
aout = float("{:.2f}".format(ina2.current()))
oled.text(dt, 5)
print(f"vbatdown {vbatdown} vbattop {vbattop} vin: {vin} vbatbottom: {vbatbottom} ain: {ain} aout: {aout}")


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
#    print(f"{dt}   batdown on {batdown_on} _off {batdown_off} ")
else:
    batdown_on = True
    batdown_off = False

statusbattop = GPIO.input(pinrelebattop)
if statusbattop:
    battop_on = False
    battop_off = True
#    print(f"{dt}   battop on {battop_on} _off {battop_off} ")
else:
    battop_on = True
    battop_off = False

statusbatbottom = GPIO.input(pinrelebatbottom)
if statusbatbottom:
    batbottom_on = False
    batbottom_off = True
#    print(f"{dt} on vbatbottom on {batbottom_on} real {vbatbottom} baterka  {vbattop}")
else:
    batbottom_on = True
    batbottom_off = False

#---------------- main -------------------------
maxvdown = 11
minvdown = 0.1

maxvtop = 14.6
minvtop = 0.1

maxvbottom = 15.2
minvbottom = 0.3

################# reley operation ##############################################
# switch on top
if battop_off == True and vbattop < minvtop:
     GPIO.output(pinrelebattop, GPIO.LOW)
     print(f"{dt} ZAPINAM 1 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" ZAPINAM 1 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
# switch off bottom
if battop_on == True and vbattop > maxvtop:
     GPIO.output(pinrelebattop, GPIO.HIGH)
     print(f"{dt} VYPINAM 1 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" VYPINAM 1 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")

# switch on down
if batdown_off == True and vbatdown < minvdown:
     GPIO.output(pinrelebatdown, GPIO.LOW)
     print(f"{dt} ZAPINAM 2 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" ZAPINAM 2 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
# switch off down
if batdown_on == True and vbatdown > maxvdown:
     GPIO.output(pinrelebatdown, GPIO.HIGH)
     print(f"{dt} VYPINAM 2 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" VYPINAM 2 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")

# switch on bottom
if batbottom_off == True and vbatbottom < minvbottom:
     GPIO.output(pinrelebatbottom, GPIO.LOW)
     print(f"{dt} ZAPINAM 3 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" ZAPINAM 3 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
# switch off bottom
if batbottom_on == True and vbatbottom > maxvbottom:
     GPIO.output(pinrelebatbottom, GPIO.HIGH)
     print(f"{dt} VYPINAM 3 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
     logging.warning(f" VYPINAM 3 vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")


# swith off power in
#if vin_on == True and (vbattop > maxvtop or vbatdown > maxvdown or vbatbottom > maxvbottom):
#     GPIO.output(pinrelevin, GPIO.HIGH)
#     print(f"{dt} VYPINAM vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
#    logging.warning(f" VYPINAM vin {vin},vbattop {vbattop}, maxvdown {maxvdown}, vbatbottom: {vbatbottom}")
