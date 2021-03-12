# -*- coding: utf-8 -*-
#http://thinkingtkinter.sourceforge.net/all_programs.html
from tkinter import *
from tkinter import messagebox
import DS18B20_Module_Class_AK
import LCD1602_Module_AK as LCD1602
import Brew_Logic_Class
import time
import Brew_Recording
import Brew_Logging
import subprocess

#Constants


class ThermControl:
    def __init__(self, parent):
        self.switch_thermometers = False
        self.show_tInt = False
        self.iPadx = "1m"
        self.iPady = "1m"
        self.tempsFile = './tempsF.txt'
        self.parent = parent
        self.backend_process = None
        self.backend_stdout = None

        self.temporaryHM = IntVar()
        self.temporaryHE = IntVar()
        self.temporaryRT = IntVar()
        self.temporaryAR = IntVar()
            
        ## For the timers
        self.bStartTimer = list()
        self.chTLink = list()
        self.chTChangeT = list()
        self.enTarget = list()
        self.enTimeSet = list()
        self.enTMessage = list()
        self.lblTimeLeft = list()
        self.vTLink = []
        self.vTChangeT = []
        self.timerStarts = []
        self.timerSets = []
        self.timeLeft = []
        
        self.lcd = LCD1602.initLCD()
        self.lcd.message = "Ain't no party \n  like MNTP"
        self.therm = DS18B20_Module_Class_AK.DS18B20()
        self.therm.findDevices()
        self.logic = Brew_Logic_Class.BrewLogic(self.therm.nThermometers)
        self.record = Brew_Recording.BrewRecord()
    
    def create_monitor_display(self):    
        self.dispFrame = Frame(self.topContainer, background = "azure",
                               borderwidth = 3, relief = "solid")
        self.dispFrame.grid(ipadx = self.iPadx, ipady = self.iPady,
                            column = 1, row = 2)
         ### Fill Display Frame ###
        self.lblthermometers = Label(self.dispFrame,
                               text="Thermometers",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
        self.lblTAname = Label(self.dispFrame,
                               text="Boil /\n Heat Pad: ",
                               font = "TkDefaultFont 18 bold",
                               background = self.dispFrame["background"])
        self.lblTBname = Label(self.dispFrame,
                               text="Mash/\nFermentor: ",
                               font = "TkDefaultFont 18 bold",
                               background = self.dispFrame["background"])
        self.lblHeaters = Label(self.dispFrame,
                               text="Heaters",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
   
        self.lblTA = Label(self.dispFrame,
                      text="XX.X",
                      font= "TkDefaultFont 20 bold",
                      padx = 8, pady = 0,width=5,
                      borderwidth=2, relief = "solid")
        self.lblTB = Label(self.dispFrame,
                      text="XX.X",
                      font= "TkDefaultFont 20 bold",
                      padx = 8, pady = 0,width=5,
                      borderwidth=2, relief = "solid")
        self.lbldTAdt = Label(self.dispFrame,
                      font= "TkDefaultFont 16 bold",
                      bg = "chartreuse2",
                      padx = 8, pady = 0, width=7,
                      borderwidth=2, relief = "solid")
        self.lbldTBdt = Label(self.dispFrame,
                      font= "TkDefaultFont 16 bold",
                      bg = "chartreuse2",
                      padx = 8, pady = 0,width=7,
                      borderwidth=2, relief = "solid")
        self.lblH1 = Label(self.dispFrame,
                      font= "TkDefaultFont 20 bold",
                      padx = 8, pady = 0,
                      borderwidth=2, relief = "solid")
        self.lblH2 = Label(self.dispFrame,
                      font= "TkDefaultFont 20 bold",
                      padx = 8, pady = 0,
                      borderwidth=2, relief = "solid")
        self.lblHeatEnabled = Label(self.dispFrame,
                      font= "TkDefaultFont 16 bold",
                      padx = 8, pady = 0,
                      borderwidth=2, relief = "solid")

        # Grid em up - Display
        self.lblthermometers.grid(row = 1, column = 2, columnspan = 3, padx = 10, pady = 10)
        self.lblTAname.grid(row=2, column = 2, padx = 5, pady = 5)
        self.lblTBname.grid(row=4, column = 2, padx = 5, pady = 5) 
        self.lblTA.grid(row=2, column = 3, sticky=W, padx = 10, pady = 5)
        self.lblTB.grid(row=4, column = 3, sticky=W, padx = 10, pady = 5)
        self.lbldTAdt.grid(row=2, column = 4, sticky=W, padx = 10, pady = 5)
        self.lbldTBdt.grid(row=4, column = 4, sticky=W, padx = 10, pady = 5)
        self.lblHeaters.grid(row = 6, column = 2, columnspan = 3, padx = 10, pady = 10)
        self.lblH1.grid(row = 8, column = 3, padx = 10, pady = 5)
        self.lblH2.grid(row = 8, column = 4, padx = 10, pady = 5)
        self.lblHeatEnabled.grid(row = 7, column = 2, columnspan = 3, padx = 10, pady =5)

    def create_top_container(self):
        self.topContainer = Frame(self.parent, bg = "azure")
        self.topContainer.grid(ipadx = self.iPadx, ipady = self.iPady)
        
    def create_controls(self):
        self.controlFrame = Frame(self.topContainer, background = "azure",
                                  borderwidth = 3, relief = "solid")
        self.controlFrame.grid(ipadx = self.iPadx, ipady = self.iPady,
                               column = 2, row = 2)
        # Target temperature slider
        self.lblTarget = Label(self.controlFrame,
                               text="Target\nTemperature",
                               font= "TkDefaultFont 12",
                               bg = "gainsboro",
                               padx = 8, pady = 0,
                               borderwidth=2, relief = "solid")
        self.slTarget = Scale(
            self.controlFrame,
            length=200,
            from_=212, to_=50,
            borderwidth=2, relief = "solid")

        
        # Enable heaters and heat mode radio buttons
        self.chEnable = Checkbutton(self.controlFrame, text = "Enable Heaters",
                                    variable = self.temporaryHE,
                                    onvalue = 1, offvalue = 0)
        self.chRecord = Checkbutton(self.controlFrame, text = "Record Temps",
                                    variable = self.temporaryRT,
                                    onvalue = 1, offvalue = 0)
        
        self.rMode1 = Radiobutton(self.controlFrame, text = "Heating",
                                  variable = self.temporaryHM, value = 0)
        self.rMode2 = Radiobutton(self.controlFrame, text = "Maintain",
                                  variable = self.temporaryHM, value = 1)
        self.rMode3 = Radiobutton(self.controlFrame, text = "Cool",
                                  variable = self.temporaryHM, value = 2)
        self.rMode4 = Radiobutton(self.controlFrame, text = "Off",
                                  variable = self.temporaryHM, value = 9)

        # Controls gridding
        self.lblTarget.grid(row=1, column=2,
                            padx=10, pady=5)
        self.slTarget.grid(row=2, column = 2,
                           padx = 25, pady=5)
        self.chEnable.grid(row = 4, column = 2, sticky = W,
                           padx = 25, pady=5)
        self.chRecord.grid(row = 5, column = 2, sticky = W,
                           padx = 25, pady = 5)
        self.rMode1.grid(row = 6, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode2.grid(row = 7, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode3.grid(row = 8, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode4.grid(row = 9, column = 2, sticky = W,
                         padx = 25, pady=4)     

    def initialize_controls(self):    
        #Initialize the radiobutton
        
        if(self.logic.heatMode==0): # Set the radio buttons to the operating mode
            self.rMode1.select()    # that the logic controller came up with
        elif(self.logic.heatMode==1):
            self.rMode2.select()
        elif(self.logic.heatMode==2):
            self.rMode3.select()
        else:
            self.rMode4.select()
        
        self.slTarget.set(self.logic.target)
    
 
    def create_scheduling(self):       
        self.schedFrame = Frame(self.topContainer, background = "azure",
                                borderwidth = 3, relief = "solid")
        self.schedFrame.grid(ipadx = self.iPadx, ipady = self.iPady,
                             column = 3, row = 2)
        # Scheduling
        self.nTimers = 7
        self.lblTimerTop = Label(self.schedFrame,text = "   Message \n Rem Time      Temp",
                            font = "TkDefaultFont 16")
        #self.bStartAllTimers = Button(self.schedFrame, command = self.timer_handling(),
        #              text = "Start All", font = "TkDefaulTFont 14" , padx = 5, pady = 5)
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(0)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(1)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(2)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(3)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(4)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(5)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timer_handling(6)))
        
        # Timer boxes
        for i in range(0,self.nTimers):
            self.vTLink.append(IntVar(value=0))
            self.vTChangeT.append(IntVar(value=0))
            self.chTLink.append(Checkbutton(self.schedFrame, text = "Link", highlightthickness=0,
                                            onvalue = 1, offvalue = 0, var=self.vTLink[i],
                                            bg = "azure"))
            self.chTChangeT.append(Checkbutton(self.schedFrame, text = "Temp", highlightthickness=0,
                                            onvalue = 1, offvalue = 0, var=self.vTChangeT[i],
                                               bg = "azure"))
            self.enTarget.append(Entry(self.schedFrame, width=5, relief="solid", bd=2))
            self.enTimeSet.append(Entry(self.schedFrame, width=5, relief="solid", bd=2))
            self.enTMessage.append(Entry(self.schedFrame, relief="solid", bd=2))
            self.lblTimeLeft.append(Label(self.schedFrame, text = "0:00", font = "TkDefaultFont 15", width=6,
                                          bg = "deep sky blue", height=2, borderwidth=2, relief="solid"))
            self.timerStarts.append(0)
            self.timerSets.append(0)
            self.timeLeft.append(0)
        
        # Scheudling Gridding
        self.lblTimerTop.grid(row=1, column = 1, columnspan = 4)
        #self.bStartAllTimers.grid(row=1, column=5)        
        for i in range(0,self.nTimers):
            self.bStartTimer[i].grid(row=2*i+3, column=5)
            self.chTLink[i].grid(row=2*i+4, column=3)
            self.chTChangeT[i].grid(row=2*i+4, column=5)
            self.enTarget[i].grid(row=2*i+4, column=4)
            self.enTimeSet[i].grid(row=2*i+4, column=2)
            self.enTMessage[i].grid(row=2*i+3, column=2,columnspan=3)
            self.lblTimeLeft[i].grid(row=2*i+3, column=1, rowspan=2)


    def create_top_Bar(self):
        self.topBarFrame = Frame(self.topContainer, bg = "azure")
        self.topBarFrame.grid(ipadx = self.iPadx, ipady = self.iPady,
                              column = 1, row = 0, columnspan = 4)        
        # Top Bar
        self.lblAlarm = Label(self.topBarFrame,
                      font = "TkDefaultFont 15 bold",
                    padx = 10, pady = 10,
                    borderwidth = 2, relief = "solid")
        if self.show_tInt:      # Internal temperature 
            self.lblTint = Label(self.topBarFrame,
                    font = "TkDefaultFont 15 bold", bg = "khaki1",
                    padx = 10, pady = 10,
                    borderwidth = 2, relief = "solid")
        self.bAcknowledge = Button(self.topBarFrame,
                             command = self.acknowledge_alarms,
                             text = "Acknowledge",
                             padx = "2m", pady = "2m",
                            font = "TkDefaultFont 15 bold",
                             width = 12)
        self.bStartBackend = Button(self.topBarFrame,
                             command = self.start_backend,
                             text = "Start Backend",
                             padx = "2m", pady = "2m",
                            font = "TkDefaultFont 15 bold",
                             width = 12)
        self.chAutoBackend = Checkbutton(self.topBarFrame, text = "Auto-restart\nBackend", highlightthickness=0,
                                            onvalue = True, offvalue = False, var=self.temporaryAR,
                                            bg = "azure")
        #Gridding up the top bar
        self.lblAlarm.grid(row = 2, column = 7)
        self.bAcknowledge.grid(row=2, column = 11, sticky = E)
        self.bStartBackend.grid(row=2, column = 5, sticky = E)
        self.chAutoBackend.grid(row=2, column=4, sticky = E)
        if self.show_tInt:
            self.lblTint.grid(row = 2, column = 4, sticky = W)
        
    
    def update_temps(self):
        self.therm.readTempsFile()
        # Temp fix
        if(self.switch_thermometers):
            self.therm.tempF = [self.therm.tempF[1], self.therm.tempF[0]]
        self.logic.thermTimeStamp = self.therm.timeStamp
        self.logic.target = self.slTarget.get()
        self.logic.heatMode = self.temporaryHM.get()
        self.logic.heatEnabled = self.temporaryHE.get()
        #self.therm.tempF = [self.therm.tempF[1], self.therm.tempF[1], self.therm.tempF[0]]
        self.logic.tempF = self.therm.tempF
        self.logic.brewCompute()
        LCD1602.dispTemps(self.lcd, self.therm.tempF, self.logic.target, self.logic.heatOn[0], self.logic.dtdT[0])
        root.after(100, self.update_others)
        
        
    def update_others(self):
        # Update Temps
        self.lblTA["text"] = str(round(self.therm.tempF[0],1))
        self.lblTB["text"] = str(round(self.therm.tempF[1],1))
        # If there's a thermometer Error, change the temp things Red
        if self.logic.thermometer_error:
            self.lblTA["bg"] = "firebrick1"
            self.lblTB["bg"] = "firebrick1"
        else:
            self.lblTA["bg"] = "chartreuse2"
            self.lblTB["bg"] = "chartreuse2"

        self.lbldTAdt["text"] = str(round(self.logic.dtdT[0],2)) + "°/m"
        self.lbldTBdt["text"] = str(round(self.logic.dtdT[1],2)) + "°/m"
        if self.show_tInt:
            self.lblTint["text"] = "Int: " + str(int(round(self.therm.tempF[1],0)))
            if(self.therm.tempF[1]>90.0):
                self.lblTint["bg"] = "firebrick1"
            else:
                 self.lblTint["bg"] = "gainsboro"   
        # Update Disabled / On/Off
        if(self.logic.heatEnabled): #If the heaters are enabled make it pink
            self.lblHeatEnabled.configure(text= "ENABLED", bg = "DeepPink2")
        else:
            self.lblHeatEnabled.configure(text= "Disabled", bg = "gainsboro")

        if(self.logic.heatOn[0]): # If the heaters are on make them orange
            self.lblH1.configure(text = "ON", bg = "DarkOrange")
        else:
            self.lblH1.configure(text = "OFF", bg = "gainsboro")
        if(self.logic.heatOn[1]):
            self.lblH2.configure(text = "ON", bg = "DarkOrange")
        else:
            self.lblH2.configure(text = "OFF", bg = "gainsboro")

        self.alarm_handling()
        self.timer_handling(-1)

        if(self.record.recording==False)&(self.temporaryRT.get()>0): # If we weren't recording but want to
            answer = messagebox.askyesno("Erase contents?","Would you like to erase the previously recorded temperatures?")
            #self.record.startRecord(answer)
        elif(self.record.recording)&(self.temporaryRT.get()>0): #If we were already recording and want to keep recording
            #self.record.tempF = self.logic.tempF
            #self.record.recordTemps()
            pass
        else: # If we want to stop recording
            self.record.recording = False

        root.after(100, self.update_temps)
        
    def alarm_handling(self):
        # This one 
        if self.logic.alarm:
            self.lblAlarm.configure(text = self.logic.alarmText, bg = "firebrick1")
            if self.logic.heatMode==0: # Set the radio buttons to the operating mode
                self.rMode1.select()    # that the logic controller came up with
            elif self.logic.heatMode==1:
                self.rMode2.select()
            elif self.logic.heatMode==2:
                self.rMode3.select()
            else:
                self.rMode4.select()
        else:
            self.lblAlarm.configure(text = self.logic.alarmText, bg = "gainsboro")
        if self.temporaryAR.get() and self.logic.thermometer_error: # If the user wants to autorset the background and the thermometers failed,
            print('Thermometer failed, restarting...')
            self.start_backend(command='end')
            time.sleep(1)
            self.start_backend(command='start')
            time.sleep(2)
            self.logic.thermometer_error = False
            self.logic.alarmText = 'Previous Thermometer Alarm\nNow Operational'
            self.logic.alarm = False

    
    def acknowledge_alarms(self):
        self.logic.alarm = False
        self.logic.alarmText = "Systems Nominal"

    def start_backend(self, command = 'toggle'):
        if command=='toggle' and self.backend_process==None: #If toggle and if it's off
            command='start'
        elif command=='toggle' and (not self.backend_process==None): # if toggle and running
            command='end'

        if command=='start':
            if self.backend_process == None:
                print('Starting new backend process')
                # Start the backend
                self.backend_process = subprocess.Popen(['python', './Brasseur_Backend.py'], 
                        stdout = self.backend_stdout)
                self.bStartBackend.configure(text = 'End Backend')
            else:
                print('Backend process already running')
        elif command=='end':
            if self.backend_process==None:
                print('Backend not running, nothing to end')
            else:
                print('Closing backend process')
                self.backend_process.terminate()
                self.backend_process = None
                self.bStartBackend.configure(text = 'Start Backend')
        else:
            print('Invalid command sent to start_backend - nothing done.')

    def timer_handling(self, timerToStart):
        if(timerToStart<0):
            for i in range(0,self.nTimers):
                if(self.timerStarts[i]>0): # If the timer is on
                    # calculate the time left
                    self.timeLeft[i]= self.timerStarts[i]+self.timerSets[i]-time.time()
                    if(self.timeLeft[i]<0): # If it's less than zero, then set the alarm
                        self.logic.alarm = True
                        if(len(self.enTMessage[i].get())<1):
                            self.logic.alarmText = "Timer Done!"
                        else:
                            self.logic.alarmText = self.enTMessage[i].get()
                        self.timerStarts[i]=0
                        self.timeLeft[i]=0
                        if(self.vTChangeT[i].get()>0):# If temp is checked, set the target temp
                            try:
                                self.slTarget.set(int(self.enTarget[i].get()))
                            except:
                                self.logic.alarmText = "Timer Done - Temp Error"
                    else: # Otherwise display the time left
                        tlMin = str(int(round(self.timeLeft[i]/60-0.5,0)))
                        tlSec = str(int(round(self.timeLeft[i]%60,0)))
                        if(round(self.timeLeft[i]%60,0)<10):
                            tlSec = "0"+ tlSec
                        strTimeLeft= tlMin + ":" + tlSec
                        self.lblTimeLeft[i].configure(text=strTimeLeft)

        
        else: # if the function was called for a specific timer, then start it
            self.timerSets[timerToStart] = int(round(float(self.enTimeSet[timerToStart].get())*60,0))
            self.timerStarts[timerToStart] = time.time() #start the specific timer
            # Turn the i'th button to a STOP button
            
    
    def closeWindow(self):
        self.parent.destroy()        
        


# Make the GUI        
root = Tk()
root.title("Brasseur - 1.0")
brasseur = ThermControl(root)

brasseur.create_top_container()
brasseur.create_monitor_display()
brasseur.create_controls()
brasseur.initialize_controls()
brasseur.create_scheduling()
brasseur.create_top_Bar()

#print("Backend is:")
#print(brasseur.backend_process)
#brasseur.start_backend()
#print("Backend is now:")
#print(brasseur.backend_process)

#time.sleep(5)
#print("Backend has error and:")
#print(brasseur.backend_process)



brasseur.update_temps() #Begin update loop

print("Starting Tk loop. GLHF!")
root.mainloop()
print("Ended Tk loop. Cheers!")


