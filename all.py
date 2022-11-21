#!/usr/bin/python3
from ina219 import INA219
from ina219 import DeviceRangeError
import time
from board import SCL, SDA
import busio
from oled_text import OledText
i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 64)

global cycle
grid_on = True
grid_off = False
SHUNT_OHMS = 0.1


import RPi.GPIO as GPIO
pinrele1 = 16
global pinrele4
pinrele4 = 21
pinregulv= 12
pinred = 26
pinwhite = 19

#rele
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinrele1, GPIO.OUT)
GPIO.output(pinrele1, GPIO.HIGH)
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
    global ain
    global vin
    global vbat1
    inain = INA219(SHUNT_OHMS)
    inain.configure()
    ina2 = INA219(SHUNT_OHMS,3, address=0x44)
    ina2.configure()
    vin= inain.voltage()
    vinoled = 'vin: ',vin
    oled.text(vinoled, 1)
    print("ina vin ", vin)
    vbat1 = ina2.voltage()
    vbat1oled = 'vbat1 ',vbat1
    oled.text(vbat1oled, 2)
    print("ina bat1: ", vbat1)
    ain= inain.current()
    ainoled = "ain: ", ain
    oled.text(ainoled, 3)
    print("ina ain: ", ain)


def charging(status, cycle):
    print("rele_in ON", cycle)
    regulacev.start(0)
    GPIO.output(pinrele4, GPIO.LOW)

    while vbat1 <10.3:
        read_ina()
        print("nabijim opakuje", cycle, vin, vbat1)
        if vin < 10.1:
            status = False
            print("nabijim a dosla stava", type(vin))
            break 
        else:    
            time.sleep(5)
            cycle +=1
            time.sleep(4)
            if ain < 200:
                vykon = 100
                regulacev.ChangeDutyCycle(vykon)
                print("regulacev is: ", vykon)
                redpwm.ChangeFrequency(vykon/100)
                time.sleep(32)
            elif ain > 200:    
                vykon = 40
                regulacev.ChangeDutyCycle(vykon)
                print("regulacev is ", vykon)
                redpwm.ChangeFrequency(vykon/100)
                time.sleep(22)


    status = False

def discharging(status, cycle):
    print("rele_bat ON", cycle)
    GPIO.output(pinrele1, GPIO.LOW)
    while vbat1 > 8.1:
        read_ina()
        print("vybijim", vin, cycle)
        time.sleep(5)

    status = False
    print("rele_bat OFF", cycle)


def grid_check():
    if vin < 10:
        global grid_on
        global grid_off
        grid_on = False
        grid_off = True
        print("grid je off on", grid_off, grid_on)
        # global vin
        # vin = 5
        # if vin <12:
        #     status = False
        #     print("break rele_in OFF", cycle, vbat1, vin)
        #     global grid_on
        #     global grid_off
        #     grid_on = False
        #     grid_off = True
        #     break



try:
    read_ina()
    
    grid_check()
    while grid_on:
        print("sit jede vin vbat", vin, vbat1)
        grid_check()
        time.sleep(1)
        if vbat1 < 10:
            charging(True, 1)


            print("sit jeste nema senzor, vstupni je ", vin)
            GPIO.output(pinrele4, GPIO.HIGH)
            time.sleep(1)
            cycle = 1
        else:
            discharging(True, 1)
            print("vybito", cycle)
            GPIO.output(pinrele1, GPIO.HIGH)


    while grid_off:
        print("neni stava", vin)
        time.sleep(2)
        print("overujeme stavu", vin)
        time.sleep(2)
        print("rele_230 ON", vin)
        time.sleep(2)
        print("rele_dcac ON", vin)
        print("rele_bat ON", vin)
        time.sleep(2)
        grid_off = False


except KeyboardInterrupt:
    regulacev.stop()
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.output(pinrele4, GPIO.HIGH)     
    print("tohle je vyjimka", vin)


print("KDE JSEM", vin)
