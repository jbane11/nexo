from tkinter import LabelFrame, Tk, Button, Label

root = Tk()
# make row 0 resize with the window
root.rowconfigure(0, weight=1)
# make column 0 and 1 resize with the window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
# create LabelFrames
top_frame = LabelFrame(root, text="top")
left_frame = LabelFrame(root, text="left")
right_frame = LabelFrame(root, text="right")

top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=(10,4), sticky="nsew")
left_frame.grid(row=1, column=0, padx=(10,4), pady=4, sticky="nsew")
right_frame.grid(row=1, column=1, padx=(4,10), pady=4, sticky="nsew")

#create widgets inside top_frame
Label(top_frame, text="I'm inside top_frame").pack()
Button(top_frame, text="Top").pack()
#create widgets inside left_frame
Label(left_frame, text="I'm inside left_frame").pack()
Button(left_frame, text="Left").pack()
#create widgets inside top_frame
Label(right_frame, text="I'm inside right_frame").pack()
Button(right_frame, text="Right").pack()

Button(root, text="Quit", command=root.destroy).grid(row=2, column=0, 
                                                     columnspan=2, pady=10)

root.mainloop()