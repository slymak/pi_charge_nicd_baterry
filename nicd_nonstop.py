#!/usr/bin/python3 -u
from ina219 import INA219
#from ina219 import DeviceRangeError
import time
import datetime
import logging
logging.basicConfig(format='%(asctime)s - %(message)s',filename='/home/sklep/digivolt/logs/log_nicd_tester.log')
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
#editable  valus -- battery setting is below while
num_period = 3		#how many times charge and discharge
waiting = 60			# delay interval for next measurement

import RPi.GPIO as GPIO
pinrele1 = 16           #vout
pinrele3 = 13           #bat1
pinrele2 = 20           #bat2 mala bila
pinrele4 = 21           #vin

#reley
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


def read_ina():
    ina3221.enable_channel(1)
    ina3221.enable_channel(2)
    ina3221.enable_channel(3)

    vin = float("{:.2f}".format(ina3221.bus_voltage(1)))
    ain = float("{:.2f}".format(ina3221.current(1) * 1000))
    vbat1 = float("{:.2f}".format(ina3221.bus_voltage(2)))
    vbat2 = float("{:.2f}".format(ina3221.bus_voltage(3)))

    ina2 = INA219(0.1, 3, address=0x44)
    ina2.configure()
    time.sleep(1)

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
    print(f"----vbat1 bat_down {vbat1} vbat2 bat_top {vbat2} vin: {vin} vout: {vout} ain: {ain} aout: {aout}")

    #collect reley status
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
    #print(f"   RELE bat1 {rbat1} bat2 {rbat2} in {rin} out {rout}")

    #grid check
    if battery == "bat_top":
        vbat = vbat2
    elif battery == "bat_down":
        vbat = vbat1
    if vin < vbat:      #dojde stava
        grid_on = False
        grid_off = True
#        print(f"grid NENI  off ma {grid_off} on ma {grid_on}")
    else:
        grid_on = True
        grid_off = False
#        print(f"grid off ma {grid_off} on ma {grid_on}")


    ina = dict()
    ina['vout'] = vout
    ina['vin'] = vin
    ina['vbat'] = vbat
    ina['vbat1'] = vbat1
    ina['vbat2'] = vbat2
    ina['aout'] = aout
    ina['ain'] = ain
    ina['grid_on'] = grid_on
    ina['grid_off'] = grid_off
    return ina

######################################
def charging(battery, pinrelebat, pinrelebat2, maxvbat):
    start_charg = time.time()
    GPIO.output(pinrele1, GPIO.HIGH)
    GPIO.output(pinrelebat, GPIO.LOW)
    GPIO.output(pinrelebat2, GPIO.HIGH)
    GPIO.output(pinrele4, GPIO.LOW)

    read_ina()
    ina = read_ina()
    xcycle = 1
    x = [1]
    y = [ina['vbat']]

    #loop till
    while ina['vbat'] < maxvbat  and ina['vin'] > ina['vbat']:
        read_ina()
        ina = read_ina()

        print(f"CHARGING {xcycle} {battery} Vbat = {ina['vbat']}, Vin = {ina['vin']}  maxvbat je {maxvbat} vbat1 je {ina['vbat1']} vbat2 je {ina['vbat2']}")
        xcycle += 1
        x.append(xcycle)
        y.append(ina['vbat'])
        time.sleep(waiting)

    #creating plot
    dt = datetime.datetime.now()
    datum = dt.strftime("%y%m%d-%H:%M")
    end_charg = (start_charg - time.time())/60
    logging.warning(f" battery {battery} charged in {end_charg} minutes took {xcycle} period")
    plt.plot(x,y)
    plt.xlabel(f"time period {waiting} sec")
    plt.ylabel('voltage')
    plt.title(f"charging battery {battery} took {xcycle} period")
    plt.savefig(f"/home/sklep/digivolt/graphs/charge_{battery}_{datum}.png")
    plt.clf()
    print (*x)
    print (*y)
    x = []
    y = []

    GPIO.output(pinrelebat, GPIO.HIGH)
    GPIO.output(pinrelebat2, GPIO.LOW)
    GPIO.output(pinrele4, GPIO.HIGH)
    GPIO.output(pinrele1, GPIO.HIGH)

#------------ main ------------------
try:
    cycle = 1
    while cycle < num_period:
        battery = "bat_down"
        read_ina()
        ina = read_ina()
        print(f"{cycle} CYCLE begining vin {ina['vin']} vbat1 {ina['vbat1']} vbat2 {ina['vbat2']}")

#grid is on ----------------------
        while ina['grid_on'] and cycle < num_period:
            if ina['grid_off'] == True:
                break
            if (cycle % 2) == 0:
# -------------- editing fields -----------------------
                # bat_down battery
                battery = "bat_down"
                maxvbat = 16.8
                pinrelebat = pinrele3
                pinrelebat2 = pinrele2
            else:
                # bat_top battery
                battery = "bat_top"
                maxvbat = 16.8
                pinrelebat = pinrele2
                pinrelebat2 = pinrele3
# -------------- editing fields -----------------------

            # charging ---------------------------------
            charging(battery, pinrelebat, pinrelebat2, maxvbat)

            read_ina()
            ina = read_ina()
            if ina['grid_off'] == True:
                break
            time.sleep(4)

            cycle += 1
            print(cycle)
            time.sleep(2)
# grid off waiting for grid
        while ina['grid_off']:
            print(f"         no input grid ")
            time.sleep(11)

            read_ina()
            ina = read_ina()
            time.sleep(4)
            if ina['grid_off'] == True:
                break


except KeyboardInterrupt:
    print("intentionaly interrupted ")
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
    print(f" cycle = {cycle} reached num_period = {num_period} charging / discharging period ")

