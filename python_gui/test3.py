# Import the library tkinter 
import customtkinter as ctk
from tkinter import *

# Supported modes : Light, Dark, System
ctk.set_appearance_mode("Dark") 

# Supported themes : green, dark-blue, blue
ctk.set_default_color_theme("dark-blue") 

appWidth, appHeight = 800 , 300

# Create a GUI app 
app = ctk.CTk() 
app.geometry(f"{appWidth}x{appHeight}+0+0")
# Give a title to your app 
app.title("Vinayak App") 

nxFrames=4
nyFrames=2

# Constructing the first frame, frame1 
frame1 = LabelFrame(app, text="Fruit", bg="black", 
					fg="white", padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2)) 
# Displaying the frame1 in row 0 and column 0 
frame1.grid(row=0, column=0) 
# Constructing the button b1 in frame1 
b1 = Button(frame1, text="Apple") 
# Displaying the button b1 
b1.pack() 

# Constructing the second frame, frame2 
frame2 = LabelFrame(app, text="Vegetable", bg="cyan", padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2)) 
# Displaying the frame2 in row 0 and column 1 
frame2.grid(row=0, column=1) 
# Constructing the button in frame2 
b2 = Button(frame2, text="Tomato") 
# Displaying the button b2 
b2.pack() 

# Constructing frame3
frame3 = LabelFrame(app, text="Places", bg="blue", padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2))
frame3.grid(row=0, column=2) 
b3 = Button(frame3, text="Jungles") 
b3.pack()

#  Constructing frame4
frame4 = LabelFrame(app, text="Artist", bg="green",padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2)) 
frame4.grid(row=0, column=3) 
b4 = Button(frame4, text="John Bon Jovi") 
b4.pack()

# Make the loop for displaying app 
app.mainloop() 
