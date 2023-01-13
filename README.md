nicd_tester.py is controlling (charge / discharge) independently two NiCd batteries (10 cels 140 Ah each) from Ferak type KPH.

Settings has two areas and allow set up: 

num_period - how many period charge and discharge

waiting - delay interval for next measurement 

in main section:

maxvbat - voltage where charging stop

minvbat - voltage where discharging stop 

A plot is created for each process and into the log is written duration.

# compounds

raspberry pi

INA209

INA3221

oled display i2c 128x64

4x relay board

PWM controller to lower power (used only by testing small batteries)





