# IMPORTS----------------------------------------------------------------------------------------------
import tkinter as tk
import ttkbootstrap as ttk
from characteristics_table import CharacteristicsInterface
# IMPORTS----------------------------------------------------------------------------------------------

class Design:
    def __init__(self, root):
        self.root = root
        self.root.title("DATABASE - ANIMAL CHARACTERISTICS")                                                                    
        self.root.state('zoomed')                                                                                               
        self.root.configure(bg='#333333')                                                                                       
        self.state_stack = []
        
    def add_widgets(self):
        welcome_label = tk.Label(self.root, text="WELCOME", bg="#333333", fg="white", font=("Montserrat", 50, "bold"))
        welcome_label.place(x=795, y=400)                                                                                       

        # functions for button/s transitions
        def enter_char_button(e):
            view_char_button['background'] = '#333333'
        
        def leave_char_button(e):
            view_char_button['background'] = '#4e4e4e'
            
        def enter_anim_button(e):
            view_anim_button['background'] = '#333333'
        
        def leave_anim_button(e):
            view_anim_button['background'] = '#4e4e4e'
        
        # btn config
        view_char_button = tk.Button(self.root, text="view characteristics", 
                                command=CharacteristicsInterface(self.root, self).open_characteristics_interface,
                                bg="#4e4e4e", fg="white", font=("Rubik", 20), borderwidth=0, cursor="hand2")
        view_char_button.bind("<Enter>", enter_char_button)                                                                     
        view_char_button.bind("<Leave>", leave_char_button)                                                                     
        view_char_button.place(x=700, y=500)

        view_anim_button = tk.Button(self.root, text="view animals",
                                bg="#4e4e4e", fg="white", font=("Rubik", 20), borderwidth=0, cursor="hand2")
        view_anim_button.bind("<Enter>", enter_anim_button)  
        view_anim_button.bind("<Leave>", leave_anim_button)
        view_anim_button.place(x=1050, y=500)
        
        def show_previous_interface(self):
        # Pop the last interface from the stack
            if self.interface_stack:
                last_interface = self.state_stack.pop()

            # Clear current widgets
                for widget in self.root.winfo_children():
                    widget.destroy()

            # Show the previous interface
                last_interface.add_widgets()
                self.state_stack.append(last_interface)