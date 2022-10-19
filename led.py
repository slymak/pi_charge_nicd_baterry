#!/usr/bin/python3
from gpiozero import PWMLED
from gpiozero import LED
from time import sleep
import numpy as np

red = PWMLED(26)
white = LED(19)

for i in reversed(np.arange(0, 1, 0.01)):
 red.value = i
 print(i, end=' ')
 sleep(0.2)
sleep(1)
white.blink()