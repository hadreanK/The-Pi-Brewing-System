import glob
import time

class DS18B20():
    def __init__(self):
        self.dir = '/sys/bus/w1/devices/'
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
            
    def updateNextTemp(self):
        f = open(self.tempFiles[self.nextTempToUpdate])
        line = f.readlines()
        f.close
        temp = float(line[0])
        self.tempC[self.nextTempToUpdate] = temp/1000.0
        self.tempF[self.nextTempToUpdate] = (temp*9/5+32.0)/1000.0
            #iterate nextTempToUpdate
        self.nextTempToUpdate = (self.nextTempToUpdate + 1)%self.nThermometers
        

    def getLabelledTemps(self, conv_to_degF):
        raw = getAllTemps(conv_to_degF)
        # 0 -> A
        # 1 -> Internal
        # 2 -> B
        labelled = [ ['A', raw[0]], \
                     ['B', raw[2]], \
                     ['internal', raw[1]]]
        return(labelled)
        
        
    def updateTempOld(self, conv_to_degF):
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/temperature'
        
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        
        temp = float(lines[0])
        temp = temp / 1000.0 # Get temp in celcius
        if(conv_to_degF):
            temp = temp * 9 / 5 + 32
        return(temp)
    
    def readTempsFile(self):
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
        f = open(self.tempsFile, 'w')
        f.write(str(self.timeStamp) + "\n")
        for i in range(0,self.nThermometers):
            f.write(str(self.tempF[i]) + "\n")
        f.close()
        
print("DS12B20 Module Loaded.")

#debug
#myTemps = DS18B20()
#myTemps.findDevices()
#print(myTemps.tempC)
#print(myTemps.nThermometers)
#myTemps.getAllTemps()
#myTemps.writeTempsFile()