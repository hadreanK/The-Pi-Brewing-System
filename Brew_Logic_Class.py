import RPi.GPIO as GPIO
import time
import sys
from pygame import mixer


class BrewLogic():
    def __init__(self, parent, nThermometers):
        self.tempF = []
        for i in range(0,nThermometers):
            self.tempF.append(0.0)
        self.tempTimeStamp = 0.0
        self.heatOn = [False, False]
        self.heatEnabled = False
        self.goodEnoughThreshold =200.0
        self.thermometer_no_resp_limit = 20.0
        self.holdingDuty = 0.70
        self.target = 0
        self.heatMode = 0
        self.heat_average_time = 1.0 #in minutes
        self.thermometer_error = False # If there's an error with the thermoemeters, set this b/c it's good to know!
        self.auto_reset_backend = False
        self.parent = parent

        # Alarm Settings
        self.alarm = False
        self.alarmText = "Systems Nominal"
        self.alarmSoundWait = 30
        self.lastAlarmTime = 0
        
        # Rate of change calcs
        self.tTT = []
        self.dtdT = [0.0, 0.0]
        self.record_temp_period = 5 # How often to record the temperature in seconds
        self.last_temp_record = 0 # Last time we recorded the temperature

        # Set Up Pins
        self.heat1Pin = 20
        self.heat2Pin = 21
        GPIO.setup(self.heat1Pin, GPIO.OUT)
        GPIO.setup(self.heat2Pin, GPIO.OUT)
        
        # Set up music / alarms
        mixer.init()
        mixer.init()
        mixer.music.load('/home/pi/Documents/Beer Maker/The-Pi-Brewing-System/Sounds/Hospital Beep.mp3')
        
        # Set up settings file stuff and get the values from the file
        self.setFile = './settings.txt'
        self.openSettingsFile()
        self.tempHistoryFile = './temp_history.txt'
        self.openTempHistoryFile()
        self.temp_history_length = 120 #Amount of time to save time/temp data for in minutes
        self.write_history_period = 30 # How often to save the temp history
        self.last_history_save = 0 # Last time we saved the history

    def brewCompute(self):
        self.heatCompute()
        self.heaterControl()
        self.calcDTs()
        self.alarmControl()
        self.saveSettingsFile()
        now = time.time()
        if (now - self.last_history_save) > self.write_history_period:
            self.saveTempHistoryFile()
            self.last_history_save = now

    def heatCompute(self):
        # Decide if the haters should be turned on
        if (self.heatMode < 2) & (self.tempF[0] < self.target) & self.heatEnabled:
            self.heatOn = [True, True]
        else:
            self.heatOn = [False, False]
            
    def heaterControl(self):
        if(self.heatEnabled):
            GPIO.output(self.heat1Pin, self.heatOn[0])
            GPIO.output(self.heat2Pin, self.heatOn[1])
        else:
            GPIO.output(self.heat1Pin, False)
            GPIO.output(self.heat2Pin, False)
        
    def alarmControl(self):
        #Heated to temp
        if(self.heatMode==0)&(self.tempF[0]>=self.target):#If heating and reach temp, 
            self.alarm = True
            self.alarmText = "Reached target Temp!"  # Set alarm and alarm text
            self.heatMode = 1   # Change to maintain
        
        #If too hot when trying to maintain
        elif(self.heatMode==1)&((self.tempF[0]-self.target)>self.goodEnoughThreshold):
            self.alarm = True
            self.alarmText = "Too Hot!"
            self.heatMode = 2 # Change to cooling
            
        #If too cold when trying to maintain
        elif(self.heatMode==1)&((self.target-self.tempF[0])>self.goodEnoughThreshold):
            self.alarm = True
            self.alarmText = "Too Cold!"
            self.heatMode = 0 # Change to heating
        
        # If it's cooled enough, turn it off
        elif(self.heatMode==2)&(self.tempF[0]<self.target):
            self.alarm = True
            self.alarmText = "Cooled to target!"
            self.heatMode = 9 # Turn it off
        
        # If the temperature we're working with is super old, then set an alarm
        if (time.time() - self.thermTimeStamp) > self.thermometer_no_resp_limit:
            self.alarm = True
            self.alarmText = "Thermometer Error!"
            #self.heatMode = 9 # Turn it off!
            self.thermometer_error = True # Set the thermometer error
        else:
            self.thermometer_error = False # Otherwise clear the thermometer error
        
        # Play sound
        if(self.alarm):
            if(time.time()>(self.lastAlarmTime+self.alarmSoundWait)):
                self.lastAlarmTime = time.time() 
                mixer.music.play() #https://www.zapsplat.com/sound-effect-category/machines/
        else:
            mixer.music.fadeout(500)
            self.lastAlarmTime = 0
            
    def calcDTs(self):
        now = time.time()
        if (now - self.last_temp_record) >  self.record_temp_period:
            self.tTT.append([now, self.tempF[0], self.tempF[1]])
            self.last_temp_record = now

        ntTTs = len(self.tTT)
        index_to_avg = 0

        for i in range(0,ntTTs):
            if self.tTT[i][0] < (now - self.heat_average_time*60): # Heat average time is in minutes
                index_to_avg = i

        if ntTTs>5:
            dt = now-self.tTT[index_to_avg][0]
            dT1 = self.tempF[0]-self.tTT[index_to_avg][1]
            dT2 = self.tempF[1]-self.tTT[index_to_avg][2]
            
            self.dtdT = [dT1*60.0/dt, dT2*60.0/dt]
        else:
            self.dtdT = [0.0, 0.0]
        
        # if cooling and got cool enough
        # Set the alarm  and text
    def saveSettingsFile(self):
        f = open(self.setFile, 'w')
        originalStdout = sys.stdout
        sys.stdout = f
        print("Settings file for the Brasseur\n")
        print("heatMode\n%d \n" % self.heatMode)
        print("target\n%d \n" % self.target)
        if self.auto_reset_backend:
            x = 1
        else:
            x = 0
        print("autoRestartBackend\n%d \n" % x)
        print("brew_id\n" + self.parent.brew_id + "\n")
        print("heat_average_time\n%f \n" % self.heat_average_time)
        sys.stdout = originalStdout
        
        
    def openSettingsFile(self):
        f = open(self.setFile, 'r')
        lines = f.readlines()
        f.close
        print("Reading from settings file...")
        i = 1
        for line in lines:
            if(i == 4):
                self.heatMode = int(line)
            if(i == 7):
                self.target = int(line)
            if i == 10:
                if int(line) == 1:
                    self.auto_reset_backend = True
            if i == 13:
                self.parent.brew_id = line.strip()
            if(i == 16):
                self.heat_average_time = float(line)
            i = i + 1
    
    def saveTempHistoryFile(self):
        f = open(self.tempHistoryFile, 'w')
        now = time.time()
        for i in range(0,len(self.tTT)):
            if (now - self.tTT[i][0]) > self.temp_history_length: # If these times were saved super long ago
                i = len(self.tTT) #Exit the loop
            else:
                line = str(round(self.tTT[i][0])) + ',' + str(self.tTT[i][1]) + ',' + str(self.tTT[i][2])
                f.write(line + '\n')
        

    def openTempHistoryFile(self):
        try:
            f = open(self.tempHistoryFile, 'r')
            lines = f.readlines()
            print(lines)
            self.tTT = []
            for line in lines:
                line_split = line.split(',')
                self.tTT.append([float(x) for x in line_split])
            print('Opened temperature history')
        except:
            print('No temp history file to open!')
        print(self.tTT)
            

