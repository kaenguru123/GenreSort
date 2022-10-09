import tkinter as tk
from Controller import Controller

class GenreSort(tk.Frame):
    PAD = 5
    def __init__(self, parent, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.genres = self.controller.model.genre_dict

        columnIndex = 0
        rowIndex = 0
        alphabetic_keys = sorted(self.genres.keys())
        for genre in alphabetic_keys:
            if rowIndex == 15: 
                columnIndex += 1
                rowIndex = 0
            tk.Button(self, text=genre, width=20, command= lambda dest=self.genres[genre]: self.controller.move_song_to(dest)).grid(row=rowIndex, column=columnIndex, padx=self.PAD, pady=self.PAD)
            rowIndex +=1