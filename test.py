#!/usr/bin/python3
from ina219 import INA219
#from ina219 import DeviceRangeError
import time
import datetime
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='logall.log')
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

import matplotlib.pyplot as plt

grid_on = True
grid_off = False
SHUNT_OHMS = 0.1


import RPi.GPIO as GPIO
pinrele1 = 16           #vout
pinrele3 = 13           #bat1
pinrele2 = 20           #bat2 mala bila
pinrele4 = 21           #vin
pinregulv= 12
pinred = 26
pinwhite = 19

#rele
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinrele1, GPIO.OUT)
GPIO.output(pinrele1, GPIO.HIGH)
GPIO.setup(pinrele2, GPIO.OUT)
GPIO.output(pinrele2, GPIO.HIGH)
GPIO.setup(pinrele3, GPIO.OUT)
GPIO.output(pinrele3, GPIO.HIGH)
GPIO.setup(pinrele4, GPIO.OUT)
GPIO.output(pinrele4, GPIO.HIGH)
# PWM regulace
GPIO.setup(pinregulv, GPIO.OUT)
regulacev = GPIO.PWM(pinregulv,9000)
#LEDky
GPIO.setup(pinred, GPIO.OUT)
redpwm = GPIO.PWM(pinred, 60)
redpwm.start(0)
GPIO.setup(pinwhite, GPIO.OUT)
whitepwm = GPIO.PWM(pinwhite, 60)


def read_ina():
    ina3221.enable_channel(1)
    ina3221.enable_channel(2)
    ina3221.enable_channel(3)

    vin = float("{:.2f}".format(ina3221.bus_voltage(1)))
    ain = float("{:.2f}".format(ina3221.current(1) * 1000)) 
    vbat1 = float("{:.2f}".format(ina3221.bus_voltage(2)))
    vbat2 = float("{:.2f}".format(ina3221.bus_voltage(3)))

    ina2 = INA219(SHUNT_OHMS,3, address=0x44)
    ina2.configure()
    
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
    print(f"----vbat1 dole {vbat1} vbat2 bila {vbat2} vin: {vin} vout: {vout} ain: {ain} aout: {aout}")
    
    status = GPIO.input(pinrele3)
    if status:
        rbat1 = 0
    else:
        rbat1 = 1
    status = GPIO.input(pinrele2)
    if status:
        rbat2 = 0
    else:
        rbat2 = 1
    status = GPIO.input(pinrele1)
    if status:
        rout = 0
    else:
        rout = 1
    status = GPIO.input(pinrele4)
    if status:
        rin = 0
    else:
        rin = 1
    print(f"   RELE bat1 {rbat1} bat2 {rbat2} in {rin} out {rout}")

    ina = dict()
    ina['vout'] = vout
    ina['vin'] = vin
    ina['vbat1'] = vbat1
    ina['vbat2'] = vbat2
    ina['aout'] = aout
    ina['ain'] = ain
    return ina
   
###############################
def grid_check():
    read_ina()
    ina = read_ina()
    if 'baterry' in locals():
        if baterry == "horni":
            vbat = ina['vbat2']
        elif baterry  == "dolni":
            vbat = ina['vbat1']
    else: vbat = ina['vbat1']
        

    if ina['vin'] < vbat:      #dojde stava
        grid_on = False
        grid_off = True
        print(f"grid NENI  off ma {grid_off} on ma {grid_on}")
    else:
        grid_on = True
        grid_off = False
        print(f"grid off ma {grid_off} on ma {grid_on}")

    grid = dict()
    grid['grid_on'] = grid_on
    grid['grid_off'] = grid_off
    return grid
    


try:
    cycle = 1
    while True:    
        read_ina()
        time.sleep(11)
        print("11sec ")
#        grid_check()
#        grid = grid_check()
 #       print(f" {cycle}    zaciname vin {ina['vin']} vbat1 {ina['vbat1']} vbat2 {ina['vbat2']}")


except KeyboardInterrupt:
    print("intentionaly interrupted ")
    regulacev.stop()
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pinrele4, GPIO.OUT)
    GPIO.output(pinrele4, GPIO.HIGH)
    GPIO.setup(pinrele2, GPIO.OUT)
    GPIO.output(pinrele2, GPIO.LOW)
    GPIO.setup(pinrele3, GPIO.OUT)
    GPIO.output(pinrele3, GPIO.HIGH)
    GPIO.setup(pinrele1, GPIO.OUT)
    GPIO.output(pinrele1, GPIO.HIGH)

else:
    print("KDE JSEM out ot try", vin)

