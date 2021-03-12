import RPi.GPIO as GPIO
import time
import sys
from pygame import mixer


class BrewLogic():
    def __init__(self, nThermometers):
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
        self.thermometer_error = False # If there's an error with the thermoemeters, set this b/c it's good to know!
        
        # Alarm Settings
        self.alarm = False
        self.alarmText = "Systems Nominal"
        self.alarmSoundWait = 30
        self.lastAlarmTime = 0
        
        # Rate of change calcs
        self.tTT = []
        self.dtdT = [0.0, 0.0]
        
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
        
        
    def brewCompute(self):
        self.heatCompute()
        self.heaterControl()
        self.calcDTs()
        self.alarmControl()
        self.saveSettingsFile()

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
            self.heatMode = 9 # Turn it off!
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
        self.tTT.append([time.time(), self.tempF[0], self.tempF[1]])
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
    def saveSettingsFile(self):
        f = open(self.setFile, 'w')
        originalStdout = sys.stdout
        sys.stdout = f
        print("Settings file for the Brasseur\n")
        print("heatMode\n%d \n" % self.heatMode)
        print("target\n%d \n" % self.target)
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
            i = i + 1
        


