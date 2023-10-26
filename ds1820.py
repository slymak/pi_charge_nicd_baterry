#!/usr/bin/python3
#pip install w1thermsensor
from datetime import datetime
from w1thermsensor import W1ThermSensor

import re

def remove_bracket_and_comma(string):
  """Removes the bracket and comma from the given string.

  Args:
    string: A string.

  Returns:
    A string without the bracket and comma.
  """

  # Remove the bracket.
  string = re.sub(r'\[|\]', '', string)

  # Remove the comma.
  string = re.sub(r',', ' ', string)

  string = re.sub(r"'", '', string)

  return string

dts = datetime.now()
dt  = dts.strftime('%Y-%m-%d %H:%M')


sensor_data = []
for sensor in W1ThermSensor.get_available_sensors():
  sensor_data.append("%.0f" % (sensor.get_temperature()))

# Print the sensor data with the time
string = remove_bracket_and_comma(f"{dt} {sensor_data}")
print(string)
