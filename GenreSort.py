import tkinter as tk

class GenreSort(tk.Frame):
    def __init__(self, parent, genre_dict):
        super().__init__(parent)

        self.PAD = 5
        
        self.genres = genre_dict

        columnIndex = 0
        rowIndex = 0
        alphabetic_keys = sorted(self.genres.keys())
        for genre in alphabetic_keys:
            if rowIndex == 15: 
                columnIndex += 1
                rowIndex = 0
            tk.Button(self, text=genre, width=20, command= lambda dest=self.genres[genre]: parent.move_file_to(dest)).grid(row=rowIndex, column=columnIndex, padx=self.PAD, pady=self.PAD)
            rowIndex +=1