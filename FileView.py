import tkinter as tk
import re
from os import listdir

class FileView(tk.Frame):
    def __init__(self, parent, directory):
        selected_song = None
        super().__init__(parent)

        self.PAD = 5

        self.song_list = None
        self.tk_song_list = None
        self.listbox_songs = None
        
        self.__init__song_lists(directory)
        self.make_listbox()

    def __init__song_lists(self, directory):
        file_list = listdir(directory)

        self.song_list = [file for file in file_list if re.search('.mp3\Z', file)]

        self.tk_song_list = tk.Variable(value=self.song_list)

    
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


    