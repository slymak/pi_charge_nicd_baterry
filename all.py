#!/usr/bin/python3
from ina219 import INA219
#from ina219 import DeviceRangeError
import time
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
    global vout
    global aout
    global vin
    global ain
    global vbat1
    global vbat2
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
    print("----vbat1 dole",vbat1, "vbat2 bila",vbat2)
    vout = float("{:.2f}".format(ina2.voltage()))
    voutoled = 'vout ',vout
    oled.text(voutoled, 4)
    aout = float("{:.2f}".format(ina2.current()))
    aoutoled = "aout: ", aout
    oled.text(aoutoled, 5)
    print(f"   ina vin: {vin} vout: {vout} ain: {ain} aout: {aout}")    
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
    print(f"   rele bat1-2 || {rbat1} {rbat2} in out {rin} {rout}")

def charging():
    cycle = 1
    start_charg = time.time()
    regulacev.start(0)
    GPIO.output(pinrele4, GPIO.LOW)
    GPIO.output(pinrele3, GPIO.LOW)
    print("_rele_in ON rele_bat1 ON", cycle)
    read_ina()
    while vbat1 <12.3 and int(vin) > int(vbat1):
        read_ina()
        print("1N in while nabijim opakuje", cycle, vin, vbat1)
        time.sleep(5)
        cycle +=1
        time.sleep(4)
        if ain < 430:
            vykon = 100
            regulacev.ChangeDutyCycle(vykon)
            print("regulacev is: ", vykon)
            redpwm.ChangeFrequency(vykon/100)
            time.sleep(32)
        else:
            vykon = 40
            regulacev.ChangeDutyCycle(vykon)
            print("regulacev is ", vykon)
            redpwm.ChangeFrequency(vykon/100)
            time.sleep(22)

    end_charg = (start_charg - time.time())/60
    logg = "suma minutpro bat1", end_charg
    logging.warning(logg)
    print("konec nabiti bat1 je v: ", end_charg)
    GPIO.output(pinrele4, GPIO.HIGH)
    GPIO.output(pinrele3, GPIO.HIGH)
    GPIO.output(pinrele2, GPIO.LOW)
    

def discharging():
    start_discharg = time.time()
    GPIO.output(pinrele3, GPIO.HIGH)
    GPIO.output(pinrele2, GPIO.LOW)
    GPIO.output(pinrele1, GPIO.LOW)
    print(f"_rele_out and bat2 ON bat1 OFF")
    
    read_ina()
    while vbat1 > 10.5 and int(vin) > int(vbat1):                
        read_ina()
        print("1VV vybijim bat1", vout, aout, vbat1, cycle)
        time.sleep(15)

    
    end_discharg = (start_discharg - time.time())/60    
    logg = "suma minut vybiti pro bat1", end_discharg
    logging.warning(logg)
    print("konec vybiti bat1 je v: ", end_discharg)
    GPIO.output(pinrele1, GPIO.HIGH)
    
    
######################################
def charging2():
    start_charg = time.time()
    regulacev.start(0)
    GPIO.output(pinrele4, GPIO.LOW)
    GPIO.output(pinrele2, GPIO.LOW)
    print("_rele_in, bat2 ON", cycle)
    
    while vbat2 <13.9  and int(vin) > int(vbat1):
        read_ina()
        print(f"nabijim2 opakuje {cycle} {vin} {vout} {vbat2}")
        if ain < 230:
            vykon = 100
            regulacev.ChangeDutyCycle(vykon)
            print("regulacev is: ", vykon)
            redpwm.ChangeFrequency(vykon/100)
            time.sleep(12)
        else:
            vykon = 20
            regulacev.ChangeDutyCycle(vykon)
            print("regulacev is ", vykon)
            redpwm.ChangeFrequency(vykon/100)
            time.sleep(12)

    end_charg = (start_charg - time.time())/60
    logg = "bat2 nabiti", end_charg
    logging.warning(logg)
    status = False
    print("2NN konec nabiti bat2 je v: ", end_charg)
    GPIO.output(pinrele2, GPIO.HIGH)
    GPIO.output(pinrele4, GPIO.HIGH)
    GPIO.output(pinrele3, GPIO.LOW)


def discharging2():
    start_discharg = time.time()
    GPIO.output(pinrele1, GPIO.LOW)
    GPIO.output(pinrele3, GPIO.LOW)
    GPIO.output(pinrele2, GPIO.HIGH)
    GPIO.output(pinrele4, GPIO.HIGH)
    print("_rele_out bat1 ON, vin,bat2 OFF ", cycle)

    while vbat2 > 9.2  and int(vin) > int(vbat1):                
        read_ina()
        print("2VV vybijim bat2", vin, vbat2, cycle)
        time.sleep(3)
        
    end_discharg = (start_discharg - time.time())/60    
    logg = "bat2 vybiti", end_discharg
    logging.warning(logg)
    GPIO.output(pinrele1, GPIO.HIGH)
    print("konec vybiti bat2 je v: ", end_discharg)

###############################
def grid_check():
    read_ina()
    global grid_on
    global grid_off
    if int(vin) <= int(vbat1):      #dojde stava
        grid_on = False
        grid_off = True
        print("grid je na tom takle", grid_off, grid_on)
    else:
        grid_on = True
        grid_off = False
        print("grid kontrola je stava", grid_off, grid_on)


try:
    read_ina()
    grid_check()
    cycle = 1
    
    while grid_on:
        print("sit jede vin vbat1", vin, vbat1)
        grid_check()
        time.sleep(1)
## cycle baterry 2
        charging2()
        grid_check()
        print("2N konci nabijeni2, vin ", vin, vbat1, vbat2, vout)

        discharging2()
        grid_check()
        print("2V vybito2 vin", vin, vbat1, vbat2, vout)
## cycle baterrry 1
        charging()
        print("1N konci nabito, vin ", vin, vbat1, vbat2, vout)
        grid_check()
        print(f"1N uplne na konci gridy jsou {grid_on}  a OFF ma {grid_off}") 

        discharging()
        print("1V konci vybito vin ", vin, vbat1, vbat2, vout)
        grid_check()
        print(f"1V uplne na konci gridy jsou {grid_on}  a OFF ma {grid_off}") 

    while grid_off:
        print(f"neni stava", vin)
        time.sleep(1)
        print("overujeme stavu", vin)
        time.sleep(1)
        print("rele_230 ON", vin)
        time.sleep(1)
        print("rele_dcac ON", vin)
        print("rele_bat ON", vin)
        time.sleep(1)
        grid_off = False


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


