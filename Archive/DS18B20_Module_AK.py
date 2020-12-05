import glob
import time

def getAllDevices():
    temp_files = []
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')
    for folder in device_folders:
        temp_file = folder + '/temperature'
        temp_files.append(temp_file)
    return(temp_files)

def getAllTemps(conv_to_degF):
    temps = []
    for file in getAllDevices():
        f = open(file, 'r')
        line = f.readlines()
        f.close()
        temp = float(line[0])
        temp = temp / 1000.0 # Get temp in celcius
        if(conv_to_degF):
            temp = temp * 9 / 5 + 32
        temps.append(temp)
    return(temps)

def getLabelledTemps(conv_to_degF):
    raw = getAllTemps(conv_to_degF)
    # 0 -> A
    # 1 -> Internal
    # 2 -> B
    labelled = [ ['A', raw[0]], \
                 ['B', raw[2]], \
                 ['internal', raw[1]]]
    return(labelled)
    
    
def getFirstTemp(conv_to_degF):
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/temperature'
    
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    
    temp = float(lines[0])
    temp = temp / 1000.0 # Get temp in celcius
    if(conv_to_degF):
        temp = temp * 9 / 5 + 32
    
    return(temp)

print("DS12B20 Module Loaded.")