from configparser import ConfigParser
import os
from tkinter import filedialog
from FileView import FileView

class Model():
    def __init__(self):
        self.config = ConfigParser()

        self.config_file = os.path.abspath('.\\GenreSortConf.ini')
        self.config.read(self.config_file)

        self.main_directory = self.config['path']['main_directory']
        self.update_genre_dict()
        self.selected_song = None

    def update_genre_dict(self):
        self.genre_dict = self.config._sections['genre']

    def save_var_in_config(self, section, var, value):
        if var == '' or value == '': return
        self.config.set(section, var, value)
        
        with open(self.config_file, 'wt') as config_file:
            self.config.write(config_file)

    def add_genre(self, genre):
        self.save_var_in_config('genre', genre, '\\' + genre)
        return ''

    def open_directory(self):
        path = filedialog.askdirectory(initialdir=self.main_directory, title='select directory with music')
        if not path == '':
            self.main_directory = path
            self.save_var_in_config('path', 'main_directory', path)
            return path
        else:
            return self.main_directory
