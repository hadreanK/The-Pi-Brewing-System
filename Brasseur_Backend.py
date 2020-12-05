#Brasseur backend does the following things:
# 1. gets the current temperatures from the thermometers and writes them to a file

import DS18B20_Module_Class_AK
import time
print("Preparing program")
myTemps = DS18B20_Module_Class_AK.DS18B20()
myTemps.findDevices()

tempDiffThreshold = 5.0
numSkipped = 0
countEr = 0

print(str(myTemps.nThermometers) + " thermometers were found")
myTemps.getAllTemps()
prevTemps = [[myTemps.tempF[0],myTemps.tempF[0],myTemps.tempF[0]]
             , [myTemps.tempF[1],myTemps.tempF[1],myTemps.tempF[1]]]
print("Initial temperatures are (in F):")
print(myTemps.tempF)
myTemps.writeTempsFile()

print("Starting Loop")
while True:
    try:
        myTemps.getAllTemps()
        recordTemps = True
        for i in range(0,2):
            for j in range(0,3):
                if(abs(prevTemps[i][j]-myTemps.tempF[i*2])>tempDiffThreshold):
                    print("problem")
                    print(prevTemps[i][j])
                    print(myTemps.tempF[i*2])
                    recordTemps = False
                    numSkipped = numSkipped+1
        if(recordTemps or (numSkipped>3)):
             myTemps.writeTempsFile()
             print("Recorded: " + str(prevTemps))
             prevTemps[0][countEr] = myTemps.tempF[0]
             prevTemps[1][countEr] = myTemps.tempF[2]
             countEr = (countEr+1)%3
             numSkipped = 0
#             
#         else:
#            print("Not Recorded:" & str(myTemps.tempF))

    except:
        print("Something went wrong, not sure what...")
        time.sleep(3)
