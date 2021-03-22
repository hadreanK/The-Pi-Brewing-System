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
from tkinter import messagebox

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
    def __init__(self, parent):
        #self.parent.brew_id = '' # string of the format 2103 - Fuggle IPA
        self.parent = parent
        self.log_folder = '/home/pi/Documents/Beer Maker/The-Pi-Brewing-System/Brew Logs/'
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
        self.temperature_history = [0, 0.0, 0]
        self.currently_logging = False
        self.date_format = "%Y-%m-%d - %Hh%M"
        
        
    def start_ferment_recording(self):
        # This method will begin the process for starting 
        # the fermentation record
        # If it's already been recording, then just continue
        print(self.parent.brew_id)
        if self.parent.brew_id == '':
            messagebox.showwarning('No Brew ID', "You must enter an ID for the brew you're makin!")
        else:
            self.open_log_file()
            self.currently_logging = False
            if self.log_file_exists:
                self.new_or_continue = 'continue'
                self.parse_log_file()
                self.currently_logging = True
            else:
                self.new_or_continue = 'new'
                temp_str = "No log file was found for " + self.parent.brew_id + ".\n\n Would you like to make a default file now?"
                response = messagebox.askquestion("No default file", temp_str)
                if response=="no":
                    messagebox.showinfo('Not logging',
                                    'Log file not created, not logging the brew.')
                else:
                    self.ferm_start_time = time.time()
                    self.write_default_file()
                    temp_str = 'Created log file for brew named:\n\n' + self.parent.brew_id + '\n\nPlease open the file and enter information about the recipe / fermentation schedule.'
                    messagebox.showinfo('File Created',temp_str)
                    self.currently_logging = False
                             
    
    def perform_logging_tasks(self):
        if self.currently_logging:
            temp_to_record = self.parent.therm.tempF[0]
            self.record_temperature(temp_to_record)

    def create_header(self):
        self.log_header.append('    HEADER')
        self.log_header.append('Brew Log written by Adrian Kirn')
        now = datetime.datetime.now()
        update_str = now.strftime(self.date_format)
        self.log_header.append('Last updated: ' + update_str)
        ferm_start_date = datetime.datetime.fromtimestamp(self.ferm_start_time)
        print(ferm_start_date)
        print('-------------')
        ferm_start_str = ferm_start_date.strftime(self.date_format)
        self.log_header.append('Fermentation started on: ' + ferm_start_str)
        
    def write_default_file(self):
        self.create_header()
        self.log_recipe.append('    RECIPE')
        self.log_temps.append('    TEMPS')
        self.log_temps.append('start_time: 0.0')
        self.log_temps.append('date/time  |  Temperature (F)')
        self.write_new_file(overwrite = False, backup_old_file=False)
        
        # Set everything back to 0 just to keep confusion down
        self.log_header = []
        self.log_temps = []
        self.log_recipe = []
        
    def set_filepaths(self):
        self.filepath = self.log_folder + self.parent.brew_id + ' - brew.log'
        self.backup_filepath = self.log_folder + self.parent.brew_id + ' - backup brew.log'
    
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
                        start_date_str = str(line.split(': ')[-1]) # Should be of the format of self.date_format, i.e. "%Y-%m-%d %Hh%M"
                        yr = int(start_date_str.split('-')[0]) # Year comes first
                        #mo = int(start_date_str.split('-')[1]) # Then month
                        self.fermet_start_time = datetime.timestamp(start_date_str)
                        
                elif section==1:
                    self.log_recipe.append(line)
                elif section==2:
                    self.log_temps.append(line)
                else:
                    print('Error reading file. Too many sections')
                    self.err = True
        # Parse the header
        

    def record_temperature(self, temperature):

        now_date = datetime.datetime.now()
        now_time = time.time()
        #date_str = now.strftime("%Y-%m-%d %Hh%M")
        temperature = round(temperature,1)
        current_hour = (now_time - self.ferm_start_time)/60
        # If this is the first recording of the hour, then make a new list entry
        if current_hour > len(self.temperature_history):
            self.temperature_history.append([0,0,0])
        # Average the temperatures etcd.

        #log_str = date_str + ', ' + str(temperature)
        #self.log_temps.append(log_str)
        #self.log_temps[-1] = log_str # RN it's putting a blank line at the end of the file
        # so by setting the last element it's not putting a line b/t each temp recording
        #self.write_new_file(overwrite=True, backup_old_file = True)

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
#brewy.write_default_file()
#brewy.start_ferment_recording()
#brewy.temperature_reading = 63.0

#brewy.record_temperature(63.1865)
#brewy.write_new_file(backup_old_file=True)


#print(brewy.log_header)
#print(brewy.log_recipe)
#print(brewy.log_temps)


