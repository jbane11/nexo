import customtkinter as ctk
ctk.set_appearance_mode("Dark")

class EntryFrame(ctk.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.variable = ctk.StringVar(value="")

        self.title = ctk.CTkLabel(self, text=self.title)
        self.title.grid(row=0,  column=0, padx=10, pady=(10,0), sticky="ew")

        for i in enumerate(self.values):
            entryfield = ctk.CTkEntry(self, textvariable=self.variable)
            entryfield.grid(row=1, column=0, padx=10, pady=(10,0), sticky="w")
        
    def get(self):
        return self.variable.get()
        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("return entry test")
        self.geometry("400x400")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.entryframe = EntryFrame(self, "Enter Here", values=["Search Query"])
        self.entryframe.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")

        self.button = ctk.CTkButton(self, text="button", command=self.buttonpress)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

        self.textbox = ctk.CTkTextbox(self, state="normal")
        self.textbox.grid(row=0, column=1,padx=10, pady=(10,0), sticky="nsew")
    
    def buttonpress(self):
        print("entry frame return:", self.entryframe.get())
        self.textbox.insert(index="0.0", text=self.entryframe.get()+"\n")

app = App()
app.mainloop()



