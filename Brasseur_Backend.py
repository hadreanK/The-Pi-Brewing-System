#Brasseur backend does the following things:
# 1. gets the current temperatures from the thermometers and writes them to a file

import DS18B20_Module_Class_AK
import time

intentionally_raise_error = False
tempDiffThreshold = 15.0
numSkipped = 0
countEr = 0  #Barely know 'er
total_num_temps = 0
prevTemps = [] #An array of 3 previous temperature readings to detect faulty measurements with 
numErrors = 0

while(True):
    myTemps = DS18B20_Module_Class_AK.DS18B20()
    myTemps.findDevices()

    print(str(myTemps.nThermometers) + " thermometers were found")

    # Get the initial temperatures and save them to prevTemps
    myTemps.getAllTemps()
    myTemps.roundTemps(1)
    prevTemps = [myTemps.tempF, myTemps.tempF, myTemps.tempF]

    print("Initial temperatures are (in F):")
    print(myTemps.tempF)
    myTemps.writeTempsFile()

    print("Starting Loop")
    while True:
        myTemps.getAllTemps()
        myTemps.roundTemps(1)
        recordTemps = True

        for i in range(0,myTemps.nThermometers): # For each thermometer
            for j in range(0,3): # For each temperature saved
                # If there's not a huge change in temperature, then save them 
                #print("i = " + str(i) + ",   j = " + str(j))
                if (abs(prevTemps[j][i]-myTemps.tempF[i]) > tempDiffThreshold):
                    print("Large change in temperature")
                    print(prevTemps[i][j])
                    print(myTemps.tempF[i*2])
                    recordTemps = False
                    numSkipped = numSkipped+1

        if(recordTemps or (numSkipped>3)):
            myTemps.writeTempsFile()
            print("Recorded: " + str(prevTemps) + 
                " - " + str(total_num_temps))
            for i in range(0,myTemps.nThermometers):                 
                prevTemps[countEr][i] = myTemps.tempF[i]
            countEr = (countEr+1)%3
            numSkipped = 0
            
        else:
            print("Not Recorded:" & str(myTemps.tempF))
        total_num_temps += 1

        if intentionally_raise_error:
            raise(ValueError("intentional error to check"))
