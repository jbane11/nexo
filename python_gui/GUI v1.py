
import customtkinter as ctk
from datetime import datetime
import os
import csv
from CTkMessagebox import CTkMessagebox
from CTkToolTip import *
import json

with open("fileconfig.json") as json_conf:
    path_config = json.load(json_conf)

#sets appearance of app (geometry, color, etc.)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class searchframe(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # Label and Entry for queries
        self.query_label = ctk.CTkLabel(self, text="Enter queries (comma-separated):")
        self.query_label.pack(pady=5)
        self.entry = ctk.CTkEntry(self, width=150)
        self.entry.pack(pady=5)

        # Search Button
        self.search_button = ctk.CTkButton(self, text="SEARCH", command=self.search_and_display)
        self.search_button.pack(pady=10)

        # Result Textbox
        self.result_label = ctk.CTkLabel(self, text="Search Results:")
        self.result_label.pack(pady=5)
        self.result_textbox = ctk.CTkTextbox(self, state="normal", height=238, width=300)
        self.result_textbox.pack(padx=10, pady=10)

    def search_and_display(self):
        base_path = format(path_config["base_path"])
        filename = format(path_config["filename"])
        queries = self.get_queries()

        results_text = self.search_csv(base_path, filename, queries)
        self.result_textbox.delete('1.0', 'end')
        self.result_textbox.insert('end', results_text)

    def get_queries(self):
        entry_text = self.entry.get()
        queries = entry_text.split(',')
        return [query.strip() for query in queries]

    def search_csv(self, base_path, filename, queries):
        filepath = os.path.join(base_path, filename)
        results = []

        try:
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                headers = next(reader)  # Read header row

                for query in queries:
                    query = query.strip()

                    found_runs = set()
                    found_rows = []

                    file.seek(0)  # Reset file pointer to the beginning

                    for row in reader:
                        if any(query.lower() in field.lower() for field in row):
                            run_id = int(row[0])
                            if run_id not in found_runs:
                                found_runs.add(run_id)
                                found_rows.append(f"RUN {run_id}: [{', '.join(row)}]\n")

                    if found_rows:
                        # Adding 3 newlines before the block header for extra spacing
                        results.append(f"\n\nRUN(S) MATCHING '{query}':\n")
                        # Add 2 newlines after each RUN #: line for extra spacing
                        results.extend([f"{line}\n\n" for line in found_rows])
                        # Adding 3 newlines after each block for extra spacing
                        results.append("\n\n")
                    else:
                        # Adding 3 newlines before the "No matching run" message for extra spacing
                        results.append(f"\n\nNO MATCHING RUN FOR '{query}'\n\n")  # 3 newlines after "No matching run"

            return "".join(results)

        except FileNotFoundError:
            return f"File '{filename}' not found."
        except Exception as e:
            return f"An error occurred: {str(e)}"


def show_search_frame():
    search_self = ctk.CTk()
    search_self.title("CSV Search Tool")

    customframe = searchframe(search_self)
    customframe.grid(padx=20, pady=20)

    search_self.mainloop()

#exits app upon close (redundant)
def close():
    exit()

#defines the App class
class App(ctk.CTk):
    #define initialization function (i.e, what happens when the app initializes or opens)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)

#OVERALL SETUP (frames and their labels)
        self.title("Run GUI")
        self.geometry("1260x740")

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


        #notes frame
        self.notes_frame = ctk.CTkFrame(self)
        self.notes_frameLabel = ctk.CTkLabel(self, text="NOTES + SEARCH", font=("Arial", 20, "bold"))
        self.notes_frameLabel.grid(row=0, column=2, sticky='nsew')
        self.notes_frame.grid(row=1, column=2, padx=5, pady=5, sticky='new')
        self.notes_frame.grid_columnconfigure(0, weight=1)
        self.notes_frame.grid_rowconfigure(0, weight=1)



#***IMPORTANT FOR LOAD DATA*** - defines the array that populates the entry boxes upon initializing of the app
        initial_array = ['000',
                         '',
                         '',
                         'Select',
                         'Select',
                         'Enter in V',
                         'Enter in V',
                         'Enter in V',
                         'Enter in V',
                         'Enter in A',
                         'Enter in Hz',
                         '',
                         '',
                         'Enter in K',
                         'Enter in PSI',
                         'Enter in K',
                         'Enter in K',
                         'Enter in K',
                         'Enter in us or select',
                         'Enter in mm or select',
                         'Enter notes regarding run']
        ring = ['']
        data = self.load_data_to_arr(self.load_data())
        ringdata = self.load_data_to_arr(self.load_data2())
        #checks each index in the length of the array called by the load_data and load_data_to_arr functions for a character length greater than 0 >
        #if that is true, it appends the data to the initial array index that matches it
        for i in range(len(data)):
            if len(data[i]) > 0:
                initial_array[i] = data[i]

        for i in range(len(ringdata)):
            if len(ringdata[i]) > 0:
                ring[i] = ringdata[i]

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
        self.configLabel = ctk.CTkLabel(self.setup_frame, text= "Config.")
        self.configLabel.grid(row=1,column=0, padx = 20, pady = 20, sticky = "ew")

        #config number selection
        configEntry_var = ctk.StringVar(value=initial_array[1])
        self.configEntry = ctk.CTkEntry(self.setup_frame, textvariable = configEntry_var, placeholder_text="Enter configuration number")
        self.configEntry.grid(row=1, column=1, padx = 20, pady = 20, sticky="ew")

        ringselect_var = ctk.StringVar(value=ring[0])
        self.ringselect = ctk.CTkComboBox(self.setup_frame, width=84, height=30, variable=ringselect_var, values=["1", "2", "3"])
        self.ringselect.grid(row=1, column=2, padx = 20, pady = 20)

        ringdisplay = CTkToolTip(self.ringselect, message="Select Number of Field Rings")

        


        #GRID CONFIGURATION DROPDOWN      
        #for loop with nested dictionaries that checks for different variations enabled for grid and run select to return corresponding configuration number
        def gridruntype_entry(*args):
            ring_select = ringselect_var.get()
            grid_select = gridSelect_var1.get()
            run_select = runSelect_var1.get()

            config_map = {
                "3": {  "Single Grid": 
                      {"Production": "131",
                        "Noise": "231",
                        "Test": "031",
                        "Commissioning": "031"},
                    "Double Grid": 
                        {"Production": "132",
                        "Noise": "232",
                        "Test": "032",
                        "Commissioning": "032"}  },

                "2": {  "Single Grid":
                    {"Production": "121",
                    "Noise": "221",
                    "Test": "021",
                    "Commissioning": "021"},
                "Double Grid":
                    {"Production": "122",
                    "Noise": "222",
                    "Test": "022",
                    "Commissioning": "022"}  },
             
                "1": {  "Single Grid":
                        {"Production": "111",
                        "Noise": "211",
                        "Test": "011",
                        "Commissioning": "011"},
                    "Double Grid":
                        {"Production": "112",
                        "Noise": "212",
                        "Test": "012",
                        "Commissioning": "012"}  }
            }

            configEntry_var.set(config_map.get(ring_select, {}).get(grid_select, {}).get(run_select, ""))   

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
        self.gridLabel = ctk.CTkLabel(self.setup_frame, text = "Grid Set-up")
        self.gridLabel.grid(row=3, column=0, padx = 20, pady = 20, sticky="ew")

        #grid config dropdown
        gridSelect_var1 = ctk.StringVar(value =initial_array[3])
        self.gridSelect = ctk.CTkOptionMenu(self.setup_frame, variable = gridSelect_var1, values=["Single Grid", "Double Grid"])
        self.gridSelect.grid(row=3, column=1, padx = 20, pady=20, sticky="ew")
        gridSelect_var1.trace("w", gridruntype_entry)

        #test type label
        self.runLabel = ctk.CTkLabel(self.setup_frame, text = "Run Type")
        self.runLabel.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        

        #test type dropdown
        runSelect_var1 = ctk.StringVar(value=initial_array[4])
        self.runSelect = ctk.CTkOptionMenu(self.setup_frame, variable=runSelect_var1, values=["Test", "Commissioning", "Noise", "Production"])
        self.runSelect.grid(row=4, column=1, padx=20, pady=20, sticky="ew")
        runSelect_var1.trace("w", gridruntype_entry)
        
        #cathode voltage label
        self.cathodeLabel = ctk.CTkLabel(self.setup_frame, text = "Cathode V.")
        self.cathodeLabel.grid(row=5, column=0, padx =20, pady = 20, sticky='we')

        #cathode voltage select/entry
        cathodeEntry_var = ctk.StringVar(value=initial_array[7])
        self.cathodeEntry = ctk.CTkEntry(self.setup_frame, textvariable=cathodeEntry_var, placeholder_text="Enter in V")
        self.cathodeEntry.grid(row=5, column=1, padx=20, pady=20, sticky='ew')

        #cathode grid voltage label
        self.cathodeGridLabel = ctk.CTkLabel(self.setup_frame, text = "Cathode Grid V.")
        self.cathodeGridLabel.grid(row=6, column=0, padx=20, pady=20, sticky="we")

        #cathode grid voltage entry
        cathodeGridEntry_var = ctk.StringVar(value=initial_array[8])
        self.cathodeGridEntry = ctk.CTkEntry(self.setup_frame, textvariable=cathodeGridEntry_var)
        self.cathodeGridEntry.grid(row=6, column=1, padx=20, pady=20, sticky="we")

        #anode grid voltage label
        self.anodeGridLabel = ctk.CTkLabel(self.setup_frame, text = "Anode Grid V.")
        self.anodeGridLabel.grid(row=7, column = 0, padx=20, pady=20, sticky="we")

        #anode grid entry
        anodeGridEntry_var = ctk.StringVar(value=initial_array[6])
        self.anodeGridEntry = ctk.CTkEntry(self.setup_frame, textvariable=anodeGridEntry_var, placeholder_text="Enter in V")
        self.anodeGridEntry.grid(row=7, column=1, padx=20, pady=20, sticky="ew")

        #anode voltage label
        self.anodeLabel = ctk.CTkLabel(self.setup_frame, text = "Anode V.")
        self.anodeLabel.grid(row=8, column=0, padx = 20, pady = 20, sticky='ew')

        #anode voltage select/entry
        anodeEntry_var = ctk.StringVar(value=initial_array[5])
        self.anodeEntry = ctk.CTkEntry(self.setup_frame, textvariable = anodeEntry_var, placeholder_text="Enter in V")
        self.anodeEntry.grid(row=8, column=1, padx=20, pady=20, sticky='ew')

        #media label
        self.mediaLabel = ctk.CTkLabel(self.setup_frame, text = 'Select Media')
        self.mediaLabel.grid(row=9, column=0, padx= 20, pady= 20, sticky='we')

        #media select
        mediaSelect_var = ctk.StringVar(value=initial_array[11])
        self.mediaSelect = ctk.CTkOptionMenu(self.setup_frame, variable=mediaSelect_var, values=["Vacuum", "Gas Xenon", "Liquid Xenon"])
        self.mediaSelect.grid(row=9, column=1, padx=20, pady=20, sticky='we')

        #laser current label
        self.currentLabel = ctk.CTkLabel(self.rundata_frame, text="Laser Current (A)")
        self.currentLabel.grid(row=0, column=0, padx = 20, pady = 20, sticky = 'we')

        #laser current entry
        currentEntry_var = ctk.StringVar(value=initial_array[9])
        self.currentEntry = ctk.CTkEntry(self.rundata_frame, textvariable=currentEntry_var, placeholder_text="Enter in A")
        self.currentEntry.grid(row=0, column=1, padx = 20, pady = 20, sticky = 'ew')

        #laser frequency label
        self.frequencyLabel = ctk.CTkLabel(self.rundata_frame, text = "Laser Freq. (Hz)")
        self.frequencyLabel.grid(row=1, column=0, padx = 20, pady = 20, sticky = 'we')

        #laser frequency entry
        frequencyEntry_var = ctk.StringVar(value=initial_array[10])
        self.frequencyEntry = ctk.CTkEntry(self.rundata_frame, textvariable=frequencyEntry_var, placeholder_text = "Enter in Hz")
        self.frequencyEntry.grid(row=1, column=1, padx = 20, pady=20, sticky='ew')


        #target channel label
        self.targetChannelLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Channel")
        self.targetChannelLabel.grid(row=2, column=0, padx = 20, pady = 20, sticky = 'we')

        #target channel select
        targetChannelSelect_var = ctk.StringVar(value=initial_array[12])
        self.targetChannelSelect = ctk.CTkOptionMenu(self.rundata_frame, values=["1", "2", "3", "4", "5", "6", "7", "8"], variable = targetChannelSelect_var)
        self.targetChannelSelect.grid(row=2, column=1, padx = 20, pady = 20, sticky = 'ew')

        #target temperature label
        self.targetTempLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Temp. (K)")
        self.targetTempLabel.grid(row=3, column=0, padx=20, pady=20, sticky="we")

        #target temperature entry
        targetTempEntry_var = ctk.StringVar(value=initial_array[13])
        self.targetTempEntry = ctk.CTkEntry(self.rundata_frame, textvariable=targetTempEntry_var, placeholder_text="Enter in K")
        self.targetTempEntry.grid(row=3, column = 1, padx=20, pady=20, sticky='ew')

        #target pressure label
        self.targetPressureLabel = ctk.CTkLabel(self.rundata_frame, text = "Target Pressure (psi)")
        self.targetPressureLabel.grid(row = 4, column = 0, padx=20, pady=20, sticky='we')

        #target pressure entry
        targetPressureEntry_var = ctk.StringVar(value=initial_array[14])
        self.targetPressureEntry = ctk.CTkEntry(self.rundata_frame, textvariable=targetPressureEntry_var, placeholder_text= "Enter in psi")
        self.targetPressureEntry.grid(row = 4, column = 1, padx = 20, pady = 20, sticky='ew')

        #bottom RTD label
        self.RTD1Label = ctk.CTkLabel(self.rundata_frame, text = "RTD 1 (K)")
        self.RTD1Label.grid(row=5, column=0, padx=20, pady=20, sticky='we')

        #bottom RTD entry
        RTD1Entry_var = ctk.StringVar(value=initial_array[15])
        self.RTD1Entry = ctk.CTkEntry(self.rundata_frame, textvariable=RTD1Entry_var, placeholder_text="Enter in K")
        self.RTD1Entry.grid(row=5, column=1, padx = 20, pady=20, sticky='we')

        #mid RTD label
        self.RTD2Label = ctk.CTkLabel(self.rundata_frame, text = "RTD 2 (K)")
        self.RTD2Label.grid(row=6, column=0, padx=20, pady=20, sticky='we')

        #mid RTD entry
        RTD2Entry_var = ctk.StringVar(value=initial_array[16])
        self.RTD2Entry = ctk.CTkEntry(self.rundata_frame, textvariable=RTD2Entry_var, placeholder_text="Enter in K")
        self.RTD2Entry.grid(row=6, column=1, padx = 20, pady=20, sticky='we')        
        
        #top RTD label
        self.RTD3Label = ctk.CTkLabel(self.rundata_frame, text = "RTD 3 (K)")
        self.RTD3Label.grid(row=7, column=0, padx=20, pady=20, sticky='we')

        #top RTD entry
        RTD3Entry_var = ctk.StringVar(value=initial_array[17])
        self.RTD3Entry = ctk.CTkEntry(self.rundata_frame, textvariable=RTD3Entry_var, placeholder_text="Enter in K")
        self.RTD3Entry.grid(row=7, column=1, padx = 20, pady=20, sticky='we')

        #window label
        self.windowLabel = ctk.CTkLabel(self.rundata_frame, text='Signal Window (us)')
        self.windowLabel.grid(row=8, column=0, padx=20, pady=20, sticky = 'ew')

        #window entry/select
        windowEntry_var = ctk.StringVar(value=initial_array[18])
        self.windowEntry = ctk.CTkComboBox(self.rundata_frame, values=["25", "50", "100", "200"], variable=windowEntry_var)
        self.windowEntry.grid(row=8, column=1, padx=20, pady=20, sticky='we')

        #drift length label
        self.lengthLabel = ctk.CTkLabel(self.rundata_frame, text = "Drift Length (mm)")
        self.lengthLabel.grid(row=9, column=0, padx = 20, pady=20, sticky="ew")

        #drift length entry/select
        lengthEntry_var = ctk.StringVar(value=initial_array[19])
        self.lengthEntry = ctk.CTkComboBox(self.rundata_frame, values=['8', '20'], variable=lengthEntry_var)
        self.lengthEntry.grid(row=9, column = 1, padx=20, pady=20, sticky='we')

        #notes
        notesEntry_var = ctk.StringVar(value=initial_array[20])
        self.notesEntry = ctk.CTkEntry(self.notes_frame, textvariable=notesEntry_var, height=100, width=360)
        self.notesEntry.grid(row=0, column=0, columnspan=3, padx=20, pady=20)

#QUERY BOX
        self.searchframe = searchframe(self.notes_frame)
        self.searchframe.grid(row=4, column=0, padx=20, pady=20,sticky="nsew")


#STORING INPUT DATA
        #this dictionary takes all of the string variables defined for each entry field and assigns them a plaintext key
        self.input_data = {
            "Run No.":entry_var,
            "Configuration No.":configEntry_var, 
            "Date":dateBox_var, 
            "Grid No.":gridSelect_var1, 
            "Run Type":runSelect_var1, 
            "Anode V.":anodeEntry_var,
            "Anode Grid V.":anodeGridEntry_var, 
            "Cathode V.":cathodeEntry_var,
            "Cathode Grid V.":cathodeGridEntry_var, 
            "Laser Current":currentEntry_var, 
            "Laser Freq.":frequencyEntry_var, 
            "Media":mediaSelect_var, 
            "Target Channel":targetChannelSelect_var, 
            "Target Temp.":targetTempEntry_var, 
            "Target Pressure":targetPressureEntry_var, 
            "RTD1":RTD1Entry_var, 
            "RTD2":RTD2Entry_var, 
            "RTD3":RTD3Entry_var, 
            "Window":windowEntry_var, 
            "Length":lengthEntry_var,
            "Notes":notesEntry_var
        }

    
#***SAVE AND LOAD DATA FUNCTIONS*** and SAVE BUTTONS (technically this should be up w setup) 
    #on closing function
        def on_closing(*args):
            self.destroy()
    
    #placing buttons, assigning SAVE CSV command to it
        self.saveButton = ctk.CTkButton(self.notes_frame, width = 40, height=40, corner_radius=6, text= "SAVE RUN", font=("Arial", 16, "bold"), hover=True, hover_color="#65ACA2", command=self.save_csv)
        self.saveButton.grid(row=3, column=0, columnspan=1, padx=20, pady=20, sticky="we")


    #closing events bound to method (imma be real i have no clue which of these actually does something i'll debug later)
        self.protocol("WM_DELETE_WINDOW", on_closing)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
            

    #LOADS data from txt file to repopulate in entry fields
    def load_data(self):
        base_path = format(path_config["base_path"])
        filename = format(path_config["userinput"])
        filepath = os.path.join(base_path, filename)
        with open(filepath, "r") as file:
            return file.read()
    
    def load_data2(self):
        base_path = format(path_config["base_path"])
        filename = format(path_config["ringdata"])
        filepath = os.path.join(base_path, filename)
        with open(filepath, "r") as file:
            return file.read()

    #takes data from load_data and loads it to an array - this is so input data can be easily appended and so it behaves better when saved to a plaintxt file
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
        now = datetime.now()
        current_time_insert = now.strftime("%H:%M:%S")
        base_path = format(path_config["base_path"])
        filename = format(path_config["userinput"])
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w") as file:
            for key, var in self.input_data.items():
                file.write(f"{key}:{var.get()}\n")
        print("data txt save for Run", self.input_data["Run No."].get(), "successful at", current_time_insert)
    
    def save_ringnumber(self):
        base_path = format(path_config["base_path"])
        filename = format(path_config["ringdata"])
        filepath = os.path.join(base_path, filename)
        with open(filepath, "w") as file:
            file.write(self.ringselect.get())


    #SEPARATE from save/load_data fcts. this SAVES all entry fields to the NAMED CSV. separated columnar by commas and placed into one ROW for each run
    #if the csv file doesn't exist (i delete it often for testing), it creates one
    #if it DOES exist, it APPENDS to a new row

    def save_csv(self):

        now = datetime.now()
        current_time_insert = now.strftime("%H:%M:%S")
        base_path = format(path_config["base_path"])
        filename = format(path_config["filename"])
        filepath = os.path.join(base_path, filename)

        # Log file path
        log_filepath = os.path.join(base_path, "save_log.txt")

        # Function to handle overwrite confirmation
        def show_question():
            message = CTkMessagebox(
                title="Overwrite Warning",
                message=f"Do you want to overwrite Run {self.input_data['Run No.'].get()}?",
                icon="question",
                options=["Cancel", "No", "Yes"]
            )
            response = message.get()
            if response == "Yes":
                print(f"Overwriting save for Run {self.input_data['Run No.'].get()} at {current_time_insert}")
                return True
            else:
                print("Dialog closed or Overwrite declined")
                return False

        # Function to check if run number already exists in the CSV
        def check_for_run():
            with open(filepath, "r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    if self.input_data["Run No."].get() == row[0]:
                        return True
                return False

        # Check if run number already exists
        if check_for_run():
            if not show_question():
                return  # Stop save process if user cancels or declines overwrite

        # Proceed with saving to CSV
        with open(filepath, "a", newline="") as file:
            writer = csv.writer(file)
            row_to_write = [var.get() for key, var in self.input_data.items()]
            writer.writerow(row_to_write)

        # Print and log success message
        success_message = f"CSV save for Run {self.input_data['Run No.'].get()} successful at {current_time_insert}"
        print(success_message)
        
        # Append success message to the log file
        with open(log_filepath, "a") as log_file:
            log_file.write(success_message + "\n")
            
    #tbd
    def on_opening(self):
        self.__init__()

    #binds the previously defined save data fct (to text file) to the closing of the app so it is automatic (reminder: csv is NOT automatic)
    #double reminder, all functions defined upon closing ONLY work if you close the GUI out properly. they DO NOT work if you kill the terminal that it's running on even though that closes the window as well.
    def on_closing(self):
        self.save_data()
        self.save_ringnumber()
        self.destroy()

#close-out/runs app fct as loop. also splits stuff for load_data fct
if __name__ == "__main__":
    
    app = App()
    string = app.load_data()
    ringstring = app.load_data2()
    split = app.load_data_to_arr(string)
    split2 = app.load_data_to_arr(ringstring)
    print(split)
    app.mainloop()

