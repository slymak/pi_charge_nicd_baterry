
#!/usr/bin/python3
import time
vin = 16
vbat1 = 14
global cycle
grid_on = True
grid_off = False

def charging(status, cycle):
    global vbat1
    print("rele_in ON", cycle)
    while vbat1 <15:
        print("nabijim opakuje", cycle)
        time.sleep(1)
        cycle +=1
        if cycle == 4:
            vbat1 = 16
            # print("rele_in OFF", cycle, vbat1)

    status = False
    print("else rele_in OFF", cycle, vbat1)

def discharging(status, cycle):
    global vbat1
    print("rele_bat ON", cycle)
    while vbat1 > 12:
        print("vybijim", vin, cycle)
        time.sleep(2)
        cycle +=1
        if cycle == 4:
            # status = False
            vbat1 = 10
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
    grid_check()
    while grid_on:
        print("sit jede vin vbat", vin, vbat1)
        grid_check()
        time.sleep(1)
        if vbat1 < 15:
            charging(True, 1)


            print("sit jeste nema senzor, vstupni je ", vin)
            time.sleep(1)
            cycle = 1
        else:
            discharging(True, 1)
            print("vybito", cycle)


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


except:
    print("tohle je vyjimka", vin)


print("KDE JSEM", vin)
