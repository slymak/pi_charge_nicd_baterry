#!/usr/bin/python3
from ina219 import INA219
from ina219 import DeviceRangeError
from time import sleep
SHUNT_OHMS = 0.1

def inabat():
  ina2 = INA219(SHUNT_OHMS,3, address=0x44)
  ina2.configure()

  v= ina2.voltage()
  print("---ina2: ", v)
  print("---Curr: ", ina2.current())
  print("---Power: ", ina2.power())

#now is there ina3221
def read_ina():
    ina = INA219(SHUNT_OHMS)
    ina.configure()

    print("Voltage: ", ina.voltage())
    try:
        print("Current: ", ina.current())
        print("Power: ", ina.power())
    except DeviceRangeError as e:
        # Current out of device range with specified shunt resistor
        print(e)


#for x in range(14):
#read_ina()
inabat()
#	sleep(2)
