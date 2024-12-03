import tkinter as tk

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
            selectmode=tk.SINGLE)
        self.listbox_songs.pack()