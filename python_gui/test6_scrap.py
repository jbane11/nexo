
import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import os
import csv
import numpy as np
import pandas as pd

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
appWidth, appHeight = 1400, 600

def close():
    exit()


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("test GUI")
        self.geometry(f"{appWidth}x{appHeight}")

        #setup frame
        self.setup_frame = ctk.CTkFrame(self)
        self.setup_frameLabel = ctk.CTkLabel(self, text = "SET UP", font = ("Arial", 20, "bold"))
        self.setup_frameLabel.grid(row=0, column=0, padx = 30, sticky = 'w')
        self.setup_frame.grid(row=1, column=0, rowspan = 8, columnspan = 3, padx = (10,0), sticky='ew')

        #laser frame
        self.laser_frame = ctk.CTkFrame(self)
        self.laser_frameLabel = ctk.CTkLabel(self, text="LASER", font = ("Arial", 20, "bold"))
        self.laser_frameLabel.grid(row=0, column=3, padx=30, sticky='w')
        self.laser_frame.grid(row=1, column=3, padx = (16, 4), sticky='ew')

        #target frame
        self.target_frame = ctk.CTkFrame(self)
        self.target_frameLabel = ctk.CTkLabel(self, text = "TARGETS", font = ("Arial", 20, "bold"))
        self.target_frameLabel.grid(row = 2, column=3, padx=30, sticky='w')
        self.target_frame.grid(row=3, column=3, padx = (16, 4), sticky='ew')

        #thermocoupler reading frame
        self.TC_frame = ctk.CTkFrame(self)
        self.TC_frameLabel = ctk.CTkLabel(self, text="TC READINGS", font=("Arial", 20, "bold"))
        self.TC_frameLabel.grid(row=0, column=5, padx=30, sticky='w')
        self.TC_frame.grid(row=1, column=5, rowspan=3, columnspan=2, padx=(16,4), pady = (0, 210), sticky="ew")

        #drift length and time frame
        self.drift_frame = ctk.CTkFrame(self)
        self.drift_frameLabel = ctk.CTkLabel(self, text="WINDOW + DRIFT LENGTH", font=("Arial", 20, "bold"))
        self.drift_frameLabel.grid(row=3, column=5, padx=30, pady=(0,150), sticky='w')
        self.drift_frame.grid(row=3, column=5, padx= (16,4), pady=(60, 0), sticky='ew')

        #notes frame
        self.notes_frame = ctk.CTkFrame(self)
        self.notes_frameLabel = ctk.CTkLabel(self, text = "NOTES", font = ("Arial", 20, "bold"))
        self.notes_frameLabel.grid(row=0, column=7, padx=30, sticky='w')
        self.notes_frame.grid(row=1, column=7, padx=(16, 4), pady = (0,50), sticky='ew')                                             


        #run number label
        self.numberLabel = ctk.CTkLabel(self.setup_frame, text = "Run Number")
        self.numberLabel.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        
        

#run entry
        #file for saved run number
        FILE_NAME = "saved_number.txt"

        #reads saved run number from file
        def read_saved_number():
            if os.path.exists(FILE_NAME):
                with open(FILE_NAME, "r") as file:
                    try:
                        return int(file.read())
                    except ValueError:
                        return 0  #default, displays if file is empty OR invalid
            return 777  #default, displays if file doesn't exist

        #saves current number to file
        def save_number():
            with open(FILE_NAME, "w") as file:
                file.write(entry_var.get())

        #increases run number
        def increase_number():
            current_value = int(entry_var.get())
            entry_var.set(current_value + 1)

        #decreases run number
        def decrease_number():
         current_value = int(entry_var.get())
         entry_var.set(current_value - 1)

        #reads saved number from file
        initial_value = read_saved_number()

        #entry box + buttons
        entry_var = ctk.StringVar(value=str(initial_value))
        self.numberEntry = ctk.CTkEntry(self.setup_frame, textvariable=entry_var, placeholder_text="Enter run number")
        self.numberEntry.grid(row=1, column=1, columnspan=1, padx=20, pady=20, sticky="w")

        increase_button = ctk.CTkButton(self.setup_frame, width=40, height = 30, text="+", font=("Arial", 16, "bold"), command=increase_number)
        increase_button.grid(row = 1, column= 2, padx= (0, 20), sticky = 'w')

        decrease_button = ctk.CTkButton(self.setup_frame, width=40, height=30, text="-", font=("Arial", 16, "bold"), command=decrease_number)
        decrease_button.grid(row=1, column = 2, padx = 10, sticky = "e")

        #binds save function to window close
        self.protocol("WM_DELETE_WINDOW", lambda: (save_number(), self.destroy()))


        #config number label
        self.configLabel = ctk.CTkLabel(self.setup_frame, text= "Configuration")
        self.configLabel.grid(row=2,column=0, padx = 20, pady = 20, sticky = "ew")

        #config number selection
        configEntry_var = ctk.StringVar()
        self.configEntry = ctk.CTkEntry(self.setup_frame, textvariable = configEntry_var, placeholder_text="Enter configuration number")
        self.configEntry.grid(row=2, column=1, columnspan=1, padx = 20, pady = 20, sticky="ew")

#GRID CONFIGURATION DROPDOWN      
        # need if statement that checks for different variations enabled for grid and run select
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
        self.dateLabel.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
#DATE BOX
        dateBox_var = ctk.StringVar()
        
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
        date_button.grid(row=3, column=2, padx=20, pady=20, sticky="ew")
        self.dateBox = ctk.CTkEntry(self.setup_frame, width = 100, height = 25, textvariable=dateBox_var, text_color='white')
        self.dateBox.grid(row = 3, column = 1, padx =20, pady =20, sticky = "ew")

        #binding callback to entry box to re-enable button when field is cleared
        self.dateBox.bind("<FocusOut>", check_date)

#LABELING AND PLACING STUFF
        #grid config label
        self.gridLabel = ctk.CTkLabel(self.setup_frame, text = "Select Grid Set-up")
        self.gridLabel.grid(row=4, column=0, padx = 20, pady = 20, sticky="ew")

        #grid config dropdown
        gridSelect_var1 = ctk.StringVar(value="Grid Number")
        self.gridSelect = ctk.CTkOptionMenu(self.setup_frame, variable = gridSelect_var1, values=["Single Grid - 20 mm", "Other"])
        self.gridSelect.grid(row=4, column=1, columnspan=1, padx = 20, pady=20, sticky="ew")
        gridSelect_var1.trace("w", gridruntype_entry)

        #test type label
        self.runLabel = ctk.CTkLabel(self.setup_frame, text = "Select Run Type")
        self.runLabel.grid(row=5, column=0, padx=20, pady=20, sticky="ew")
        

        #test type dropdown
        runSelect_var1 = ctk.StringVar(value="Run Type")
        self.runSelect = ctk.CTkOptionMenu(self.setup_frame, variable=runSelect_var1, values=["Test", "Commissioning", "Noise", "Production"])
        self.runSelect.grid(row=5, column=1, columnspan=1, padx=20, pady=20, sticky="ew")
        runSelect_var1.trace("w", gridruntype_entry)

        #anode voltage label
        self.anodeLabel = ctk.CTkLabel(self.setup_frame, text = "Anode Voltage")
        self.anodeLabel.grid(row=6, column=0, padx = 20, pady = 20, sticky='ew')

        #anode voltage select/entry
        anodeEntry_var = ctk.StringVar(value = "Enter in V")
        self.anodeEntry = ctk.CTkEntry(self.setup_frame, textvariable = anodeEntry_var, placeholder_text="Enter in V")
        self.anodeEntry.grid(row=6, column=1, columnspan=1, padx=20, pady=20, sticky='ew')

        #cathode voltage label
        self.cathodeLabel = ctk.CTkLabel(self.setup_frame, text = "Cathode Voltage")
        self.cathodeLabel.grid(row=7, column=0, padx =20, pady = 20, sticky='we')

        #cathode voltage select/entry
        cathodeEntry_var = ctk.StringVar(value = "Enter in V")
        self.cathodeEntry = ctk.CTkEntry(self.setup_frame, textvariable=cathodeEntry_var, placeholder_text="Enter in V")
        self.cathodeEntry.grid(row=7, column=1, columnspan=1, padx=20, pady=20, sticky='ew')

        #laser current label
        self.currentLabel = ctk.CTkLabel(self.laser_frame, text="Laser Current")
        self.currentLabel.grid(row=1, column=4, padx = 20, pady = 20, sticky = 'we')

        #laser current entry
        currentEntry_var = ctk.StringVar(value="Enter in A")
        self.currentEntry = ctk.CTkEntry(self.laser_frame, textvariable=currentEntry_var, placeholder_text="Enter in A")
        self.currentEntry.grid(row=1, column=5, padx = 20, pady = 20, sticky = 'ew')

        #laser frequency label
        self.frequencyLabel = ctk.CTkLabel(self.laser_frame, text = "Laser Frequency")
        self.frequencyLabel.grid(row=2, column=4, padx = 20, pady = 20, sticky = 'we')

        #laser frequency entry
        frequencyEntry_var = ctk.StringVar(value="Enter in Hz")
        self.frequencyEntry = ctk.CTkEntry(self.laser_frame, textvariable=frequencyEntry_var, placeholder_text = "Enter in Hz")
        self.frequencyEntry.grid(row=2, column=5, padx = 20, pady=20, sticky='ew')

        #media label
        self.mediaLabel = ctk.CTkLabel(self.setup_frame, text = 'Select Media')
        self.mediaLabel.grid(row=8, column=0, padx= 20, pady= 20, sticky='we')

        #media select
        mediaSelect_var = ctk.StringVar(value="Media")
        self.mediaSelect = ctk.CTkOptionMenu(self.setup_frame, variable=mediaSelect_var, values=["Vacuum", "Gas Xenon", "Liquid Xenon"])
        self.mediaSelect.grid(row=8, column=1, columnspan = 1, padx=20, pady=20, sticky='we')

        #target channel label
        self.targetChannelLabel = ctk.CTkLabel(self.target_frame, text = "Target Temp. Channel")
        self.targetChannelLabel.grid(row=4, column=3, padx = 20, pady = 20, sticky = 'we')

        #target channel select
        targetChannelSelect_var = ctk.StringVar(value="Select Channel")
        self.targetChannelSelect = ctk.CTkOptionMenu(self.target_frame, values=['4', '5'], variable = targetChannelSelect_var)
        self.targetChannelSelect.grid(row=4, column=4, columnspan = 1, padx = 20, pady = 20, sticky = 'ew')

        #target temperature label
        self.targetTempLabel = ctk.CTkLabel(self.target_frame, text = "Target Temperature")
        self.targetTempLabel.grid(row=5, column=3, padx=20, pady=20, sticky="we")

        #target temperature entry
        targetTempEntry_var = ctk.StringVar(value = "Enter in K")
        self.targetTempEntry = ctk.CTkEntry(self.target_frame, textvariable=targetTempEntry_var, placeholder_text="Enter in K")
        self.targetTempEntry.grid(row=5, column = 4, columnspan=1, padx=20, pady=20, sticky='ew')

        #target pressure label
        self.targetPressureLabel = ctk.CTkLabel(self.target_frame, text = "Target Pressure")
        self.targetPressureLabel.grid(row = 6, column = 3, padx=20, pady=20, sticky='we')

        #target pressure entry
        targetPressureEntry_var = ctk.StringVar(value = "Enter in psi")
        self.targetPressureEntry = ctk.CTkEntry(self.target_frame, textvariable=targetPressureEntry_var, placeholder_text= "Enter in psi")
        self.targetPressureEntry.grid(row = 6, column = 4, columnspan = 1, padx = 20, pady = 20, sticky='ew')

        #bottom thermocoupler label
        self.TC1Label = ctk.CTkLabel(self.TC_frame, text = "TC 1")
        self.TC1Label.grid(row=1, column=5, padx=20, pady=20, sticky='we')

        #bottom thermocoupler entry
        TC1Entry_var = ctk.StringVar(value="Enter in K")
        self.TC1Entry = ctk.CTkEntry(self.TC_frame, textvariable=TC1Entry_var, placeholder_text="Enter in K")
        self.TC1Entry.grid(row=1, column=6, columnspan = 1, padx = 20, pady=20, sticky='we')

        #mid thermocoupler label
        self.TC2Label = ctk.CTkLabel(self.TC_frame, text = "TC 2")
        self.TC2Label.grid(row=2, column=5, padx=20, pady=20, sticky='we')

        #mid thermocoupler entry
        TC2Entry_var = ctk.StringVar(value = "Enter in K")
        self.TC2Entry = ctk.CTkEntry(self.TC_frame, textvariable=TC2Entry_var, placeholder_text="Enter in K")
        self.TC2Entry.grid(row=2, column=6, columnspan = 1, padx = 20, pady=20, sticky='we')        
        
        #top thermocoupler label
        self.TC3Label = ctk.CTkLabel(self.TC_frame, text = "TC 3")
        self.TC3Label.grid(row=3, column=5, padx=20, pady=20, sticky='we')

        #top thermocoupler entry
        TC3Entry_var = ctk.StringVar(value = "Enter in K")
        self.TC3Entry = ctk.CTkEntry(self.TC_frame, textvariable=TC3Entry_var, placeholder_text="Enter in K")
        self.TC3Entry.grid(row=3, column=6, columnspan = 1, padx = 20, pady=20, sticky='we')

        #window label
        self.windowLabel = ctk.CTkLabel(self.drift_frame, text='Signal Window')
        self.windowLabel.grid(row=4, column=5, padx=20, pady=20, sticky = 'ew')

        #window entry/select
        windowEntry_var = ctk.StringVar(value='Enter in us or select')
        self.windowEntry = ctk.CTkComboBox(self.drift_frame, values=["25", "50", "100", "200"], variable=windowEntry_var)
        self.windowEntry.grid(row=4, column=6, columnspan = 1, padx=20, pady=20, sticky='we')

        #drift length label
        self.lengthLabel = ctk.CTkLabel(self.drift_frame, text = "Drift Length")
        self.lengthLabel.grid(row=5, column=5, padx = 20, pady=20, sticky="ew")

        #drift length entry/select
        lengthEntry_var = ctk.StringVar(value='Enter in mm or select')
        self.lengthEntry = ctk.CTkComboBox(self.drift_frame, values=['20'], variable=lengthEntry_var)
        self.lengthEntry.grid(row=5, column = 6, columnspan = 1, padx=20, pady=20, sticky='we')

        #notes
        self.notesEntry = ctk.CTkTextbox(self.notes_frame, height=100, width=200)
        self.notesEntry.grid(row=1, column=7, padx=20, pady=20)

#variables that store input
        #def fetch(info):
            #data = {}
            #for key, value in info.items():
                #data[key] = value.get()
            #print(data)
        
        self.input_data = {
            "Run No.":entry_var.get(),
            "Configuration No.":configEntry_var.get(), 
            "Date":dateBox_var.get(), 
            "Grid No.":gridSelect_var1.get(), 
            "Run Type":runSelect_var1.get(), 
            "Anode V":anodeEntry_var.get(), 
            "Cathode V":cathodeEntry_var.get(), 
            "Laser Current":currentEntry_var.get(), 
            "Laser Freq.":frequencyEntry_var.get(), 
            "Media":mediaSelect_var.get(), 
            "Target Channel":targetChannelSelect_var.get(), 
            "Target Pressure":targetTempEntry_var.get(), 
            "Target Temp.":targetPressureEntry_var.get(), 
            "TC1":TC1Entry_var.get(), 
            "TC2":TC2Entry_var.get(), 
            "TC3":TC3Entry_var.get(), 
            "Window":windowEntry_var.get(), 
            "Length":lengthEntry_var.get(),
        }
       
       #load saved data
        self.load_data()

        for key in self.input_data:
            value = self.input_data[key]
        
        testfilepath = os.path.join("C:/Users/jasonbane/Desktop/example_folder", "test_data_xyz.csv")
        #def csv_save_fct():
            #with open(testfilepath, 'wb') as file:
                #fetched = pd.DataFrame.from_dict(self.input_data, orient = "index")
                #.T.reset_index().to_csv("test_data_xyz.csv", header=False, index=False))
                #file.write(fetched).to_bytes("loremipsum.txt")
                #file.write("loremipsum.txt")


                #result = not all(self.input_data.values())
                #if result == True:
                    #pass

                    
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.protocol("WM_DELETE_WINDOW", self.csv_save_fct)

    #def csv_save_fct(self):
        #filename_test = "datatest.csv"
        #base_path = "C:/Users/jasonbane/Desktop/example_folder"        
        #filepath = os.path.join(base_path, filename_test)
        #field_names = ["Run No.",
                #
        #with open("datatest.csv", 'w', newline="\n") as csvfile:
            #writer = csv.writer(csvfile, fieldnames=field_names, delimiter="\n")
            #writer.writeheader()
            #writer.writerows(self.input_data)
            #print("Task successful")
            
            
    def load_data(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "user_data.txt"
        filepath = os.path.join(base_path, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                for key, var in self.input_data.items():
                    try:
                        return key, var
                    except FileNotFoundError or ValueError:
                        print("opening default")
                        pass
    
    def save_data(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "user_data.txt"
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w") as file:
            for key, var in self.input_data.items():
                file.write(f"{key}:{var}\n")
                print("Task successful")


    def on_closing(self):
        self.save_data()
        self.destroy()

#SAVE BUTTONS
    #define save button function
        #def save_button_press(*args):
            #with open(file_path, 'w') as file:
                #file.write("Example text")
            #print("Task performed successfully")


    #define closing function
        #def on_closing(*args):
            #self.destroy()


    #save buttons
        #self.saveButton = ctk.CTkButton(self, width = 40, height=40, corner_radius=40, text= "Save Run", font=("Arial", 16, "bold"))
        #self.saveButton.grid(row=2, column=7) #out of service

        #self.saveAsButton = ctk.CTkButton(self, width = 40, height = 40, corner_radius=40, text = "Save As...", font=("Arial", 16, "bold"))
        #self.saveAsButton.grid(row=3, column=7, pady=(0,160)) #not currently functional

    # Variables 
        #base_path = "C:/Users/jasonbane/Desktop/example_folder"
        #runnumber_to_string = str(entry_var.get())
        #date_to_string = str(dateBox_var.get())
        #config_to_string = str(configEntry_var.get())
        #filename_raw = (date_to_string, "-",config_to_string,"00",runnumber_to_string)
        #file_name1 = "".join(filename_raw)
        #final_csv = 
  
    # Using os.path.join() 
        #file_path = os.path.join(base_path, file_name1) 
  
    #closing event bound to method
        #self.protocol("WM_DELETE_WINDOW", on_closing)
 
if __name__ == "__main__":
    app = App()
    app.mainloop()