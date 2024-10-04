import customtkinter as ctk
from datetime import date

class EntryWithAutoDatePopulate:
    def __init__(self, master):
        self.master = master
        master.title("Entry with Auto Date Populate")

        # Create entry box
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(master, textvariable=self.entry_var)
        self.entry.grid(row=0, column=0)

        # Create button
        self.populate_button = ctk.CTkButton(master, text="Populate with Today's Date", command=self.populate_date)
        self.populate_button.grid(row=0, column=1)

        # Bind callback to entry box to re-enable button when cleared
        self.entry.bind("<FocusOut>", self.check_entry)

    def populate_date(self):
        today = date.today()
        self.entry_var.set(today.strftime("%Y-%m-%d"))
        self.populate_button.configure(state=ctk.NORMAL)  # Re-enable button

    def check_entry(self, event):
        if not self.entry_var.get():
            self.populate_button.configure(state=ctk.NORMAL)  # Re-enable button
        else:
            self.populate_button.configure(state=ctk.DISABLED)  # Disable button

def main():
    root = ctk.CTk()
    app = EntryWithAutoDatePopulate(root)
    root.mainloop()

if __name__ == "__main__":
    main()
