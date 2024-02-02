import tkinter as tk

class CharacteristicsInterface:
    def __init__(self, root, design):
        self.root = root
        self.design = design
        
    def open_characteristics_interface(self):
        for widget in self.root.winfo_children():                                                                               
            widget.destroy()

        char_interface_title = tk.Label(self.root, text="CHARACTERISTICS", bg="#333333", fg="white", font=("Montserrat", 50, "bold"))
        char_interface_title.place(x=645, y=200)
        
        def enter_return_button(e):
            return_home['background'] = '#333333'
        
        def leave_return_button(e):
            return_home['background'] = '#4e4e4e'
            
        return_home = tk.Button(self.root, text="<", bg="#4e4e4e", fg="white", font=("Montserrat", 25, "bold"),
                                borderwidth=0, cursor="hand2", command=self.return_to_main)
        return_home.place(x=100, y=100)
        return_home.bind("<Enter>", enter_return_button)
        return_home.bind("<Leave>", leave_return_button)
        
    def return_to_main(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.design.add_widgets()
