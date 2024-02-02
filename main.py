# main.py
import tkinter as tk
from main_design import Design

root = tk.Tk()
app = Design(root)
app.add_widgets()

root.mainloop()
