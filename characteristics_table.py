# IMPORTS---------------------------------------------------------
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox
import time
from connect_to_db import get_db_connection
# ----------------------------------------------------------------

class CharacteristicsInterface:
    def __init__(self, root, design):                                                                           # init interface
        self.root = root
        self.design = design
        self.db = get_db_connection()
        self.visualize_query = "SELECT characteristic FROM characteristics"                                     # query used for fetching data from mysql table
        
    def open_characteristics_interface(self):                                                                   # on opening the interface, these elements will be added
        self._clear_root()
        self._add_add_entry_button()
        self._add_kill_entry_button()
        self._add_interface_title("CHARACTERISTICS")
        self._add_return_home_button()
        self._add_treeview()
        self._add_hide_button()
        
    def _clear_root(self):                                                                                      # destroy elements from previous interface
        for widget in self.root.winfo_children():                                                               # will be called back on return
            widget.destroy()

    def _add_interface_title(self, title):
        interface_title = tk.Label(self.root, text=title, bg="white", fg="#0078D4", font=("Montserrat", 50, "bold"))
        interface_title.place(relx=0.5, rely=0.1, anchor='n')

    def _add_return_home_button(self):                                                                          # return to main interface
        return_home = self.design._create_button("<", self.return_to_main)
        return_home.place(relx=0.05, rely=0.1, anchor='nw')

    def _add_hide_button(self):                                                                                 # hide button to hide table
        self.hide_button= self.design._create_button("x", self.hide)
        
    def _add_add_entry_button(self):                                                                            # add entry to initial table button
        self.add_entry = self.design._create_button("+", self.add_entry)
        self.add_entry.place(relx=0.595, rely=0.32, anchor='ne', width=30, height=42)
    
    def _add_kill_entry_button(self):
        self.kill_entry = self.design._create_button("-", self.kill_entry)                                      # del entry from initial table button
        self.kill_entry.place(relx=0.595, rely=0.36, anchor="ne", width=30, height=42)
        
    def _add_treeview(self):                                                                                    # treeview = table; defining table params
        style = ttk.Style()
        style.configure("Treeview", font=("Montserrat", 25), rowheight=40, foreground="#0078D4")
        style.configure("Treeview.Cell", padding=(10, 0))
        style.configure("Treeview", borderwidth=0)
        style.map('Treeview',
                background=[('selected', '#0078D4')],
                foreground=[('selected', 'white')])

        cursor = self.db.cursor()                                                                               # init fetching from database
        cursor.execute(self.visualize_query)
        rows = cursor.fetchall()

        if not hasattr(self, 'tree'):                                                                           # if treeview is not visible, show it
            self.tree = ttk.Treeview(self.root, height=len(rows), style="Treeview", show='tree')
            self.tree["columns"]=("one")
            self.tree.column("#0", width=0, stretch=tk.NO)
            self.tree.column("one", width=300, stretch=tk.YES)
            self.tree.place(relx=0.5, rely=0.6, anchor='center')
            self.tree.bind("<Enter>", lambda e: self.tree.config(cursor="hand2"))                               # init style choices to hovering over entries
            self.tree.bind("<Leave>", lambda e: self.tree.config(cursor=""))
            self.tree.bind("<Double-1>", self.on_treeview_click)                                                # bind doubleclick event to entry of tables

        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=row)
    
    def on_treeview_click(self, event):                                                                         # def for double-click event
        item = self.tree.selection()[0]                                                                         # get the selected item
        characteristic = self.tree.item(item, "values")[0]                                                      # get the characteristic from the selected item
        self.tree.place(relx=0.6, rely=0.6, anchor='center')
        self.add_entry.place(relx=0.695, rely=0.32, anchor='ne', width=30, height=42)                           # move the add_entry button so it aligns
        self.kill_entry.place(relx=0.695, rely=0.36, anchor="ne", width=30, height=42)                          # move the kill_entry button -//-
        self.hide_button.place(relx=0.305, rely=0.3435, anchor='w', width=30, height=42)
        # Execute SQL query to get all animals associated with the selected characteristic
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT a.name 
            FROM animals a 
            JOIN junction j ON a.idAnimals = j.idAnimals 
            JOIN characteristics c ON j.idCharacteristics = c.idCharacteristics 
            WHERE c.characteristic = %s
        """, (characteristic,))
        animals = cursor.fetchall()

        if hasattr(self, 'animal_tree'):                                                                        # make sure the previous fetched data is destroyed
            self.animal_tree.destroy()                                                                          # after clicking on another entry
        
        self.animal_tree = ttk.Treeview(self.root, height=len(animals), style="Treeview", show='tree')          # create a new treeview to display the animals    
        self.animal_tree["columns"]=("one")
        self.animal_tree.column("#0", width=0, stretch=tk.NO)
        self.animal_tree.column("one", width=300, stretch=tk.YES)
        self.animal_tree.place(relx=0.4, rely=0.323, anchor='n')                                                # move treeview to make sure they dont overlap

        for i, animal in enumerate(animals, start=1):
            self.animal_tree.insert("", "end", values=animal)
    
    def hide(self):                                                                                             # hide function for hide button
        self.tree.place(relx=0.5, rely=0.6, anchor='center')
        self.hide_button.place_forget()
        self.animal_tree.place_forget()
        self.add_entry.place(relx=0.595, rely=0.32, anchor='ne', width=30, height=42)
        self.kill_entry.place(relx=0.595, rely=0.36, anchor="ne", width=30, height=42)
        
    def add_entry(self):                                                                                        # prompting user for adding a query
        new_entry = simpledialog.askstring("New Entry", "Enter the new characteristic:")

        if new_entry:
            try:              
                new_animals = simpledialog.askstring("New entry", "Enter the animals you want to associate the characteristic to:")
            
                if new_animals:
                    animals = [animal.strip() for animal in new_animals.split(',')]
                    animal_ids = []
                
                    for animal in animals:
                        cursor = self.db.cursor()
                        cursor.execute("SELECT idAnimals FROM animals WHERE name = %s", (animal,))
                        result = cursor.fetchone()
                
                        if result is not None:
                            animal_ids.append(result[0])
                        else:
                            tk.messagebox.showinfo("Error", f"The animal '{animal}' was not found. Please add it first.")
                            return  # Return early if any animal is not found
                
                # Only insert the characteristic if all animals exist
                    cursor = self.db.cursor()
                    cursor.execute("INSERT INTO characteristics (characteristic) VALUES (%s)", (new_entry,))
                    self.db.commit()
                    id_characteristic = cursor.lastrowid  # Get the ID of the last inserted row
                
                    for id_animal in animal_ids:
                        cursor.execute("INSERT INTO junction (idCharacteristics, idAnimals) VALUES (%s, %s)", (id_characteristic, id_animal))
                
                    self.db.commit()
                    cursor.close()
                else:
                    tk.messagebox.showinfo("Error", f"No animals inserted in the appropriate field.")      
                self._add_treeview()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            tk.messagebox.showinfo("Error", f"No characteristic inserted in the appropriate field.")
                   
    def kill_entry(self):
        del_entry = simpledialog.askstring("Delete entry", "Enter the characteristic you want to delete (this will also disassociate the animals):")

        if del_entry:
            try:
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM characteristics WHERE characteristic = (%s)", (del_entry,))
                self.db.commit()
                cursor.close()
                self._add_treeview()
            except Exception as e:
                print(f"An error ocurred: {e}")
        else:
            tk.messagebox.showinfo("Error", f"No characteristic added in field.")
            
    def return_to_main(self):                                                                                   # delete current interface and return widgets from main
        self._clear_root()
        self.design.add_widgets()
