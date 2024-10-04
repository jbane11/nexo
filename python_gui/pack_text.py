import customtkinter as ctk
import tkinter as ctk

root = ctk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.state('zoomed')
root.geometry("%dx%d+0+0" % (w-15, h-75))

A = ctk.Label(root,text='A', bd=2)
B = ctk.LabelFrame(root,text='B', bd=2)
CD = ctk.Frame(root)
C = ctk.LabelFrame(CD,text='C', bd=2)
D = ctk.LabelFrame(CD,text='D', bd=2)
E = ctk.LabelFrame(root,text='E', bd=2)

C.pack(side=ctk.LEFT,fill=ctk.BOTH, expand=ctk.TRUE)
D.pack(side=ctk.RIGHT,fill=ctk.BOTH, expand=ctk.TRUE)

A.pack(fill=ctk.BOTH, expand=ctk.TRUE)
B.pack(fill=ctk.BOTH, expand=ctk.TRUE)
CD.pack(fill=ctk.BOTH, expand=ctk.TRUE)
E.pack(side=ctk.BOTTOM, fill=ctk.BOTH, expand=ctk.TRUE)

root.mainloop()