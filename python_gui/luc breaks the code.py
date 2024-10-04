
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import os
import csv
import numpy as np
import pandas as pd

#sets appearance of app (geometry, color, etc.)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#exits app upon close (redundant)
def close():
    exit()

#defines the App class as a customtkinter class
class App(ctk.CTk):
    #define initialization function (i.e, what happens when the app initializes or opens)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)


#OVERALL SETUP (frames and their labels)
        self.title("Run GUI")
        self.geometry("1100x600")

        #setup frame
        self.setup_frame = ctk.CTkFrame(self)
        self.setup_frameLabel = ctk.CTkLabel(self, text = "SET UP", font = ("Arial", 20, "bold"))
        self.setup_frameLabel.grid(row=0, column=0, sticky = 'nsew')
        self.setup_frame.grid(row=1, column=0, padx=5, pady=5, sticky='new')
        self.setup_frame.grid_columnconfigure(0, weight=1)
        self.setup_frame.grid_rowconfigure(0, weight=1)

        #run data frame
        self.rundata_frame = ctk.CTkFrame(self)
        self.rundata_frameLabel = ctk.CTkLabel(self, text="RUN DATA", font = ("Arial", 20, "bold"))
        self.rundata_frameLabel.grid(row=0, column=1, sticky='nsew')
        self.rundata_frame.grid(row=1, column=1, padx=5, pady=5, sticky='new')
        self.rundata_frame.grid_columnconfigure(0, weight=1)
        self.rundata_frame.grid_rowconfigure(0, weight=1)


        #oscilloscope and notes frame
        self.oscillo_frame = ctk.CTkFrame(self)
        self.oscillo_frameLabel = ctk.CTkLabel(self, text="OSCILLO/NOTES", font=("Arial", 20, "bold"))
        self.oscillo_frameLabel.grid(row=0, column=2, sticky='nsew')
        self.oscillo_frame.grid(row=1, column=2, padx=5, pady=5, sticky='new')
        self.oscillo_frame.grid_columnconfigure(0, weight=1)
        self.oscillo_frame.grid_rowconfigure(0, weight=1)



#***IMPORTANT FOR LOAD DATA*** - defines the array that populates the entry boxes upon initializing of the app
        initial_array = ['247','','','','','Enter in V','Enter in V','Enter in A','Enter in Hz','','','Enter in K','Enter in PSI','Enter in K','Enter in K','Enter in K','Enter in us or select','Enter in mm or select','']
        data = self.load_data_to_arr(self.load_data())
        #checks each index in the length of the array called by the load_data and load_data_to_arr functions for a character length greater than 0 >
        #if that is true, it appends the data to the initial array index that matches it
        for i in range(len(data)):
            if len(data[i]) > 0:
                initial_array[i] = data[i]

#LABELING AND PLACING STUFF - placing all of the entry boxes and labels INSIDE the already defined frames. this part is hellish
        #run number label
        self.numberLabel = ctk.CTkLabel(self.setup_frame, text = "Run Number")
        self.numberLabel.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        #run entry
        #increases run number
        def increase_number():
            current_value = int(entry_var.get())
            entry_var.set(current_value + 1)

        #decreases run number
        def decrease_number():
         current_value = int(entry_var.get())
         entry_var.set(current_value - 1)

        #run entry box + buttons
        entry_var = ctk.StringVar(value=initial_array[0])
        self.numberEntry = ctk.CTkEntry(self.setup_frame, textvariable=entry_var, placeholder_text="Enter run number")
        self.numberEntry.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        increase_button = ctk.CTkButton(self.setup_frame, width=40, height = 30, text="+", font=("Arial", 16, "bold"), command=increase_number)
        increase_button.grid(row = 0, column= 2, padx= (0, 20), sticky = 'w')

        decrease_button = ctk.CTkButton(self.setup_frame, width=40, height=30, text="-", font=("Arial", 16, "bold"), command=decrease_number)
        decrease_button.grid(row=0, column = 2, padx = 10, sticky = "e")


        #config number label
        self.configLabel = ctk.CTkLabel(self.setup_frame, text= "Configuration")
        self.configLabel.grid(row=1,column=0, padx = 20, pady = 20, sticky = "ew")

        #config number selection
        configEntry_var = ctk.StringVar()
        self.configEntry = ctk.CTkEntry(self.setup_frame, textvariable = configEntry_var, placeholder_text="Enter configuration number")
        self.configEntry.grid(row=1, column=1, padx = 20, pady = 20, sticky="ew")

        #GRID CONFIGURATION DROPDOWN      
        # if statement that checks for different variations enabled for grid and run select to spit out a corresponding configuration number
        def gridruntype_entry(*args):
            if gridSelect_var1.get() == "Single Grid - 20 mm" and runSelect_var1.get() == "Production":
                configEntry_var.set("131")
            elif gridSelect_var1.get() == "Single Grid - 20 mm" and runSelect_var1.get() == "Noise":
                configEntry_var.set("231")
            elif gridSelect_var1.get() == "Single Grid - 20 mm" and runSelect_var1.get() == "Test" or runSelect_var1.get() == "Commissioning":
                configEntry_var.set("031")
            else:
                configEntry_var.set("")

        #date label
        self.dateLabel = ctk.CTkLabel(self.setup_frame, text = "Date")
        self.dateLabel.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        #date bawx
        dateBox_var = ctk.StringVar(value=initial_array[2])
        
        #date button press function
        def date_button_press():
            formatted_date = datetime.now().strftime("%Y%m%d")
            dateBox_var.set(formatted_date)
            date_button.configure(state=ctk.NORMAL)
        
        #check for date
        def check_date(*args):
            if not dateBox_var.get():
                date_button.configure(state=ctk.NORMAL)
            else:
                date_button.configure(state=ctk.DISABLED)
        
        #date button and box
        date_button = ctk.CTkButton(self.setup_frame, width=56, height=30, text = "Today", command=date_button_press)
        date_button.grid(row=2, column=2, padx=20, pady=20, sticky="ew")
        self.dateBox = ctk.CTkEntry(self.setup_frame, width = 100, height = 25, textvariable=dateBox_var, text_color='white')
        self.dateBox.grid(row = 2, column = 1, padx =20, pady =20, sticky = "ew")

        #binding callback to entry box to re-enable button when field is cleared
        self.dateBox.bind("<FocusOut>", check_date)

        #grid config label
        self.gridLabel = ctk.CTkLabel(self.setup_frame, text = "Select Grid Set-up")
        self.gridLabel.grid(row=3, column=0, padx = 20, pady = 20, sticky="ew")

        #grid config dropdown
        gridSelect_var1 = ctk.StringVar(value ="Grid Number")
        self.gridSelect = ctk.CTkOptionMenu(self.setup_frame, variable = gridSelect_var1, values=["Single Grid - 20 mm", "Other"])
        self.gridSelect.grid(row=3, column=1, padx = 20, pady=20, sticky="ew")
        gridSelect_var1.trace("w", gridruntype_entry)

        #test type label
        self.runLabel = ctk.CTkLabel(self.setup_frame, text = "Select Run Type")
        self.runLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        

        #test type dropdown
        runSelect_var1 = ctk.StringVar(value="Run Type")
        self.runSelect = ctk.CTkOptionMenu(self.setup_frame, variable=runSelect_var1, values=["Test", "Commissioning", "Noise", "Production"])
        self.runSelect.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
        runSelect_var1.trace("w", gridruntype_entry)

        #anode voltage label
        self.anodeLabel = ctk.CTkLabel(self.setup_frame, text = "Anode Voltage")
        self.anodeLabel.grid(row=5, column=0, padx = 20, pady = 20, sticky='ew')

        #anode voltage select/entry
        anodeEntry_var = ctk.StringVar(value=initial_array[5])
        self.anodeEntry = ctk.CTkEntry(self.setup_frame, textvariable = anodeEntry_var, placeholder_text="Enter in V")
        self.anodeEntry.grid(row=5, column=1, padx=20, pady=20, sticky='ew')

        #cathode voltage label
        self.cathodeLabel = ctk.CTkLabel(self.setup_frame, text = "Cathode Voltage")
        self.cathodeLabel.grid(row=6, column=0, padx =20, pady = 20, sticky='we')

        #cathode voltage select/entry
        cathodeEntry_var = ctk.StringVar(value=initial_array[6])
        self.cathodeEntry = ctk.CTkEntry(self.setup_frame, textvariable=cathodeEntry_var, placeholder_text="Enter in V")
        self.cathodeEntry.grid(row=6, column=1, padx=20, pady=20, sticky='ew')

        #media label
        self.mediaLabel = ctk.CTkLabel(self.setup_frame, text = 'Select Media')
        self.mediaLabel.grid(row=7, column=0, padx= 20, pady= 20, sticky='we')

        #media select
        mediaSelect_var = ctk.StringVar(value="Media")
        self.mediaSelect = ctk.CTkOptionMenu(self.setup_frame, variable=mediaSelect_var, values=["Vacuum", "Gas Xenon", "Liquid Xenon"])
        self.mediaSelect.grid(row=7, column=1, padx=20, pady=20, sticky='we')

        #laser current label
        self.currentLabel = ctk.CTkLabel(self.rundata_frame, text="Laser Current")
        self.currentLabel.grid(row=0, column=0, padx = 20, pady = 20, sticky = 'we')

        #laser current entry
        currentEntry_var = ctk.StringVar(value=initial_array[7])
        self.currentEntry = ctk.CTkEntry(self.rundata_frame, textvariable=currentEntry_var, placeholder_text="Enter in A")
        self.currentEntry.grid(row=0, column=1, padx = 20, pady = 20, sticky = 'ew')

        #laser frequency label
        self.frequencyLabel = ctk.CTkLabel(self.rundata_frame, text = "Laser Frequency")
        self.frequencyLabel.grid(row=1, column=0, padx = 20, pady = 20, sticky = 'we')

        #laser frequency entry
        frequencyEntry_var = ctk.StringVar(value=initial_array[8])
        self.frequencyEntry = ctk.CTkEntry(self.rundata_frame, textvariable=frequencyEntry_var, placeholder_text = "Enter in Hz")
        self.frequencyEntry.grid(row=1, column=1, padx = 20, pady=20, sticky='ew')


        #target channel label
        self.targetChannelLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Temp. Channel")
        self.targetChannelLabel.grid(row=2, column=0, padx = 20, pady = 20, sticky = 'we')

        #target channel select
        targetChannelSelect_var = ctk.StringVar(value="Select Channel")
        self.targetChannelSelect = ctk.CTkOptionMenu(self.rundata_frame, values=['4', '5'], variable = targetChannelSelect_var)
        self.targetChannelSelect.grid(row=2, column=1, padx = 20, pady = 20, sticky = 'ew')

        #target temperature label
        self.targetTempLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Temperature")
        self.targetTempLabel.grid(row=3, column=0, padx=20, pady=20, sticky="we")

        #target temperature entry
        targetTempEntry_var = ctk.StringVar(value=initial_array[11])
        self.targetTempEntry = ctk.CTkEntry(self.rundata_frame, textvariable=targetTempEntry_var, placeholder_text="Enter in K")
        self.targetTempEntry.grid(row=3, column = 1, padx=20, pady=20, sticky='ew')

        #target pressure label
        self.targetPressureLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Pressure")
        self.targetPressureLabel.grid(row = 4, column = 0, padx=20, pady=20, sticky='we')

        #target pressure entry
        targetPressureEntry_var = ctk.StringVar(value=initial_array[12])
        self.targetPressureEntry = ctk.CTkEntry(self.rundata_frame, textvariable=targetPressureEntry_var, placeholder_text= "Enter in psi")
        self.targetPressureEntry.grid(row = 4, column = 1, padx = 20, pady = 20, sticky='ew')

        #bottom thermocoupler label
        self.TC1Label = ctk.CTkLabel(self.rundata_frame, text = "TC 1")
        self.TC1Label.grid(row=5, column=0, padx=20, pady=20, sticky='we')

        #bottom thermocoupler entry
        TC1Entry_var = ctk.StringVar(value=initial_array[13])
        self.TC1Entry = ctk.CTkEntry(self.rundata_frame, textvariable=TC1Entry_var, placeholder_text="Enter in K")
        self.TC1Entry.grid(row=5, column=1, padx = 20, pady=20, sticky='we')

        #mid thermocoupler label
        self.TC2Label = ctk.CTkLabel(self.rundata_frame, text = "TC 2")
        self.TC2Label.grid(row=6, column=0, padx=20, pady=20, sticky='we')

        #mid thermocoupler entry
        TC2Entry_var = ctk.StringVar(value=initial_array[14])
        self.TC2Entry = ctk.CTkEntry(self.rundata_frame, textvariable=TC2Entry_var, placeholder_text="Enter in K")
        self.TC2Entry.grid(row=6, column=1, padx = 20, pady=20, sticky='we')        
        
        #top thermocoupler label
        self.TC3Label = ctk.CTkLabel(self.rundata_frame, text = "TC 3")
        self.TC3Label.grid(row=7, column=0, padx=20, pady=20, sticky='we')

        #top thermocoupler entry
        TC3Entry_var = ctk.StringVar(value=initial_array[15])
        self.TC3Entry = ctk.CTkEntry(self.rundata_frame, textvariable=TC3Entry_var, placeholder_text="Enter in K")
        self.TC3Entry.grid(row=7, column=1, padx = 20, pady=20, sticky='we')

        #window label
        self.windowLabel = ctk.CTkLabel(self.oscillo_frame, text='Signal Window')
        self.windowLabel.grid(row=0, column=0, padx=20, pady=20, sticky = 'ew')

        #window entry/select
        windowEntry_var = ctk.StringVar(value=initial_array[16])
        self.windowEntry = ctk.CTkComboBox(self.oscillo_frame, values=["25", "50", "100", "200"], variable=windowEntry_var)
        self.windowEntry.grid(row=0, column=1, padx=20, pady=20, sticky='we')

        #drift length label
        self.lengthLabel = ctk.CTkLabel(self.oscillo_frame, text = "Drift Length")
        self.lengthLabel.grid(row=1, column=0, padx = 20, pady=20, sticky="ew")

        #drift length entry/select
        lengthEntry_var = ctk.StringVar(value=initial_array[17])
        self.lengthEntry = ctk.CTkComboBox(self.oscillo_frame, values=['20'], variable=lengthEntry_var)
        self.lengthEntry.grid(row=1, column = 1, padx=20, pady=20, sticky='we')

        #notes
        notesEntry_var = ctk.StringVar(value=initial_array[18])
        self.notesEntry = ctk.CTkEntry(self.oscillo_frame, textvariable=notesEntry_var, height=100, width=200)
        self.notesEntry.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        #query box all code (i dont feel like separating it)
        # querybox_label = ctk.CTkLabel(self.oscillo_frame, text = "Search Database", bg_color="gray30")
        # querybox_label.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="we")
        # querybox_var = ctk.StringVar()
        # querybox_entry = ctk.CTkComboBox(self.oscillo_frame, values=

#STORING INPUT DATA
        #this dictionary takes all of the string variables defined for each entry field and assigns them a plaintext key
        self.input_data = {
            "Run No.":entry_var,
            "Configuration No.":configEntry_var, 
            "Date":dateBox_var, 
            "Grid No.":gridSelect_var1, 
            "Run Type":runSelect_var1, 
            "Anode V":anodeEntry_var, 
            "Cathode V":cathodeEntry_var, 
            "Laser Current":currentEntry_var, 
            "Laser Freq.":frequencyEntry_var, 
            "Media":mediaSelect_var, 
            "Target Channel":targetChannelSelect_var, 
            "Target Temp.":targetTempEntry_var, 
            "Target Pressure":targetPressureEntry_var, 
            "TC1":TC1Entry_var, 
            "TC2":TC2Entry_var, 
            "TC3":TC3Entry_var, 
            "Window":windowEntry_var, 
            "Length":lengthEntry_var,
            "Notes":notesEntry_var
        }

#***SAVE AND LOAD DATA FUNCTIONS*** and SAVE BUTTONS (technically this should be up w setup) 
    #on closing function
        def on_closing(*args):
            self.destroy()
    
    #placing buttons, assigning SAVE CSV command to it
        self.saveButton = ctk.CTkButton(self.oscillo_frame, width = 40, height=40, corner_radius=20, text= "Save Run", font=("Arial", 16, "bold"), command=self.save_csv)
        self.saveButton.grid(row=3, column=0, columnspan=2, padx=5, pady=5)


    #closing events bound to method (imma be real i have no clue which of these actually does something i'll debug later)
        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    #LOADS data from txt file to repopulate in entry fields
    def load_data(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "user_data.txt"
        filepath = os.path.join(base_path, filename)
        with open(filepath, "r") as file:
            return file.read()

    #takes data from load_data and loads it to an ARRAYYYY (thank u loick U ROCK) - this is so input data can be easily appended and so it behaves better when saved to a plaintxt file
    def load_data_to_arr(self, string):
        temp = string.split('\n')
        for i in range(len(temp)):
            if len(temp[i].split(':'))>1:
                temp[i] = temp[i].split(':')[1] 
        return temp
    
    #paired with load data - SAVES values to plaintext file; however note that this DOES NOT PULL FROM THE ARRAY. this pulls from the input_data DICTIONARY (gets the value of the stringvariables upon closing)
    #the ARRAY loads from the TEXT FILE that is populated by pulling stuff from the DICTIONARY
    #print statements are for debug but i am leaving them 4 proof that the functions are still working as intended

    def save_data(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "user_data.txt"
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w") as file:
            for key, var in self.input_data.items():
                file.write(f"{key}:{var.get()}\n")
        print("data save successful")

    #SEPARATE from save/load_data fcts. this SAVES all entry fields to the NAMED CSV. separated columnar by commas and placed into one ROW for each run
    #if the csv file doesn't exist (i delete it often for testing), it creates one
    #if it DOES exist, it APPENDS to a new row
    def save_csv(self):
        # print(self.input_data.get("Run No."))
        # self.input_data.update("Run No."==int(str((self.input_data.get('Run No.')))+1))
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "test_csv.csv"
        filepath = os.path.join(base_path, filename)
        with open(filepath, "a") as file:
            for key, var in self.input_data.items():
                file.write(f"{var.get()},")
            file.write("\n")
        print("csv save successful")


#QUERY BOX loose code
    base_path = "C:/Users/jasonbane/Desktop/example_folder"
    filename = "test_csv.csv"
    filepath = os.path.join(base_path, filename)

    # with open(filepath, "rt") as c:
    #     stringfromcsv = c.readlines()
    # if str("131") in str(stringfromcsv):
    #     print("True")
    # else:
    #     print("False")

    #i have no idea what this does :P debug l8r
    def on_opening(self):
        self.__init__()

    #binds the previously defined save data fct (to text file) to the closing of the app so it is automatic (reminder: csv is NOT automatic)
    def on_closing(self):
        self.save_data()
        self.destroy()
 
#close-out/runs app fct as loop. also splits stuff for load_data fct
if __name__ == "__main__":
    
    app = App()
    string = app.load_data()
    split = app.load_data_to_arr(string)
    print(split)
    app.mainloop()