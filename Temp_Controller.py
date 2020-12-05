#http://thinkingtkinter.sourceforge.net/all_programs.html
from tkinter import *
import DS18B20_Module_Class_AK
import LCD1602_Module_AK as LCD1602
import Brew_Logic_Class
import time

#Constants
bPadx = "1m"
bPady = "1m"
bIPadx = "1m"
bIPady = "1m"
bFont = ""

class ThermControl:
    def __init__(self, parent):
        
        ### Instance variables ###
        self.tempsFile = './tempsF.txt'
        self.MyParent = parent
        self.temporaryHM = IntVar()
        self.temporaryHE = IntVar()
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
        self.logic = Brew_Logic_Class.BrewLogic()
        
        ### Make Frames ###
        self.myParent = parent
        self.topContainer = Frame(parent, bg = "azure")
        self.topContainer.grid(ipadx = bIPadx, ipady = bIPady)
        self.dispFrame = Frame(self.topContainer, background = "azure",
                               borderwidth = 3, relief = "solid")
        self.dispFrame.grid(ipadx = bIPadx, ipady = bIPady,
                            column = 1, row = 2)
        self.controlFrame = Frame(self.topContainer, background = "azure",
                                  borderwidth = 3, relief = "solid")
        self.controlFrame.grid(ipadx = bIPadx, ipady = bIPady,
                               column = 2, row = 2)
        self.schedFrame = Frame(self.topContainer, background = "azure",
                                borderwidth = 3, relief = "solid")
        self.schedFrame.grid(ipadx = bIPadx, ipady = bIPady,
                             column = 3, row = 2)
        self.botBarFrame = Frame(self.topContainer)
        #self.botBarFrame.grid(ipadx = bIPadx, ipady = bIPady,
                              #column = 1, row = 3, columnspan = 2)
        self.topBarFrame = Frame(self.topContainer, bg = "azure")
        self.topBarFrame.grid(ipadx = bIPadx, ipady = bIPady,
                              column = 1, row = 0, columnspan = 4)        
        ### Fill Display Frame ###
        self.lblthermometers = Label(self.dispFrame,
                               text="Thermometers",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
        self.lblTAname = Label(self.dispFrame,
                               text="A: ",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
        self.lblTBname = Label(self.dispFrame,
                               text="B: ",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
        self.lblHeaters = Label(self.dispFrame,
                               text="Heaters",
                               font = "TkDefaultFont 20 bold",
                               background = self.dispFrame["background"])
   
        self.lblTA = Label(self.dispFrame,
                      text="XX.X",
                      font= "TkDefaultFont 20 bold",
                      bg = "chartreuse2",
                      padx = 8, pady = 0,width=5,
                      borderwidth=2, relief = "solid")
        self.lblTB = Label(self.dispFrame,
                      text="XX.X",
                      font= "TkDefaultFont 20 bold",
                      bg = "chartreuse2",
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
        
        ### Controls ###
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

        self.slTarget.set(190)
        
        # Enable heaters and heat mode radio buttons
        self.cHEnable = Checkbutton(self.controlFrame, text = "Enable Heaters",
                                    variable = self.temporaryHE,
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
        self.cHEnable.grid(row = 4, column = 2, sticky = W,
                           padx = 25, pady=10)
        self.rMode1.grid(row = 6, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode2.grid(row = 7, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode3.grid(row = 8, column = 2, sticky = W,
                         padx = 25, pady=4)
        self.rMode4.grid(row = 9, column = 2, sticky = W,
                         padx = 25, pady=4)
        
        # Scheduling
        self.nTimers = 7
        self.lblTimerTop = Label(self.schedFrame,text = "   Message \n Rem Time      Temp",
                            font = "TkDefaultFont 16")
        self.bStartAllTimers = Button(self.schedFrame, command = self.timerHandling,
                      text = "Start All", font = "TkDefaulTFont 14" , padx = 5, pady = 5)
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(0)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(1)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(2)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(3)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(4)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(5)))
        self.bStartTimer.append(Button(self.schedFrame, text = "Start", font="TkDefaultFont 10",
                                           command = lambda: self.timerHandling(6)))
            
        
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
        self.bStartAllTimers.grid(row=1, column=5)        
        for i in range(0,self.nTimers):
            self.bStartTimer[i].grid(row=2*i+3, column=5)
            self.chTLink[i].grid(row=2*i+4, column=3)
            self.chTChangeT[i].grid(row=2*i+4, column=5)
            self.enTarget[i].grid(row=2*i+4, column=4)
            self.enTimeSet[i].grid(row=2*i+4, column=2)
            self.enTMessage[i].grid(row=2*i+3, column=2,columnspan=3)
            self.lblTimeLeft[i].grid(row=2*i+3, column=1, rowspan=2)
        i=69
            
            
            
            
        #self.bTimer1.grid(row=2, column=5)
        # Bottom bar 
        self.bClose = Button(self.botBarFrame,
                             command = self.closeWindow,
                             text = "Close",
                             padx = "2m", pady = "2m",
                             width = 10)
        # Gridding the bottom bar
        self.bClose.grid(row = 1, column = 10, sticky = E)
        
        # Top Bar
        self.lblAlarm = Label(self.topBarFrame,
                      font = "TkDefaultFont 15 bold",
                    padx = 10, pady = 10,
                    borderwidth = 2, relief = "solid")
        self.lblTint = Label(self.topBarFrame,
                      font = "TkDefaultFont 15 bold", bg = "khaki1",
                    padx = 10, pady = 10,
                    borderwidth = 2, relief = "solid")
        self.bAcknowledge = Button(self.topBarFrame,
                             command = self.acknowledgeAlarms,
                             text = "Acknowledge",
                             padx = "2m", pady = "2m",
                            font = "TkDefaultFont 15 bold",
                             width = 12)
        #Gridding up the top bar
        self.lblAlarm.grid(row = 2, column = 7)
        self.lblTint.grid(row = 2, column = 4, sticky = W)
        self.bAcknowledge.grid(row=2, column = 11, sticky = E)
        
    
    def updateTemps(self):
       # get the temps from the stuff
        self.therm.readTempsFile()
        self.logic.thermTimeStamp = self.therm.timeStamp
        self.logic.target = self.slTarget.get()
        self.logic.heatMode = self.temporaryHM.get()
        self.logic.heatEnabled = self.temporaryHE.get()
        self.therm.tempF = [self.therm.tempF[2], self.therm.tempF[1], self.therm.tempF[0]]
        self.logic.tempF = self.therm.tempF
        self.logic.brewCompute()
        LCD1602.dispTemps(self.lcd, self.therm.tempF)
        root.after(100, self.updateOtherThings)
        
        
    def updateOtherThings(self):
        # Update Temps
        self.lblTA["text"] = str(round(self.therm.tempF[0],1))
        self.lblTB["text"] = str(round(self.therm.tempF[2],1))
        self.lbldTAdt["text"] = str(round(self.logic.dtdT[0],2)) + "°/m"
        self.lbldTBdt["text"] = str(round(self.logic.dtdT[1],2)) + "°/m"
        self.lblTint["text"] = "Int: " + str(int(round(self.therm.tempF[1],0)))
        if(self.therm.tempF[1]>90.0):
            self.lblTint["bg"] = "firebrick1"
        else:
             self.lblTint["bg"] = "gainsboro"   
        # Update Disabled / On/Off
        if(self.logic.heatEnabled):
            self.lblHeatEnabled.configure(text= "ENABLED", bg = "DeepPink2")
        else:
            self.lblHeatEnabled.configure(text= "Disabled", bg = "gainsboro")
        if(self.logic.heatOn[0]):
            self.lblH1.configure(text = "ON", bg = "DarkOrange")
        else:
            self.lblH1.configure(text = "OFF", bg = "gainsboro")
        if(self.logic.heatOn[1]):
            self.lblH2.configure(text = "ON", bg = "DarkOrange")
        else:
            self.lblH2.configure(text = "OFF", bg = "gainsboro")
        self.alarmHandling()
        self.timerHandling(-1)
        self.logic.saveSettingsFile()
        root.after(100, self.updateTemps)
        
    def alarmHandling(self):
        # 
        if(self.logic.alarm):
            self.lblAlarm.configure(text = self.logic.alarmText, bg = "firebrick1")
            if(self.logic.heatMode==0): # Set the radio buttons to the operating mode
                self.rMode1.select()    # that the logic controller came up with
            elif(self.logic.heatMode==1):
                self.rMode2.select()
            elif(self.logic.heatMode==2):
                self.rMode3.select()
            else:
                self.rMode4.select()
        else:
            self.lblAlarm.configure(text = self.logic.alarmText, bg = "gainsboro")
    
    def acknowledgeAlarms(self):
        self.logic.alarm = False
        self.logic.alarmText = "Systems Nominal"
        
    def timerHandling(self, timerToStart):
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
            print(timerToStart)
            print(self.enTimeSet[timerToStart].get())
            self.timerStarts[timerToStart] = time.time() #start the specific timer
            # Turn the i'th button to a STOP button
            
    
    def closeWindow(self):
        self.MyParent.destroy()        
        

#Initialize things
        
root = Tk()
root.title("Brasseur - 0.9")
myapp = ThermControl(root)
myapp.updateTemps()

print("Starting Tk loop")
root.mainloop()
print("Ended Tk loop")


