import customtkinter as ctk
import csv

class DataEntryApp:
    def __init__(self, master):
        self.master = master
        master.title("Data Entry App")

        # Create variables to store entered data
        self.string_vars = []
        self.selected_options = []

        # Load previously entered data from CSV file, if available
        self.load_data()

        # Create entry fields for string variables
        for i in range(3):
            var = ctk.StringVar(value=self.string_vars[i].get())  # Changed this line
            entry = ctk.CTkEntry(master, textvariable=var)  # Changed this line
            entry.insert(0, var.get())  # Insert initial value
            entry.bind("<FocusOut>", lambda event, index=i: self.update_string_var(event, index))
            entry.grid(row=i, column=0, sticky="ew")

# Create option menus for selecting options
        options = ["Option 1", "Option 2", "Option 3"]
        for i in range(3):
            var = ctk.StringVar(value=self.selected_options[i].get())  # Changed this line
            option_menu = ctk.CTkOptionMenu(master, values=var)
            option_menu.grid(row=i, column=1)
            self.selected_options[i] = var


        # Bind the closing event to a method
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_data(self):
        try:
            with open("data.csv", mode="r") as file:
                reader = csv.reader(file)
                data = list(reader)
                for i in range(3):
                    self.string_vars.append(ctk.StringVar(value=data[i][0]))
                    self.selected_options.append(ctk.StringVar(value=data[i+3][0]))
        except FileNotFoundError:
            # Initialize string variables and selected options if file doesn't exist
            for _ in range(3):
                self.string_vars.append(ctk.StringVar())
                self.selected_options.append(ctk.StringVar())

    def save_data(self):
        with open("data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            for var in self.string_vars + self.selected_options:
                writer.writerow([var.get()])

    def update_string_var(self, event, index):
        self.string_vars[index].set(event.widget.get())

    def on_closing(self):
        self.save_data()
        self.master.destroy()

def main():
    root = ctk.CTk()
    app = DataEntryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
