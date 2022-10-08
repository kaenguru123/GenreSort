import tkinter as tk
from Controller import Controller

class FileView(tk.Frame):
    def __init__(self, parent, song_list):
        super().__init__(parent)

        self.listbox_songs = None
        
        self.tk_song_list = tk.Variable(value=song_list)
        self.make_listbox()
    
    def make_listbox(self):
        self.listbox_songs = tk.Listbox(self,
            listvariable=self.tk_song_list, 
            height=40, 
            width=100, 
            selectmode=tk.SINGLE, 
            yscrollcommand=None)
        self.listbox_songs.activate(0)
        self.listbox_songs.pack()

    def select_first(self):
        self.listbox_songs.activate(0)
    
    def get_selected(self):
        selected = self.listbox_songs.curselection()
        return selected

    # def update_selected(self):
    #     self.controller.model.selected_song = self.listbox_songs.curselection()


    