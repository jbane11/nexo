import customtkinter as ctk
import csv

class StringVariablesApp:
    def __init__(self, master):
        self.master = master
        master.title("String Variables App")

        self.labels = []
        self.entries = []

        # Create labels and entry fields for string variables
        for i in range(3):  # Change the range as per your requirement
            label = ctk.CTkLabel(master, text=f"String Variable {i+1}:")
            entry = ctk.CTkEntry(master)
            label.grid(row=i, column=0, sticky="e")
            entry.grid(row=i, column=1)
            self.labels.append(label)
            self.entries.append(entry)

        # Bind the closing event to a method
        master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # Save string variables to a CSV file
        filename = "string_variables.csv"
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for entry in self.entries:
                writer.writerow([entry.get()])
            print("Task completed")

        # Close the GUI
        self.master.destroy()

def main():
    root = ctk.CTk()
    app = StringVariablesApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
