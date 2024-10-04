import tkinter as tk
from tkinter import simpledialog
import customtkinter as ctk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
appWidth, appHeight = 1000, 500

def close():
    exit()


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("test GUI")
        self.geometry(f"{appWidth}x{appHeight}")
            

    def take_input():
        user_input = simpledialog.askstring('pop up for user input', 'add option?')
        if user_input != "":
            dropDown.add_command(label=user_input)

    dropDown = ctk.CTkOptionMenu(self, values = )
    dropDown.add_command(label = 'add option', command = take_input)

    my_entry = tk.Entry(win)
    my_entry.pack()

    menubar.add_cascade(label = 'drop down', menu = dropDown)
    win.config(menu = menubar)

if __name__ == "__main__":
    app = App()
    app.mainloop()
