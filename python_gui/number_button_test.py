import customtkinter as ctk
import os

# Define the file to save the number
FILE_NAME = "saved_number.txt"

# Function to read the saved number from the file
def read_saved_number():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                return int(file.read())
            except ValueError:
                return 777  # Default value if the file is empty or invalid
    return 0  # Default value if the file does not exist

# Function to save the current number to the file
def save_number():
    with open(FILE_NAME, "w") as file:
        file.write(entry_var.get())

# Function to increase the number
def increase_number():
    current_value = int(entry_var.get())
    entry_var.set(current_value + 1)

# Function to decrease the number
def decrease_number():
    current_value = int(entry_var.get())
    entry_var.set(current_value - 1)

# Create the main window
root = ctk.CTk()
root.title("Number Increment/Decrement Example")

# Read the saved number from the file
initial_value = read_saved_number()

# Create and place the entry box
entry_var = ctk.StringVar(value=str(initial_value))
entry = ctk.CTkEntry(root, textvariable=entry_var, width=100, justify="center")
entry.pack(pady=20)

# Create and place the buttons
frame = ctk.CTkFrame(root)
frame.pack(pady=10)

increase_button = ctk.CTkButton(frame, text="+", command=increase_number)
increase_button.pack(side="left", padx=10)

decrease_button = ctk.CTkButton(frame, text="-", command=decrease_number)
decrease_button.pack(side="right", padx=10)

# Bind the save function to the window close event
root.protocol("WM_DELETE_WINDOW", lambda: (save_number(), root.destroy()))

# Run the application
root.mainloop()
