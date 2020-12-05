#http://thinkingtkinter.sourceforge.net/all_programs.html
from tkinter import *

class Brasseur:
    def __init__(self, parent):
        
        # Instance variables
        self.temps = [0.0, 0.0, 0.0] #TA, TB, int
        
        
        
        
        self.myParent = parent
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()
        
        self.button1 = Button(self.myContainer1, command=lambda
                              arg1 = 1: self.buttonClick(arg1))
        self.button1["text"] = "Bonjour Terre"
        self.button1["background"] = "blue"
        self.button1.pack(side = LEFT)
        self.button1.focus_force()
        
        self.button2 = Button(self.myContainer1,text = "close, then eat", \
                              background = "red", \
                              command = lambda
                              arg1 = 2: self.buttonClick(arg1))
        self.button2.pack(side = RIGHT)

    
    def buttonClick(self, buttonID):
        if(buttonID==1):
            print("Button #1 clicked")
        elif(buttonID==2):
            print("Button #2 clicked")
        else:
            print("Some other button clicked...")

root = Tk()
myapp = MyApp(root)
root.mainloop

