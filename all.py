#re!/usr/bin/python3
from ina219 import INA219
from ina219 import DeviceRangeError
from time import sleep
SHUNT_OHMS = 0.1


import RPi.GPIO as GPIO
pinrele1 = 16
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
regulacev = GPIO.PWM(pinregulv,2000)
#LEDky
GPIO.setup(pinred, GPIO.OUT)
redpwm = GPIO.PWM(pinred, 60)
#redpwm.start(0)
GPIO.setup(pinwhite, GPIO.OUT)
whitepwm = GPIO.PWM(pinwhite, 60)


# ina1 is behind power
# ina2 is behind battery
def read_ina():
  global a1
  global v1
  global v2
  ina1 = INA219(SHUNT_OHMS)
  ina1.configure()
  ina2 = INA219(SHUNT_OHMS,3, address=0x44)
  ina2.configure()
  v1= ina1.voltage()
  print("ina v1 ", v1)
  a1= ina1.current()
  print("ina a1: ", a1)
  v2 = ina2.voltage()
  
#pinrele4 switch power to regulator
def rele2power():
    regulacev.start(0)
    GPIO.output(pinrele4, GPIO.LOW)
    sleep(4)
    if a1 < 400:
        vykon = 100
        regulacev.ChangeDutyCycle(vykon)
        print("regulacev is: ", vykon)
        whitepwm.ChangeDutyCycle(vykon)
        sleep(12)
    elif a1 > 500:    
        vykon = 40
        regulacev.ChangeDutyCycle(vykon)
        print("regulacev is ", vykon)
        whitepwm.ChangeDutyCycle(vykon)
        sleep(22)
    else:
        GPIO.output(pinrele4, GPIO.HIGH)

#pinrele1 switch batttery to bulb
def rele2bat():
    GPIO.output(pinrele1, GPIO.LOW)
    while True:
        sleep(9)
        read_ina()
        print("discharging: ", v2 )
        if v2 < 8.7:
            GPIO.output(pinrele1, GPIO.HIGH)
        break
        



try:
  read_ina()
    
  while v2 > 1.0:
    read_ina()
    sleep(2)
    if v2 > 11:
        rele2bat()
    else:
      print("baterka ma: ", v2 )
      rele2power()
    
      


except KeyboardInterrupt:
    regulacev.stop()
    GPIO.cleanup()
 