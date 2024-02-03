# main_design.py
import tkinter as tk
from characteristics_table import CharacteristicsInterface
from animals_table import AnimalsInterface

class Design:
    def __init__(self, root):
        self.root = root
        self.root.title("DATABASE - ANIMAL CHARACTERISTICS")                                                                    
        self.root.state('zoomed')                                                                                               
        self.root.configure(bg='white')                                                                                       
        self.state_stack = []

    def add_widgets(self):
        self._add_welcome_label()
        self._add_view_char_button()
        self._add_view_anim_button()
        self._add_footer_label()
        self._message()

    def _add_welcome_label(self):
        welcome_label = tk.Label(self.root, text="WELCOME", bg="white", fg="#0078D4", font=("Montserrat", 50, "bold"))
        welcome_label.place(relx=0.5, rely=0.45, anchor='center')
    
    def _message(self):
        message_label = tk.Label(self.root, text="What would you like to do?", bg="white", fg="#0078D4", font=("Montserrat", 20, "bold"))
        message_label.place(relx=0.5, rely=0.55, anchor='center')

    def _add_view_char_button(self):
        view_char_button = self._create_button("view characteristics", CharacteristicsInterface(self.root, self).open_characteristics_interface)
        view_char_button.place(relx=0.5, rely=0.6, anchor='center')

    def _add_view_anim_button(self):
        view_anim_button = self._create_button("view animals", AnimalsInterface(self.root, self).open_animals_interface)
        view_anim_button.place(relx=0.5, rely=0.65, anchor='center')

    def _create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command, bg="white", fg="#0078D4", font=("Rubik", 20), borderwidth=0, cursor="hand2")
        button.bind("<Enter>", self._enter_button)
        button.bind("<Leave>", self._leave_button)
        return button
    
    def _add_footer_label(self):
        footer_label = tk.Label(self.root, text="HORIA SCARLAT  |  PIBD 2023-2024", bg="white", fg="#0078D4", font=("Montserrat", 10, "bold"))
        footer_label.place(relx=0.5, rely=0.99, anchor='s')

    def _enter_button(self, e):
        e.widget['background'] = '#0078D4'
        e.widget['foreground'] = 'white'

    def _leave_button(self, e):
        e.widget['background'] = 'white'
        e.widget['foreground'] = '#0078D4'
