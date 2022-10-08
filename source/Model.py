from configparser import ConfigParser
import os
import re

class Model():
    def __init__(self):
        self.config = ConfigParser()

        self.config_file = os.path.abspath('.\\GenreSortConf.ini')
        self.config.read(self.config_file)

        self.main_directory = self.config['path']['main_directory']
        if not os.path.exists(self.main_directory): self.main_directory = os.path.abspath('.')

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
        dir_content = sorted(os.listdir(self.main_directory))
        self.song_list = [file for file in dir_content if re.search('.mp3\Z', file)]
        if self.song_list: self.selected_song = self.song_list[0]

    def save_var_in_config(self, section, var, value):
        if var == '' or value == '': return
        self.config.set(section, var, value)
        
        with open(self.config_file, 'wt') as config_file:
            self.config.write(config_file)