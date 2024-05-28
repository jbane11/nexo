# Python program to create a basic GUI 
# application using the customtkinter module
import customtkinter as ctk
import tkinter as tk
import numpy as np
# Basic parameters and initializations
# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark") 

# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("dark-blue") 

appWidth, appHeight = 800 , 500









window = ctk.CTk()
window.title("GUI Application")
window.geometry(f"{appWidth}x{appHeight}")

n=8
for i in np.arange(0,n,1):
    

    print(int(np.floor(i/2)), int((i+1)%2 ) )
    frame = tk.Frame(master=window, relief=tk.RIDGE )#, borderwidth=appWidth/(n*0.5) )
    frame.grid( column=int(np.floor(i/2)), row= int((i+1)%2 ),padx=appWidth/(n*0.5),pady=appHeight/2 ,sticky='E')
    #frame.pack(side=tk.LEFT)

    label = tk.Label(master=frame, text=i)

    label.pack()


window.mainloop()