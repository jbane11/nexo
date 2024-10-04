from tkinter import *
import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

appWidth, appHeight = 1000, 800
app = ctk.CTk()
app.geometry(f"{appWidth}x{appHeight}+0+0")

app.title("test GUI") 

nxFrames=4
nyFrames=2

#frame1 
frame1 = LabelFrame(app, text="RN", bg="black", 
					fg="white", padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2)) 

frame1.pack(padx=0, pady=0)

# Constructing the button b1 in frame1 
def show():
    label.config(text=clicked.get())

options = ["One", "Two", "Three", "Four"]

clicked = StringVar()
clicked.set("Select run number")

drop = OptionMenu(frame1, clicked, *options)
drop.pack()

b1 = Button(frame1, text = "click here", command=show).pack()

label = Label(frame1, text = "lorem ipsum")
label.pack()

button = Button(app, text='test')
button.pack(side=TOP, pady = 5, padx = 5)

#frame 2
frame2 = LabelFrame(app, text="Date", bg="green", 
                    fg="white", padx=appWidth/(nxFrames*2), pady=appHeight/(nyFrames*2))
frame2.pack(padx=500, pady=0)
b2 = Button(frame2, text="Date")

app.mainloop()



#app = ctk.CTk()
#app.geometry()

#root = Tk()
#appWidth, appHeight = 800, 600

#def show():
    #label.config(text=clicked.get())

#options = ["One", "Two", "Three", "Four"]

#clicked = StringVar()
#clicked.set("Initial Text")

#drop = OptionMenu(root, clicked, *options)
#drop.pack()

#button = Button(root, text = "click here", command=show).pack()

#label = Label(root, text = "bleh")
#label.pack()

#root.mainloop()