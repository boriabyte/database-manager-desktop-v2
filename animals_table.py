# IMPORTS---------------------------------------------------------
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox
from connect_to_db import get_db_connection
# ----------------------------------------------------------------

### ALL FUNCTIONS IN THIS FILE ARE EQUIVALENT TO THE ONES FROM characteristics_table
### REFER TO IT FOR ANY PROBLEMS

# ----------------------------------------------------------------

class AnimalsInterface:
    def __init__(self, root, design):
        self.root = root
        self.design = design
        self.db = get_db_connection()
        self.visualize_query = "SELECT name FROM animals"

    def open_animals_interface(self):
        self._clear_root()
        self._add_add_entry_button()
        self._add_kill_entry_button()
        self._add_interface_title("ANIMALS")
        self._add_return_home_button()
        self._add_treeview()
        self._add_hide_button()
        
    def _clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _add_interface_title(self, title):
        interface_title = tk.Label(self.root, text=title, bg="white", fg="#0078D4", font=("Montserrat", 50, "bold"))
        interface_title.place(relx=0.5, rely=0.1, anchor='n')

    def _add_return_home_button(self):
        return_home = self.design._create_button("<", self.return_to_main)
        return_home.place(relx=0.05, rely=0.1, anchor='nw')
    
    def _add_hide_button(self):
        self.hide_button= self.design._create_button("x", self.hide)
        
    def _add_add_entry_button(self):
        self.add_entry = self.design._create_button("+", self.add_entry)
        self.add_entry.place(relx=0.595, rely=0.28, anchor='ne', width=30, height=42)
    
    def _add_kill_entry_button(self):
        self.kill_entry = self.design._create_button("-", self.kill_entry)
        self.kill_entry.place(relx=0.595, rely=0.32, anchor="ne", width=30, height=42)

    def _add_treeview(self):
        style = ttk.Style()
        style.configure("Treeview", font=("Montserrat", 25), rowheight=40, foreground="#0078D4")
        style.configure("Treeview.Cell", padding=(10, 0))
        style.configure("Treeview", borderwidth=0)
        style.map('Treeview',
                background=[('selected', '#0078D4')],
                foreground=[('selected', 'white')])

        cursor = self.db.cursor()
        cursor.execute(self.visualize_query)
        rows = cursor.fetchall()

        if not hasattr(self, 'tree'):
            self.tree = ttk.Treeview(self.root, height=len(rows), style="Treeview", show='tree')
            self.tree["columns"]=("one")
            self.tree.column("#0", width=0, stretch=tk.NO)
            self.tree.column("one", width=300, stretch=tk.YES)
            self.tree.place(relx=0.5, rely=0.6, anchor='center')
            self.tree.bind("<Enter>", lambda e: self.tree.config(cursor="hand2"))
            self.tree.bind("<Leave>", lambda e: self.tree.config(cursor=""))
            self.tree.bind("<Double-1>", self.on_treeview_click)
            
        for i in self.tree.get_children():
            self.tree.delete(i)

        for i, row in enumerate(rows, start=1):
            self.tree.insert("", "end", values=row)

    def on_treeview_click(self, event):
        item = self.tree.selection()[0]  # Get the selected item
        animal = self.tree.item(item, "values")[0]  # Get the characteristic from the selected item
        self.tree.place(relx=0.6, rely=0.6, anchor='center')
        self.add_entry.place(relx=0.695, rely=0.28, anchor='ne', width=30, height=42)  # Move the add_entry button
        self.kill_entry.place(relx=0.695, rely=0.32, anchor="ne", width=30, height=42)  # Move the kill_entry button
        self.hide_button.place(relx=0.305, rely=0.3435, anchor='w', width=30, height=42)
        # Execute SQL query to get all animals associated with the selected characteristic
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT c.characteristic 
            FROM characteristics c 
            JOIN junction j ON c.idCharacteristics = j.idCharacteristics 
            JOIN animals a ON j.idAnimals = a.idAnimals 
            WHERE a.name = %s
        """, (animal,))
        characteristics = cursor.fetchall()

        if hasattr(self, 'characteristic_tree'):
            self.characteristic_tree.destroy()
        
        # Create a new treeview to display the animals
        self.characteristic_tree = ttk.Treeview(self.root, height=len(characteristics), style="Treeview", show='tree')
        self.characteristic_tree["columns"]=("one")
        self.characteristic_tree.column("#0", width=0, stretch=tk.NO)
        self.characteristic_tree.column("one", width=300, stretch=tk.YES)
        self.characteristic_tree.place(relx=0.4, rely=0.323, anchor='n')  # Place the treeview to the left of the main treeview

        for i, characteristic in enumerate(characteristics, start=1):
            self.characteristic_tree.insert("", "end", values=characteristic)
    
    def hide(self):
        self.tree.place(relx=0.5, rely=0.6, anchor='center')
        self.hide_button.place_forget()
        self.characteristic_tree.place_forget()
        self.add_entry.place(relx=0.595, rely=0.28, anchor='ne', width=30, height=42)
        self.kill_entry.place(relx=0.595, rely=0.32, anchor="ne", width=30, height=42)
        
    def add_entry(self):
        new_entry = simpledialog.askstring("New Entry", "Enter the new animal:")

        if new_entry:
            try:                
                new_characteristics = simpledialog.askstring("New entry", "Enter the characteristics you want to associate the animal to:")
            
                if new_characteristics:
                    characteristics = [characteristic.strip() for characteristic in new_characteristics.split(',')]
                    characteristic_ids = []
                
                    for characteristic in characteristics:
                        cursor = self.db.cursor()
                        cursor.execute("SELECT idCharacteristics FROM characteristics WHERE characteristic = %s", (characteristic,))
                        result = cursor.fetchone()
                
                        if result is not None:
                            characteristic_ids.append(result[0])
                        else:
                            tk.messagebox.showinfo("Error", f"The characteristic '{characteristic}' was not found. Please add it first.")
                            return  # Return early if any animal is not found
                
                # Only insert the characteristic if all animals exist
                    cursor = self.db.cursor()
                    cursor.execute("INSERT INTO animals (name) VALUES (%s)", (new_entry,))
                    self.db.commit()
                    id_animal = cursor.lastrowid  # Get the ID of the last inserted row
                
                    for id_characteristic in characteristic_ids:
                        cursor.execute("INSERT INTO junction (idCharacteristics, idAnimals) VALUES (%s, %s)", (id_characteristic, id_animal))
                
                    self.db.commit()
                    cursor.close()
                else:
                    tk.messagebox.showinfo("Error", f"No characteristics inserted in the appropriate field.")      
                self._add_treeview()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            tk.messagebox.showinfo("Error", f"No animal inserted in the appropriate field.")
                
    def kill_entry(self):
        del_entry = simpledialog.askstring("Delete entry", "Enter the animal you want to delete (this will also disassociate the characteristics):")

        if del_entry:
            try:
                cursor = self.db.cursor()
                cursor.execute("DELETE FROM animals WHERE name = (%s)", (del_entry,))
                self.db.commit()
                cursor.close()

                self._add_treeview()
            except Exception as e:
                print(f"An error ocurred: {e}")
        else:
            tk.messagebox.showinfo("Error", f"No animal inserted in the appropriate field.")
            
    def return_to_main(self):
        self._clear_root()
        self.design.add_widgets()
