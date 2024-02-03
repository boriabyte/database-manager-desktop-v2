from tkinter import ttk
import tkinter as tk
from connect_to_db import get_db_connection

class AnimalsInterface:
    def __init__(self, root, design):
        self.root = root
        self.design = design
        self.db = get_db_connection()
        self.visualize_query = "SELECT name FROM animals"

    def open_animals_interface(self):
        self._clear_root()
        self._add_interface_title("ANIMALS")
        self._add_return_home_button()
        self._add_treeview()

    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _add_interface_title(self, title):
        interface_title = tk.Label(self.root, text=title, bg="white", fg="#0078D4", font=("Montserrat", 50, "bold"))
        interface_title.place(relx=0.5, rely=0.1, anchor='n')

    def _add_return_home_button(self):
        return_home = self.design._create_button("<", self.return_to_main)
        return_home.place(relx=0.05, rely=0.1, anchor='nw')

    def _add_treeview(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Montserrat", 25), rowheight=40, foreground="#0078D4")  # adjust the font size, row height, and font color as needed
        style.configure("Treeview.Cell", padding=(10, 0))  # add padding to each cell
        style.configure("Treeview", borderwidth=0)  # make the border invisible
        style.map('Treeview',
                background=[('selected', '#0078D4')],  # change the background color of selected entry to "#0078D4"
                foreground=[('selected', 'white')])  # change the font color of selected entry to white

        cursor = self.db.cursor()
        cursor.execute(self.visualize_query)
        rows = cursor.fetchall()

        tree = ttk.Treeview(self.root, height=len(rows), style="Treeview", show='tree')
        tree["columns"]=("one")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("one", width=300, stretch=tk.YES)

        for i, row in enumerate(rows, start=1):  # start enumeration from 1
            tree.insert("", "end", values=row)
    
        tree.place(relx=0.5, rely=0.6, anchor='center')
        tree.bind("<Enter>", lambda e: tree.config(cursor="hand2"))  # change cursor to hand2 when mouse enters
        tree.bind("<Leave>", lambda e: tree.config(cursor=""))
        tree.config(highlightthickness=0)

    def return_to_main(self):
        self._clear_root()
        self.design.add_widgets()
