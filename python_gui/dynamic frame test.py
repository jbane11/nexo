import customtkinter as ctk
ctk.set_appearance_mode("Dark")

class CheckboxFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky='w')
            self.checkboxes.append(checkbox)

    #hardcodes values of checkboxes in frame
        # self.checkbox1 = ctk.CTkCheckBox(self, text="checkbox 1")
        # self.checkbox1.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        # self.checkbox2 = ctk.CTkCheckBox(self, text="checkbox 2")
        # self.checkbox2.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        # self.checkbox3 = ctk.CTkCheckBox(self, text="checkbox 3")
        # self.checkbox3.grid(row=2, column=0, padx=10, pady=(10,0), sticky='w')

    def get(self):
        checked_boxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_boxes.append(checkbox.cget("text"))
        return checked_boxes

    #hardcoding (what i'm doing)
        # if self.checkbox1.get()==1:
        #     checked_boxes.append(self.checkbox1.cget("text"))
        # if self.checkbox2.get()==1:
        #     checked_boxes.append(self.checkbox2.cget("text"))
        # if self.checkbox3.get()==1:
        #     checked_boxes.append(self.checkbox3.cget("text"))
        # return checked_boxes

class RadiobuttonFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky='ew')

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable)
            radiobutton.grid(row=i+1, column=0, padx=10, pady=(10,0), sticky="w")
            self.radiobuttons.append(radiobutton)
    def get(self):
        return self.variable.get()
    
    def set(self, value):
        self.variable.set(value)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("frame test")
        self.geometry("400x220")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.checkboxframe = CheckboxFrame(self, "Values", values=["value 1", "value 2", "value 3"])
        self.checkboxframe.grid(row=0, column=0, padx=10, pady=(10,0), sticky='nsew')

        self.radiobuttonframe = RadiobuttonFrame(self, "Options", values=["option 1", "option 2"])
        self.radiobuttonframe.grid(row=0, column=1, padx=(0,10), pady=(10,0), sticky="nsew")

        self.button = ctk.CTkButton(self, text="button", command=self.buttonpress)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky='ew', columnspan=2)

    def buttonpress(self):
        print("checkbox frame:", self.checkboxframe.get())
        print("radio button frame:", self.radiobuttonframe.get())

app = App()
app.mainloop()