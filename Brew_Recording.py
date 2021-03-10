import time


class BrewRecord():
    def __init__(self):
        self.fileName = "./tempHistory.csv"
        self.recording = False
        self.startTime = 0.0
        self.tempF = [0.0, 0.0, 0.0]

        # Rate of change calcs
        self.tTT = []
        self.dtdT = [0.0, 0.0]
        self.recordInterval = 10 # How often (in seconds) to record the temperature
        self.lastRecord = 0
        self.allTemps = [] # first index is time, second index is temp A
        
    def startRecord(self, eraseContents):
        # This method will start the recording process
        if(eraseContents):
            self.startTime = time.time()
            f = open(self.fileName, 'w')
            f.write(str(round(self.startTime)) + "\n")
            f.write("Time, TempA, TempB\n")
            f.close()
        else:
            f = open(self.fileName, 'r')
            line = f.readline()
            print(line)
        self.recording = True
        
    
    def stopRecord(self):
        self.recording = False
    # this method will stop the recording process
        pass
    
    def recordTemps(self):
    # This method will record temps if needed
        if(self.recording)&(time.time()> (self.lastRecord + self.recordInterval)): # Only record if it's been a while since the last recording
            f = open(self.fileName, 'a')
            strTemps = "%d, %2.1f, %2.1f\n" % (time.time() - self.startTime, self.tempF[0], self.tempF[2])
            f.write(strTemps)
            f.close
            self.lastRecord = time.time() # Save now as the most recent record time
    
    def importTemps(self, timePeriod):
        # This method will get all temps and times stored in the recording file in
        # the last number of seconds called out by timePeriod
        f = open(self.fileName, 'r')
        lines = f.readlines()
        i = len(lines)-1
        lastRecordedTime = lines[i][0]
        time=lastRecordedTime
        while False: #((lastRecordedTime-time)>timePeriod) & (i>1): # The i>1 is to keep from reading the header
            line = lines[i].split(",")
            print(line)
            time = line[0]
            tempA = line[1]
            i = i - 1
            
    def calcStats(self, target):
    # This method will calculate the average temperature over the past length of time,
    # the rate of change of the temperatures, the estimated time to the target temp,
        pass
    
    def calcDTs(self):
        self.tTT.append([time.time(), self.tempF[0], self.tempF[2]])
        ntTTs = len(self.tTT)

        nToAvg = min(ntTTs-2, 100)
        if(nToAvg>10):
            dt = self.tTT[ntTTs-1][0]-self.tTT[ntTTs-1-nToAvg][0]
            dT1 = self.tTT[ntTTs-1][1]-self.tTT[ntTTs-1-nToAvg][1]
            dT2 = self.tTT[ntTTs-1][2]-self.tTT[ntTTs-1-nToAvg][2]
            
            self.dtdT = [dT1*60/dt, dT2*60/dt]
        else:
            self.dtdT = [0.0, 0.0]
        
        # if cooling and got cool enough
        # Set the alarm  and text
        
print("Imported Brew Recording module")
# ### DEBUG
brewy = BrewRecord()
startTime = time.time()
brewy.importTemps(60)
print(time.time()-startTime)

