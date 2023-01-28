import tkinter as tk
from Controller import Controller

class GenreSort(tk.Frame):
    PAD = 0
    def __init__(self, parent, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.genres = self.controller.model.genre_dict

        alphabetic_keys = sorted(self.genres.keys())
        
        text = tk.Text(self, width=30)
        text.pack(side="left")
        sb = tk.Scrollbar(self, command=text.yview)
        sb.pack(side="right")
        text.configure(yscrollcommand=sb.set)
        
        for genre in alphabetic_keys:
            button = tk.Button(self, text=genre, width=20, command= lambda dest=self.genres[genre]: self.controller.move_song_to(dest))
            text.window_create("end", window=button)
            text.insert("end", "\n")
            
        text.configure(state="disabled")


        
            