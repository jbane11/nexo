from customtkinter import CTk, CTkButton, CTkScrollableFrame

root = CTk()

frame = CTkScrollableFrame(root)
frame.pack(fill="both", expand=True)

# Create buttons and store them in a list
buttons = []
for n in range(30):
    button = CTkButton(frame, text=f"Button {n}")
    button.pack()
    buttons.append(button)

# Set initial focus to the first button
buttons[0].focus_set()

def highlight_button(button):
    """Helper function to update the button's appearance when focused."""
    button.configure(fg_color="lightblue")  # Highlight color (button with focus)
    
def reset_button(button):
    """Reset the button appearance."""
    button.configure(fg_color="white")  # Default button color

def navigate_up(event):
    """Move focus up and highlight the button."""
    for i, button in enumerate(buttons):
        if button == root.focus_get():
            reset_button(button)  # Reset the previous focused button
            if i > 0:
                buttons[i - 1].focus_set()  # Set focus to the previous button
                highlight_button(buttons[i - 1])  # Highlight the new focused button
            break

def navigate_down(event):
    """Move focus down and highlight the button."""
    for i, button in enumerate(buttons):
        if button == root.focus_get():
            reset_button(button)  # Reset the previous focused button
            if i < len(buttons) - 1:
                buttons[i + 1].focus_set()  # Set focus to the next button
                highlight_button(buttons[i + 1])  # Highlight the new focused button
            break

# Initial highlight for the first button
highlight_button(buttons[0])

# Bind the up and down arrow keys to navigate between buttons
root.bind("<Up>", navigate_up)
root.bind("<Down>", navigate_down)

root.mainloop()

