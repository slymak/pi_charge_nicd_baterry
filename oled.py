#!/usr/bin/python3
from board import SCL, SDA
import busio
from oled_text import OledText

i2c = busio.I2C(SCL, SDA)
oled = OledText(i2c, 128, 32)

oled.text(" slymak", 1)
oled.text(" ma display ", 2)
