import tkinter as tk
from Controller import Controller

class GenreSort(tk.Frame):
    PAD = 5
    def __init__(self, parent, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.genres = self.controller.model.genre_list
        black_list = ['DUPLICATES']
        columnIndex = 0
        rowIndex = 0
        alphabetic_genres = sorted(self.genres)
        for genre in alphabetic_genres:
            if black_list.__contains__(genre): continue
            if rowIndex == 15: 
                columnIndex += 1
                rowIndex = 0
            tk.Button(self, text=genre, width=20, command= lambda dest=genre: self.controller.move_song_to(dest)).grid(row=rowIndex, column=columnIndex, padx=self.PAD, pady=self.PAD)
            rowIndex +=1
        else: 
            value_new_genre = tk.StringVar()
            tk.Entry(self, width=25, textvariable=value_new_genre).grid(row=0, column=columnIndex+1, pady=self.PAD)
            tk.Button(self, text='add', width=20, command= lambda: value_new_genre.set(self.controller.add_genre(value_new_genre.get()))).grid(row=1, column=columnIndex+1, padx=self.PAD, pady=self.PAD)