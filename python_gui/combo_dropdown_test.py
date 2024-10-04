import customtkinter as ctk

def update_entry(*args):
    if option_var1.get() == "Single Grid" and option_var2.get() == "Production":
        entry_var.set("131")
    else:
        entry_var.set("")

# Create the main window
root = ctk.CTk()
root.title("Dropdown Selection Example")

# Create and place the first option menu
label1 = ctk.CTkLabel(root, text="Select Option 1:")
label1.pack(pady=5)

option_var1 = ctk.StringVar(value="Select an option")
option_menu1 = ctk.CTkOptionMenu(root, variable=option_var1, values=["Single Grid", "Option 1", "Option 2"])
option_menu1.pack(pady=5)
option_var1.trace("w", update_entry)

# Create and place the second option menu
label2 = ctk.CTkLabel(root, text="Select Option 2:")
label2.pack(pady=5)

option_var2 = ctk.StringVar(value="Select an option")
option_menu2 = ctk.CTkOptionMenu(root, variable=option_var2, values=["Production", "Option A", "Option B"])
option_menu2.pack(pady=5)
option_var2.trace("w", update_entry)

# Create and place the entry box
entry_var = ctk.StringVar()
entry = ctk.CTkEntry(root, textvariable=entry_var)
entry.pack(pady=20)

# Run the application
root.mainloop()
