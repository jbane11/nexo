import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.minsize(width=600, height=400)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        # Create a 3x3 grid layout of mixed entry boxes and option menus
        self.widgets = []
        self.option_menus = []  # To store references to option menus
        for i in range(9):
            if i % 2 == 0:  # Even indices (0, 2, 4, 6, 8) will be Entry boxes
                widget = tk.Entry(self.main_frame, width=10)
            else:  # Odd indices (1, 3, 5, 7) will be Option menus
                choices = ['Option 1', 'Option 2', 'Option 3']
                var = tk.StringVar(self.main_frame)
                var.set(choices[0])
                widget = tk.OptionMenu(self.main_frame, var, *choices)
                self.option_menus.append((widget, var, choices))

            widget.grid(row=i // 3, column=i % 3, padx=10, pady=10)
            self.widgets.append(widget)

        self.current_index = 0

        self.bind('<Left>', self.left_key)
        self.bind('<Right>', self.right_key)
        self.bind("<Up>", self.up_key)
        self.bind("<Down>", self.down_key)
        self.bind("<Return>", self.enter_key)

    def left_key(self, event):
        if self.current_index % 3 > 0:  # Check if not in leftmost column
            self.current_index -= 1
        self.focus_widget()

    def right_key(self, event):
        if self.current_index % 3 < 2:  # Check if not in rightmost column
            self.current_index += 1
        self.focus_widget()

    def up_key(self, event):
        if self.current_index >= 3:  # Check if not in top row
            self.current_index -= 3
        self.focus_widget()

    def down_key(self, event):
        if self.current_index < 6:  # Check if not in bottom row
            self.current_index += 3
        self.focus_widget()

    def enter_key(self, event):
        widget = self.widgets[self.current_index]
        if isinstance(widget, tk.OptionMenu):
            # Open the dropdown if closed
            widget['menu'].post(widget.winfo_rootx(), widget.winfo_rooty() + widget.winfo_height())
        elif isinstance(widget, tk.Entry):
            widget.focus()

    def focus_widget(self):
        widget = self.widgets[self.current_index]
        if isinstance(widget, tk.OptionMenu):
            widget.focus()
        else:
            widget.focus()

if __name__ == "__main__":
    app = App()
    app.mainloop()
