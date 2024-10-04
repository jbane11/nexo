import customtkinter as ctk
import os

class DataEntryApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Entry App")

        # Create variables to store entered data
        self.dateBox_var = ctk.StringVar()
        self.configEntry_var = ctk.StringVar()

        # Create entry fields for input
        date_label = ctk.CTkLabel(master, text="Date:")
        date_label.grid(row=0, column=0)
        self.date_entry = ctk.CTkEntry(master, textvariable=self.dateBox_var)
        self.date_entry.grid(row=0, column=1)

        config_label = ctk.CTkLabel(master, text="Config:")
        config_label.grid(row=1, column=0)
        self.config_entry = ctk.CTkEntry(master, textvariable=self.configEntry_var)
        self.config_entry.grid(row=1, column=1)

        # Create save button
        save_button = ctk.CTkButton(master, text="Save", command=self.save_data)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Bind the closing event to a method
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def save_data(self):
        # Variables 
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        runnumber_to_string = "247"  # Replace with appropriate value
        filename_raw = (self.dateBox_var.get(), "-", self.configEntry_var.get(),"00",runnumber_to_string)
        file_name1 = "".join(filename_raw)
  
        # Using os.path.join() 
        file_path = os.path.join(base_path, file_name1) 

        # Write to the file
        with open(file_path, 'w') as file: 
            file.write("Hello, this is an example.") 
        print("Task performed successfully")

    def on_closing(self):
        self.master.destroy()

def main():
    root = ctk.CTk()
    app = DataEntryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
