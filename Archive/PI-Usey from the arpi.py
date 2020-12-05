import serial
import time
from tkinter import *

# --- Define variables --- #
Temps = [0.0, 0.0, 0.0]
Target = 170
HeaterOn = [0, 0]
HeaterEnabled = False

def EnableHeater():
    global HeaterEnabled
    HeaterEnabled = not HeaterEnabled
    if(HeaterEnabled):
        print("Heater is enabled")
        bHeat.configure(bg = "orange red", text = "Heater is Enabled")
        print(HeaterEnabled)
    else:
        print("Heater is disabled")
        print(HeaterEnabled)
        bHeat.configure(bg = "gray69", text = "Heater is Disabled")

def updateTarget():
    global Target
    Target = slTarget.get()
    print(Target)

def UpdateLabels():
    global Temps
    global HeaterOn
    
    if (HeaterOn[0]>0):
        lblHeatOn.configure(text = " ON ", bg = "orange red")
    else:
        lblHeatOn.configure(text = " OFF ", bg = "gray69")
    lblT1.configure(text = str(Temps[0]))
    lblT2.configure(text = str(Temps[1]))
    lblTint.configure(text = str(Temps[2]))
    main.after(567, UpdateLabels)
    

# --- Start Cereal Communication --- #
try: 
    serArd = serial.Serial("/dev/ttyACM0",9600)
except:
    print("ttyACM0 not available, attempting ttyACM1")
    serArd = serial.Serial("/dev/ttyACM1",9600)
    
serArd.baudrate = 9600
serArd.timeout = 5
time.sleep(2)
print("\nSerial connection success!\n")

# --- Make tk Window --- #
main = Tk()


# Info display labels
lblT1name = Label(main,text="T1: ")
lblT1name.grid(row=5, column = 5, sticky=E, padx = 10, pady = 5)
lblT2name = Label(main,text="T2: ")
lblT2name.grid(row=6, column = 5, sticky=E, padx = 10, pady = 5)
lblTintname = Label(main,text="Internal Temp: ")
lblTintname.grid(row=7, column = 5, sticky=E, padx = 10, pady = 5)

lblT1 = Label(main,text="XX.X", font= "TkDefaultFont 20 bold", bg = "chartreuse2")
lblT1.grid(row=5, column = 6, sticky=W, padx = 10, pady = 5)
lblT2 = Label(main,text="XX.X", font= "TkDefaultFont 20 bold", bg = "chartreuse2")
lblT2.grid(row=6, column = 6, sticky=W, padx = 10, pady = 5)
lblTint = Label(main,text="XX.X", font= "TkDefaultFont 20 bold", bg = "chartreuse2")
lblTint.grid(row=7, column = 6, sticky=W, padx = 10, pady = 5)

lblHeatOn = Label(main,text="Heater is: ")
lblHeatOn.grid(row=5, column = 7, padx = 10, pady = 5)
lblHeatOn = Label(main,text=" OFF ", font = "TkDefaultFont 22 bold", bg = "gray69")
lblHeatOn.grid(row=6, column = 7, padx = 10, pady = 5)

# Target label and slider
lblTarg = Label(main,text="Target Temperature")
lblTarg.grid(row=15, column = 5, sticky=E, padx = 10, pady = 5)

slTarget = Scale(
        main,
        orient=HORIZONTAL,
        length=200,
        from_=50,
        to_=212,
        command = lambda self: updateTarget())
slTarget.grid(row=14, column = 6,
     padx = 25, pady=10, rowspan = 3, columnspan = 3)
slTarget.set(170)



# Buttons
bHeat = Button(main,bg="gray69",text="Heater is Disabled",command= lambda: EnableHeater())
bHeat.grid(row=17,column=6)

main.after(3000, CerealComm) # After 3 seconds, Talk to the Arduino
main.after(567, UpdateLabels)

main.mainloop()



