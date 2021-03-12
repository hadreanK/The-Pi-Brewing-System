'''
Functions:
1.  Create default file
a.  Have a warning if the file already exists
b.  Makes the default file so I can go in and add the recipe
2.  Start/continue ferment recording
a.  If there isn’t a ferment start time, then make now the start time 


'''


import time
import datetime
import shutil

def write_string_to_file(filepath,string):
    """-----------------------------------
    Written by Adrian Kirn on or around 31 January, 2021
    Purpose: This function writes a list of strings to a file

    Inputs: The filepath to write to, and the string or list of
            strings to write
    Output: The file with the strings in it
    Note: The containing folder must already exist.
    -----------------------------------"""  
    f = open(filepath,'w') # Open the file for editing
    if(isinstance(string,list)): # If it's a list, then write each line
        for line in string:
            f.write(line + '\n')
    else: # Otherwise write just the string
        f.write(string)
    f.close() # Close the file

class BrewLog():
    def __init__(self):
        self.brew_id = '' # string of the format 2103 - Fuggle IPA
        self.filepath = ''
        self.backup_filepath = ''
        self.log_file_exists = False
        self.new_or_continue = ''
        self.imported_log_file_text = []
        self.new_log_file_text = []
        self.log_header = [] 
        self.log_recipe = []
        self.log_temps = []
        self.ferm_start_time = 0
        self.section_break = '\n-------------\n'
        self.err = False
        self.temperature_reading = 0.0
        self.temperature_history = []
    
    def start_ferment_recording(self):
        # This method will begin the process for starting 
        # the fermentation record
        # If it's already been recording, then just continue
        
        self.open_log_file()
        
        if self.log_file_exists:
            self.new_or_continue = 'continue'
            self.parse_log_file()
            
        else:
            self.new_or_continue = 'new'
            #self.ferm_start_time = time.time()
            #self.write_default_file()
            self.err = True
            print('No file detected, please make a default file.')
        

            

    def create_header(self):
        self.log_header.append('    HEADER')
        self.log_header.append('Brew Log written by Adrian Kirn')
        now = datetime.datetime.now()
        update_str = now.strftime("%Y-%m-%d %Hh%M")
        self.log_header.append('Last updated: ' + update_str)
        start_date = datetime.fromtimestamp(self.ferm_start_time)
        start_str = start_date.strftime("%Y-%m-%d %Hh%M")
        self.log_header.append('Fermentation started on:' + start_str)
        
    def write_default_file(self):
        self.create_header()
        self.log_recipe.append('    RECIPE')
        self.log_temps.append('    TEMPS')
        self.log_temps.append('start_time: 0.0')
        self.log_temps.append('date/time  |  Temperature (F)')
        self.write_new_file(False)
        
        # Set everything back to 0 just to keep confusion down
        self.log_header = []
        self.log_temps = []
        self.log_recipe = []
        
    def set_filepaths(self):
        self.filepath = './' + self.brew_id + ' - brew.log'
        self.backup_filepath = './' + self.brew_id + ' - backup brew.log'
    
    def open_log_file(self):
        # This will open the log file and import the text into self.imported_log_file_text
        self.set_filepaths()

        try:
            f = open(self.filepath,'r') # Open the file for reading only
            self.log_file_exists = True
        except:
            print('Log file does not exist.')
            self.log_file_exists = False

        if self.log_file_exists:
            self.imported_log_file_text = f.read().split('\n')    
        
    def parse_log_file(self):
        section = 0 # This is the section currently bieng read
        #0 is header, 1 is recipe, 2 is temps
        for line in self.imported_log_file_text:
            if '-----' in line:
                section = section + 1
            else: #if it's not a section break, then make record it
                if section==0:
                    self.log_header.append(line)
                    if 'Fermentation started on:' in line:
                        self.ferm_start_time = str(line.split(':')[-1])
                        print(self.ferm_start_time)
                elif section==1:
                    self.log_recipe.append(line)
                elif section==2:
                    self.log_temps.append(line)
                else:
                    print('Error reading file. Too many sections')
                    self.err = True
        # Parse the header
        

    def record_temperature(self, temperature):
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d %Hh%M")
        temperature = round(temperature,1)
        log_str = date_str + ', ' + str(temperature)
        #self.log_temps.append(log_str)
        self.log_temps[-1] = log_str # RN it's putting a blank line at the end of the file
        # so by setting the last element it's not putting a line b/t each temp recording
            
    def write_new_file(self, overwrite=True, backup_old_file = False):
        self.set_filepaths()
        if backup_old_file:
            shutil.copy(self.filepath,self.backup_filepath)
        
        # Concatenate all the stuff
        self.new_log_file_text = self.log_header
        self.new_log_file_text.append(self.section_break)
        for line in self.log_recipe:
            self.new_log_file_text.append(line)
        self.new_log_file_text.append(self.section_break)
        for line in self.log_temps:
            self.new_log_file_text.append(line)
        
        write_string_to_file(self.filepath,self.new_log_file_text)
        print("Wrote log file to " + self.filepath)

    
        
print("Imported brew logging module")

# ### DEBUG
brewy = BrewLog()
brewy.brew_id = '2103 - Fuggle IPA'
#brewy.write_default_file()
brewy.start_ferment_recording()
#brewy.temperature_reading = 63.0

#brewy.record_temperature(63.1865)
#brewy.write_new_file(backup_old_file=True)


print(brewy.log_header)
#print(brewy.log_recipe)
#print(brewy.log_temps)


