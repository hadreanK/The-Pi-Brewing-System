from subprocess import Popen, PIPE
from time import sleep
from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

def initLCD():
    # Modify this if you have a different sized character LCD
    lcd_columns = 16
    lcd_rows = 2

    # compatible with all versions of RPI as of Jan. 2019
    # v1 - v3B+
    lcd_rs = digitalio.DigitalInOut(board.D22)
    lcd_en = digitalio.DigitalInOut(board.D17)
    lcd_d4 = digitalio.DigitalInOut(board.D25)
    lcd_d5 = digitalio.DigitalInOut(board.D24)
    lcd_d6 = digitalio.DigitalInOut(board.D23)
    lcd_d7 = digitalio.DigitalInOut(board.D18)

    # Initialise the lcd class
    lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
                                          lcd_d7, lcd_columns, lcd_rows)
    return(lcd)

# looking for an active Ethernet or WiFi device
def find_interface():
    find_device = "ip addr show"
    interface_parse = run_cmd(find_device)
    for line in interface_parse.splitlines():
        if "state UP" in line:
            dev_name = line.split(':')[1]
    return dev_name

# find an active IP on the first LIVE network device
def parse_ip(interface):
    find_ip = "ip addr show %s" % interface
    find_ip = "ip addr show %s" % interface
    ip_parse = run_cmd(find_ip)
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]
    return ip

# run unix shell command, return as ASCII
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')

def printIP(lcd):
    interface = find_interface()
    ip_address = parse_ip(interface)
    lcd.clear()
    lcd.message = "Pi's IP:\n  " + ip_address
# wipe LCD screen before we start

def welcomeScreen(lcd, delay):
    print("Dislaying welcome screen and PI's IP address.")
    lcd.clear()
    lcd.message = "Welcome to..."
    sleep(delay)
    lcd.message = lcd.message + "\n Beer Making!"
    sleep(delay)
    printIP(lcd)
   # print(lcd.message)
    sleep(delay)
    
def dispTemps(lcd, temps, target, heatOn, dTAdt):
    TA = temps[0]
    TB = temps[1]
    Tint = temps[1]
    strHeatOn = "OFF"
    
    if(heatOn):
        strHeatOn = " ON"
    # Display the temps
    line1 = "A:%2.1f x:%d %3.2f" % (TA, target, dTAdt)
    line2 = "%2.1f  %d %s" % (TB, Tint, strHeatOn)
    lcd.message = line1 + "     \n" + line2 + "        "
    #print(lcd.message)
    
    
print("LCD1602 Module Loaded")
