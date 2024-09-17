from caen_libs import caenhvwrapper as hv  
from pycaenhv.wrappers import init_system, deinit_system, get_board_parameters, get_crate_map, get_channel_parameter_property, get_channel_parameters, list_commands,get_channel_parameter
from pycaenhv.enums import CAENHV_SYSTEM_TYPE, LinkType
from pycaenhv.errors import CAENHVError
import os, time
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Global variable to store the connection handle
handle = None
ch_keys=[]



type="N1470"   ##Type of power suppl
link="USB_VCP" ##How the supply is connected
address="COM10"   ##The connection port
class ConnectionHandle:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"ConnectionHandle({self.name})"

def connect():
    
    global handle

    system_type = CAENHV_SYSTEM_TYPE[type] #Function to pull enum from list of types
    link_type = LinkType[link]             #Function to pull enum from list of links

    try:
        deinit_system(handle)
    except:
        print("System already closed")

    # Make connection  
    print("Opening connection")
    try:
        handle = init_system(system_type, link_type,
                            address,
                            '','')
    except:

        print("issue with connection")
        exit()

    try:
        print(f"Got handle: {handle}")
        crate_map = get_crate_map(handle)
        for name, value in crate_map.items():
            print(name, value)
        board_parameters = get_board_parameters(handle, 0)
    except CAENHVError as err:
        print(f"Got error: {err}\nExiting ...")

    #messagebox.showinfo("Connection", "Connected Successfully!")
    ch_keys=get_channel_parameters(handle,0,0)
    print(ch_keys)
    return(handle)

def close_app():
    global handle
    
    confirm=True
    
    # confirm = messagebox.askokcancel("Close", "Double check the HV?")
    if confirm:
        deint(handle)
        print("Closing connection")
        app.destroy()


def deint(handle):
    
    try:
        deinit_system(handle)
    except:
        print("Issue with closing connection")


# Function to update the graph based on parameters
def update_graph():
    try:
        param1 = float(entry1.get())
        param2 = float(entry2.get())
        param3 = float(entry3.get())
        # Simulate graphs based on input parameters
        for i, ax in enumerate(axes):
            ax.clear()
            ax.plot([param1, param2, param3], label=f"Graph {i+1}")
            ax.legend()
        canvas.draw()
    except ValueError:
        messagebox.showerror("Error", "Invalid parameters! Please enter numeric values.")


# Function to update the current time every second
def update_time():
    global handle
    global ch_keys
    
    current_time = time.strftime('%H:%M:%S')  # Get the current time
    time_label.configure(text=f"Current Time: {current_time}")  # Update the label
    
    if handle!=None:


        Board_parameter=[]
        for i in (0,1,2,3):
            channel_parameter={}
            for key in ch_keys:
                print(i,key)
                channel_parameter[key]=readparamaters(handle,i,key)

            Board_parameter.append(channel_parameter)   
            

        print(Board_parameter)

    app.after(1000, update_time)  # Call this function again after 1000 ms (1 second)

def readparameters(handle,channel,key):

    for key in ch_keys:
        print(key , get_channel_parameter(handle,0,channel,key))



# Initialize the main window
app = ctk.CTk()
app.geometry("800x600")
app.title("CustomTkinter with Graphs")

# Set layout with two frames
left_frame = ctk.CTkFrame(app)
left_frame.pack(side="left", fill="y", padx=10, pady=10)

right_frame = ctk.CTkFrame(app)
right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Left frame widgets: Buttons and Entries for parameters
label = ctk.CTkLabel(left_frame, text="Set Parameters", font=("Arial", 16))
label.pack(pady=10)

# Text Boxes for Parameters
label1 = ctk.CTkLabel(left_frame, text="Parameter 1:")
label1.pack(pady=5)
entry1 = ctk.CTkEntry(left_frame)
entry1.pack(pady=5)

label2 = ctk.CTkLabel(left_frame, text="Parameter 2:")
label2.pack(pady=5)
entry2 = ctk.CTkEntry(left_frame)
entry2.pack(pady=5)

label3 = ctk.CTkLabel(left_frame, text="Parameter 3:")
label3.pack(pady=5)
entry3 = ctk.CTkEntry(left_frame)
entry3.pack(pady=5)

# Connect Button
connect_button = ctk.CTkButton(left_frame, text="Connect", command=connect)
connect_button.pack(pady=20)

# Update Graph Button
update_button = ctk.CTkButton(left_frame, text="Update Graph", command=update_graph)
update_button.pack(pady=10)

# Close Button
close_button = ctk.CTkButton(left_frame, text="Close", command=close_app)

close_button.pack(pady=10)



# Right frame for graphs using Matplotlib
fig, axes = plt.subplots(1, 3, figsize=(10, 4))

# Embed the Matplotlib figure in the Tkinter right_frame
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Add a label for displaying time, and update it every second
time_label = ctk.CTkLabel(left_frame, text="Current Time: ", font=("Arial", 14))
time_label.pack(pady=20)

# Start the loop for updating the time every second
update_time()


# Start the main loop
app.mainloop()