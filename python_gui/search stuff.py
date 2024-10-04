import os
import csv
import tkinter as tk

class YourClassName:
    def __init__(self, root):
        self.root = root
        self.query = tk.StringVar()  # Assuming you have defined StringVar elsewhere
        
        # Example usage: Setting the initial value of query (replace with actual logic)
        self.query.set("Default Query")
        
        # Creating a Text widget for displaying results
        self.result_textbox = tk.Text(root, height=10, width=50)
        self.result_textbox.pack(pady=10)

    def search_csv(self):
        base_path = "C:/Users/jasonbane/Desktop/example_folder"
        filename = "test_csv.csv"
        filepath = os.path.join(base_path, filename)
        
        found_match = False
        
        with open(filepath, "r") as c:
            reader = csv.reader(c)
            first_match_found = True  # Flag to print the matching message only once
            result_text = ""
            for row in reader:
                if self.query.get() in row:  # Using .get() to get the actual string value of query
                    found_match = True
                    if first_match_found:
                        result_text += f"Run(s) matching {self.query.get()}:\n"
                        first_match_found = False
                    result_text += f"RUN {int(row[0])}: [{', '.join(row)}]\n"
        
        if not found_match:
            result_text = f"No matching run for '{self.query.get()}'."
        
        # Clear previous content in the Text widget
        self.result_textbox.delete('1.0', tk.END)
        # Insert new content
        self.result_textbox.insert(tk.END, result_text)

# Example usage:
root = tk.Tk()
instance = YourClassName(root)

# Function to trigger search and update the textbox
def search_and_update():
    instance.search_csv()

# Button to trigger the search
search_button = tk.Button(root, text="Search", command=search_and_update)
search_button.pack(pady=10)

root.mainloop()  # Start the tkinter main loop
