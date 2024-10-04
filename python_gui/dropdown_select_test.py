# Import the tkinter module 
import tkinter as tk

# Create the default window 
root = tk.Tk() 
root.title("Welcome to GeeksForGeeks") 
root.geometry('700x500') 


option_var = tk.StringVar()

def submit_option():
	option_input = option_var.get()
	print('option given is:' + option_input)
	option_var.set("")

entry_label = tk.Label(root, text = 'populate here')
entry = tk.Entry(root, textvariable=option_var)


# Create the list of options 
options_list = ["Option 1", "Option 2", "Option 3", "Option 4"] 

# Variable to keep track of the option 
# selected in OptionMenu 
value_inside = tk.StringVar(root) 

# Set the default value of the variable 
value_inside.set("Select an Option") 

# Create the optionmenu widget and passing 
# the options_list and value_inside to it. 
question_menu = tk.OptionMenu(root, value_inside, *options_list) 
question_menu.pack() 

# Function to print the submitted option-- testing purpose 

def print_answers(): 
	("Selected Option: {}".format(value_inside.get())) 
	return None


# Submit button 
# Whenever we click the submit button, our submitted 
# option is printed ---Testing purpose 
submit_button = tk.Button(root, text='Submit', command=print_answers) 
submit_button.pack() 

root.mainloop() 
