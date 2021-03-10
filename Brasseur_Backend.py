#Brasseur backend does the following things:
# 1. gets the current temperatures from the thermometers and writes them to a file

import DS18B20_Module_Class_AK
import time

myTemps = DS18B20_Module_Class_AK.DS18B20()
myTemps.findDevices()

tempDiffThreshold = 5.0
numSkipped = 0
countEr = 0  #Barely know 'er
prevTemps = []

print(str(myTemps.nThermometers) + " thermometers were found")

# Get the initial temperatures and save them to prevTemps
myTemps.getAllTemps()
myTemps.roundTemps(1)
print(myTemps.nThermometers)
for i in range(0,myTemps.nThermometers):
    print("found another thermo!")
    prevTemps.append([myTemps.tempF[i], myTemps.tempF[i], myTemps.tempF[i]])

print(prevTemps)

print("Initial temperatures are (in F):")
print(myTemps.tempF)
myTemps.writeTempsFile()

print("Starting Loop")
while True:
    #try:
    if(True):
        myTemps.getAllTemps()
        myTemps.roundTemps(1)
        recordTemps = True
        for i in range(0,2): # For each temperature saved
            for j in range(0,myTemps.nThermometers): # For each thermometer
                # If there's not a huge change in temperature, then save them 
                if(abs(prevTemps[i][j]-myTemps.tempF[i])>tempDiffThreshold):
                    print("problem")
                    print(prevTemps[i][j])
                    print(myTemps.tempF[i*2])
                    recordTemps = False
                    numSkipped = numSkipped+1
        if(recordTemps or (numSkipped>3)):
             myTemps.writeTempsFile()
             print("Recorded: " + str(prevTemps))
             for i in range(0,myTemps.nThermometers):                 
                 prevTemps[i][countEr] = myTemps.tempF[i]
             countEr = (countEr+1)%3
             numSkipped = 0
            
        else:
           print("Not Recorded:" & str(myTemps.tempF))

    #except:
    else:
        print("Something went wrong, not sure what...")
        time.sleep(3)
        myTemps.findDevices()
        time.sleep(2)
