import tkinter as tk
from tkinter.constants import END

window = tk.Tk()
window.title("Disappearing Text Writing App")
window.minsize(500, 500)
counter = 0


def disappear_text():
    textbox.delete(1.0, tk.END)
    textbox.insert(tk.END, "")

def check_disappear():
    global counter, text
    if text == textbox.get(1.0, tk.END):
        if counter == 10:
            window.after(1000, disappear_text)
            counter = -1
        window.after(1000, check_disappear)
        counter += 1
    else:
        window.after(1000, check_disappear)
        text = textbox.get(1.0, tk.END)
        counter = 0



title = tk.Label(window, text="Welcome to the Disappearing Text app", font = ("Arial Bold",20), bg = "grey", fg = "white")
title.grid(row=0, column=1, padx=10, pady=10)

text = ""
textbox = tk.Text(height=10, width=60, yscrollcommand=False, )
textbox.focus()
textbox.grid(row=3, column=1, padx=10, pady=10)

window.after(1000, check_disappear)
window.mainloop()