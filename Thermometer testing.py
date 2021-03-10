#Brasseur backend does the following things:
# 1. gets the current temperatures from the thermometers and writes them to a file

import DS18B20_Module_Class_AK
import time

myTemps = DS18B20_Module_Class_AK.DS18B20()
thermsFound = 0

for i in range(0,100):
    myTemps.findDevices()
    print("Attempt # " + str(i))
    print(str(myTemps.nThermometers) + " thermometers were found")
    try:
        myTemps.getAllTemps()
        print("Thermometers found!")
        thermsFound = thermsFound+1
    except:
        pass
    time.sleep(5)

print(str(thermsFound) + " total thermometers founded")