#!/usr/bin/python3
from board import SCL, SDA
import busio
from oled_text import OledText


import time
import sys
import board
from barbudor_ina3221.lite import INA3221
i2c_bus = board.I2C()
ina3221 = INA3221(i2c_bus)


i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 64)

ina3221.enable_channel(1)
ina3221.enable_channel(2)
ina3221.enable_channel(3)

vin = ina3221.bus_voltage(1)
ain = ina3221.current(1)

bat1 = ina3221.bus_voltage(2)
bat2 = ina3221.bus_voltage(3)

#
grid =  "in",(vin),"V ",(ain),"A "
line_current =       " {:6.5f} A ".format(ain)
bat1dis = "bat1 ",bat1
bat2dis = "bat2 ",bat2

print(grid)
print(line_current)
print(bat1dis)
print(bat2dis)

oled.text(grid, 1)
oled.text(bat1dis, 2)
oled.text(bat2dis, 3)
