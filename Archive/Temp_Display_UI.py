#http://thinkingtkinter.sourceforge.net/all_programs.html
from tkinter import *
import DS18B20_Module_AK as DS18B20
import LCD1602_Module_AK as LCD1602
from time import sleep

#Constants
bPadx = "3m"
bPady = "2m"
bIPadx = "10m"
bIPady = "8m"
bFont = ""

class ThermDisp:
    def __init__(self, parent):
        
        # Instance variables
        self.MyParent = parent
        self.temps = [0.0, 0.0, 0.0] #TA, TB, int    
        self.lcd = LCD1602.initLCD()
        self.lcd.message = "Ain't no party \n  like MNTP"
        
        self.myParent = parent
        self.thermContainer = Frame(parent)
        self.thermContainer.pack(ipadx = bIPadx, ipady = bIPady)
        
        self.button1 = Button(self.thermContainer, command=self.updateTemps
                                , text = "Get Temps",
                                padx = bPadx, pady = bPady,
                                width = 10)
        self.button1.pack(side = LEFT)
        self.button1.focus_force()
        
        self.bClose = Button(self.thermContainer,
                             command = self.closeWindow,
                             text = "Close",
                             padx = "2m", pady = "2m",
                             width = 10)
        self.bClose.pack(side = RIGHT)
        
    
    def updateTemps(self):
       # get the temps from the stuff
        self.temps = DS18B20.getLabelledTemps(True)
        LCD1602.dispTemps(self.lcd, self.temps)
        print("Temps are: " + 
              str(self.temps[0]) + ", " +
              str(self.temps[1]) + ", " +
              str(self.temps[2]))
        
    def closeWindow(self):
        self.MyParent.destroy()

#Initialize things
        
temps = DS18B20.getAllTemps(True)
root = Tk()
myapp = ThermDisp(root)
myapp.temps = temps
print("Starting Tk loop")
root.mainloop()
print("Ended Tk loop")

