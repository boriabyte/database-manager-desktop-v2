# IMPORTS---------------------------------------------------------
import tkinter as tk
from main_design import Design
# ----------------------------------------------------------------

root = tk.Tk()                                                                          # init window
app = Design(root)                                                                      # the app itself is the design class which initializes everything &
                                                                                        # from which everything branches
app.add_widgets()
root.mainloop()                                                                         # keep process open as long as user wants
