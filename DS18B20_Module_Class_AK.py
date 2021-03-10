import glob
import time


class DS18B20():
    def __init__(self):
        self.dir = '/sys/bus/w1/devices/'
        self.thermIDs = []
        self.tempsFile = './tempsF.txt'
        self.tempFiles = []
        self.nThermometers = 0
        self.tempF = []
        self.tempC = []
        self.timeStamp = 0
        self.x = "hi"
        self.nextTempToUpdate = 0
        
    def findDevices(self):
        device_folders = glob.glob(self.dir + '28*')
        for folder in device_folders:
            ID = folder.split('/')[-1]
            self.thermIDs.append(ID)
            temp_file = folder + '/temperature'
            self.tempFiles.append(temp_file)
            self.nThermometers = self.nThermometers+1
            self.tempF.append(0.0)
            self.tempC.append(0.0)

    def getAllTemps(self):
        self.tempF = []
        self.tempC = []
        for file in self.tempFiles:
            f = open(file, 'r')
            line = f.readlines()
            f.close()
            temp = float(line[0])
            temp = temp / 1000.0 # Get temp in celcius
            self.tempC.append(temp)
            temp = temp * 9 / 5 + 32
            self.tempF.append(temp)
        self.timeStamp = time.time()
            
    
    def readTempsFile(self):
        '''
        This method reads the most recent temperatures written to
        the temperature file.
        ''' 
        f = open(self.tempsFile, 'r')
        lines = f.readlines()
        f.close()
        i = 0
        for line in lines:
            if(i==0):
                self.timeStamp = float(line)
            else:
                self.tempF[i-1] = float(line)
            i = i + 1
                
    def writeTempsFile(self):
        '''
        This method writes the temps to the file
        '''
        if(self.nThermometers>0):                
            f = open(self.tempsFile, 'w')
            f.write(str(self.timeStamp) + "\n")
            for i in range(0,self.nThermometers):
                f.write(str(self.tempF[i]) + "\n")
            f.close()
            print('Temps written to file')
        else:
            print("No thermometers loaded, nothing written to the file!")
    def roundTemps(self, nDigits):
        for i in range(0,self.nThermometers):
            self.tempF[i] = round(self.tempF[i],nDigits)
            self.tempC[i] = round(self.tempC[i],nDigits)
print("DS12B20 Module Loaded.")

#debug
# myTemps = DS18B20()
# myTemps.findDevices()
# print(myTemps.tempC)
# print(myTemps.nThermometers)
# myTemps.getAllTemps()
# myTemps.writeTempsFile()
# print(myTemps.thermIDs)
# myTemps.roundTemps(1)
# print(myTemps.tempC)
# myTemps.getAllTemps()
# myTemps.writeTempsFile()
# myTemps.readTempsFile()
# print(myTemps.tempC)
