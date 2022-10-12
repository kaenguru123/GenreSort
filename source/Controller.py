import os
from tkinter import filedialog
from Model import Model

class Controller():
    def __init__(self):
        self.model = Model()
        self.clear_track = None

    def move_song_to(self, destination):
        self.clear_track()

        song = self.model.current_song
        directory = self.model.main_directory.replace('/', '\\')

        dest_dir = os.path.join(directory, destination)
        dest = os.path.join(dest_dir, song)
        origin = os.path.join(directory, song)
        
        if not os.path.isdir(dest_dir): os.mkdir(dest_dir)
        try:
            os.rename(origin, dest)
            print(song + ' -> ' + dest)
        except FileExistsError:
            dest_dir = os.path.join(directory, 'DUPLICATES')
            dest = os.path.join(dest_dir, song)
            if not os.path.isdir(dest_dir): os.mkdir(dest_dir)
            os.rename(origin, dest)
            print('ERR: song already exists in that genre!')

        self.model.update_song_list()
        self.model.update()

    def add_genre(self, genre):
        self.model.save_var_in_config('genre', genre, genre)
        return ''

    def open_directory(self):
        path = filedialog.askdirectory(initialdir=self.model.main_directory, title='select directory with music')
        if not path == '':
            self.model.main_directory = path
            self.model.save_var_in_config('path', 'main_directory', path)
            return path
        else:
            return self.model.main_directory
