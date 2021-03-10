import RPi.GPIO as GPIO
import time
import sys
from pygame import mixer


class BrewLogic():
    def __init__(self):
        # Set Up Pins
        self.heat1Pin = 20
        self.heat2Pin = 21
        GPIO.setup(self.heat1Pin, GPIO.OUT)
        GPIO.setup(self.heat2Pin, GPIO.OUT)
    def turn_heat_on(self):        
        GPIO.output(self.heat1Pin, True)
        GPIO.output(self.heat2Pin, True)

emergency_brew = BrewLogic()
print("Are you sure you want to turn on the heaters?")
time.sleep(1)
print("You have 10 seconds to cancel")
for i in range(0,10):
    print(str(10-i) + " seconds...")
    time.sleep(1)
emergency_Brew.turn_heat_on()