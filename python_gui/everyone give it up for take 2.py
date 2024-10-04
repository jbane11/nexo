import customtkinter as ctk
from datetime import datetime
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SetupFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            entryfield_label = ctk.CTkLabel(self, text=value)
            entryfield_label.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.labels.append(entryfield_label)
        
        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var)
            entryfield.grid(row=i+1, column=1, padx=10, pady=(10,0), sticky='w')
            self.entryfields.append(entryfield)
            if "Grid Set-up" and "Run Type" and "Media" in self.values:
                entryfield_var1 = ctk.StringVar()
                entryfield_var2 = ctk.StringVar()
                entryfield_var3 = ctk.StringVar()
                entryfield = ctk.CTkOptionMenu(self, variable=entryfield_var1, values=["Single Grid - 20 mm", "Other"])
                entryfield.grid(row=4, column=1, padx=10, pady=(10,0), sticky='w')
                entryfield = ctk.CTkOptionMenu(self, variable=entryfield_var2, values = ["Test", 
                                                                                        "Commissioning", 
                                                                                        "Noise", 
                                                                                        "Production"])
                entryfield.grid(row=5, column=1, padx=10, pady=(10,0), sticky='w')
                entryfield = ctk.CTkOptionMenu(self, variable=entryfield_var3, values=["Vacuum", "Gas Xenon", "Liquid Xenon"])
                entryfield.grid(row=8, column=1, padx=10, pady=(10,0), sticky='w')
            

                

    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data

class LaserFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            entryfield_label = ctk.CTkLabel(self, text=value)
            entryfield_label.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.labels.append(entryfield_label)
        
        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var)
            entryfield.grid(row=i+1, column=1, padx=10, pady=(10,0), sticky='w')
            self.entryfields.append(entryfield)

    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data
    
class TargetFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            entryfield_label = ctk.CTkLabel(self, text=value)
            entryfield_label.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.labels.append(entryfield_label)
        
        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var)
            entryfield.grid(row=i+1, column=1, padx=10, pady=(10,0), sticky='w')
            self.entryfields.append(entryfield)
            if "Target Temp Channel" in self.values:
                entryfield_var1 = ctk.StringVar()
                entryfield = ctk.CTkOptionMenu(self, variable=entryfield_var1, values=["4","5"])
                entryfield.grid(row=1, column=1, padx=10, pady=(10,0), sticky="w")


    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data


class ThermoFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            entryfield_label = ctk.CTkLabel(self, text=value)
            entryfield_label.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.labels.append(entryfield_label)
        
        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var)
            entryfield.grid(row=i+1, column=1, padx=10, pady=(10,0), sticky='w')
            self.entryfields.append(entryfield)

    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data
    
class WindowFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            entryfield_label = ctk.CTkLabel(self, text=value)
            entryfield_label.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.labels.append(entryfield_label)
        
        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var)
            entryfield.grid(row=i+1, column=1, padx=10, pady=(10,0), sticky='w')
            self.entryfields.append(entryfield)

    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data

class NotesFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.labels = []
        self.entryfields = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

        for i, value in enumerate(self.values):
            entryfield_var = ctk.StringVar()
            entryfield = ctk.CTkEntry(self, textvariable=entryfield_var, height=100, width=200)
            entryfield.grid(row=i+1, column=0, padx=10, pady=(10,0),  sticky='w')
            self.entryfields.append(entryfield)
        
    def get(self):
        entryfield_data = []
        for entryfield_var in self.entryfields:
            if entryfield_var.get() != "":
                entryfield_data.append(entryfield_var.get())
        return entryfield_data

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Run GUI v2")
        self.geometry("1100x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setupframe = SetupFrame(self, "SET UP", values=["Run Number",
                                                             "Configuration",
                                                             "Date",
                                                             "Grid Set-up",
                                                             "Run Type",
                                                             "Anode Voltage",
                                                             "Cathode Voltage",
                                                             "Media"])
        
        self.setupframe.grid(row=0, column=0, padx=10, pady=(10,0), sticky='nsew')

        self.laserframe = LaserFrame(self, "LASER", values=["Laser Current",
                                                            "Laser Frequency"])
        self.laserframe.grid(row=1, column=0, padx=10, pady=(10,0), sticky='nsew')

        self.targetframe = TargetFrame(self, "TARGET", values=["Target Temp Channel", 
                                                               "Target Temperature", 
                                                               "Target Pressure"])
        self.targetframe.grid(row=0, column=1, padx=10, pady=(10,0), sticky="nsew")

        self.thermoframe = ThermoFrame(self, "TC READINGS", values=["TC 1",
                                                                    "TC 2",
                                                                    "TC 3"])
        self.thermoframe.grid(row=1, column=1, padx=10, pady=(10,0), sticky="nsew")

        self.windowframe = WindowFrame(self, "WINDOW + DRIFT LENGTH", values=["Signal Window",
                                                                              "Drift Length"])
        self.windowframe.grid(row=0, column=2, padx=10, pady=(10,0), sticky="nsew")

        self.notesframe = NotesFrame(self, "NOTES", values=[""])
        self.notesframe.grid(row=1, column=2, padx=10, pady=(10,0), sticky="nsew")

        self.returnbutton = ctk.CTkButton(self, text="click to return", command=self.buttonpress)
        self.returnbutton.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.setupbutton = ctk.CTkButton(self, text="return setup data", command=self.setupbuttonpress)
        self.setupbutton.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

        # self.generatebutton = ctk.CTkButton(self, text="generate new frame", command=self.generate)
        # self.generatebutton.grid(row=3, column=2, padx=10, pady=10, sticky='ew')

        # self.newfieldname = ctk.StringVar()
        # self.newfield = ctk.CTkEntry(self, textvariable=self.newfieldname)
        # self.newfield.grid(row=2, column=2, padx=10, pady=(10,0), sticky="nsew")

    def buttonpress(self):
        print("setup frame entry:", self.setupframe.get())
        print("laser frame entry:", self.laserframe.get())
        print("target frame entry:", self.targetframe.get())
        print("thermocoupler frame entry:", self.thermoframe.get())
        print("window + drift length:", self.windowframe.get())
        print("notes:", self.notesframe.get())
    
    def setupbuttonpress(self):
        print(self.setupframe.get())
        # def generate(self):
    #     class InsertedFrame(ctk.CTkFrame):
    #         def __init__(self, master, title, values):
    #             super().__init__(master)
    #             self.grid_columnconfigure(0, weight=1)
    #             self.values = values
    #             self.title = title
    #             self.entryfields = []

    #             self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6, font=("Arial", 14, "bold"))
    #             self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="ew")

    #             for i, value in enumerate(self.values):
    #                 entryfield_var = ctk.StringVar()
    #                 entryfield = ctk.CTkEntry(self, textvariable=entryfield_var, height=100, width=200)
    #                 entryfield.grid(row=i+1, column=0, padx=10, pady=(10,0),  sticky='w')
    #                 self.entryfields.append(entryfield)
                
    #         def get(self):
    #             entryfield_data = []
    #             for entryfield_var in self.entryfields:
    #                 if entryfield_var.get() != "":
    #                     entryfield_data.append(entryfield_var.get())
    #             return entryfield_data




app = App()
app.mainloop()