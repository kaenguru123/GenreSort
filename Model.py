from configparser import ConfigParser
import os
import re
from tkinter import filedialog

class Model():
    def __init__(self):
        self.config = ConfigParser()

        self.config_file = os.path.abspath('.\\GenreSortConf.ini')
        self.config.read(self.config_file)

        self.main_directory = self.config['path']['main_directory']
        self.genre_dict = {}
        self.update_genre_dict()
        self.selected_song = ''
        self.song_list = []
        
        self.update_song_list()

        try:
            self.update()
        except:
            self.update = None

    def update_genre_dict(self):
        self.genre_dict = self.config._sections['genre']

    def update_song_list(self):
        if not os.path.exists(self.main_directory): self.main_directory = os.path.abspath('.')
        dir_content = sorted(os.listdir(self.main_directory))
        self.song_list = [file for file in dir_content if re.search('.mp3\Z', file)]
        if self.song_list: self.selected_song = self.song_list[0]

    def save_var_in_config(self, section, var, value):
        if var == '' or value == '': return
        self.config.set(section, var, value)
        
        with open(self.config_file, 'wt') as config_file:
            self.config.write(config_file)

    def add_genre(self, genre):
        self.save_var_in_config('genre', genre, genre)
        return ''

    def open_directory(self):
        path = filedialog.askdirectory(initialdir=self.main_directory, title='select directory with music')
        if not path == '':
            self.main_directory = path
            self.save_var_in_config('path', 'main_directory', path)
            return path
        else:
            return self.main_directory

    def move_song_to(self, destination):
        song = self.selected_song
        directory = self.main_directory.replace('/', '\\')

        dest_dir = os.path.join(directory, destination)
        dest = os.path.join(dest_dir, song)
        origin = os.path.join(directory, song)
        
        if not os.path.isdir(dest_dir): os.mkdir(dest_dir)
        os.rename(origin, dest)

        self.update_song_list()
        self.update()
