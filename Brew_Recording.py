import time


class BrewRecord():
    def __init__(self):
        self.fileName = "tempHistory.csv"
        self.recording = False
        self.tempF = [0.0, 0.0]

        # Rate of change calcs
        self.tTT = []
        self.dtdT = [0.0, 0.0]
        self.recordInterval = 10 # How often (in seconds) to record the temperature
        self.lastRecord = 0
        
    def startRecord(self):
    # This method will start the recording process
        print(time.time())
    
    def stopRecord(self):
    # this method will stop the recording process
        pass
    
    def manageRecord(self):
    # This method will record temps if needed
        pass
    
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

brewy = BrewRecord()
print(brewy.tempF)
brewy.startRecord()