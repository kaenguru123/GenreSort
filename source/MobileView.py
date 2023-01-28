import tkinter as tk

# Controller.py
import os
from tkinter import filedialog

# ./source/Model.py
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

        self.current_song = ''
        self.song_list = []
        self.update_song_list()

        self.update = None

    def update_genre_dict(self):
        self.genre_dict = self.config._sections['genre']

    def update_song_list(self):
        dir_content = sorted(os.listdir(self.main_directory))
        self.song_list = [file for file in dir_content if re.search('.mp3\Z', file)]
        if self.song_list: self.current_song = self.song_list[0]

    def save_var_in_config(self, section, var, value):
        if var == '' or value == '': return
        self.config.set(section, var, value)
        
        with open(self.config_file, 'wt') as config_file:
            self.config.write(config_file)
    
    def get_path_curr_song(self):
        return os.path.join(self.main_directory.replace('/', '\\'), self.current_song)
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

# ./source/FileView.py
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
            height=10, 
            width=50, 
            selectmode=tk.SINGLE)
        self.listbox_songs.pack()
# ./source/GenreSort.py
import tkinter as tk
from Controller import Controller

class GenreSort(tk.Frame):
    PAD = 0
    def __init__(self, parent, controller: Controller):
        super().__init__(parent)

        self.controller = controller
        self.genres = self.controller.model.genre_dict

        alphabetic_keys = sorted(self.genres.keys())
        
        text = tk.Text(self, width=30)
        text.pack(side="left")
        sb = tk.Scrollbar(self, command=text.yview)
        sb.pack(side="right")
        text.configure(yscrollcommand=sb.set)
        
        for genre in alphabetic_keys:
            button = tk.Button(self, text=genre, width=20, command= lambda dest=self.genres[genre]: self.controller.move_song_to(dest))
            text.window_create("end", window=button)
            text.insert("end", "\n")
            
        text.configure(state="disabled")


        
            
# ./source/MusicPlayer.py
from enum import Enum
import tkinter as tk
from turtle import width
import pygame

class MusicPlayer(tk.Frame):
    STATUS_PLAY = u'\u25B6'
    STATUS_PAUSE = u'\u23F8'
    STATUS_STOP = u'\u23F9'

    def __init__(self, parent):
        super().__init__(parent)

        self.curr_pos = 0

        pygame.init()
        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        self.build_button_frame()
    
    def clear_track(self):
        pygame.mixer.music.unload()

    def update_mp(self, new_track):
        self.track.set(new_track)
        if self.status.get() == self.STATUS_PLAY:
            pygame.mixer.music.load(self.track.get())
            pygame.mixer.music.play()

    def build_button_frame(self):
        tk.Label(self,textvariable=self.status,font=('times new roman',24,'bold'),bg='orange',fg='gold').grid(row=0,column=0,padx=10,pady=5)
        tk.Button(self,text=u'\u23EF',command=self.play_pause,width=10,height=1,font=('times new roman',16,'bold'),fg='navyblue',bg='pink').grid(row=0,column=1,padx=10,pady=5)
        tk.Button(self,text=u'\u23F9',command=self.stopsong,width=10,height=1,font=('times new roman',16,'bold'),fg='navyblue',bg='pink').grid(row=0,column=2,padx=10,pady=5)
        tk.Button(self,text='set',command=self.set_track_pos,width=10,height=1,font=('times new roman',16,'bold'),fg='navyblue',bg='pink').grid(row=1,column=0,padx=10,pady=5)
        self.track_slider = tk.Scale(self, from_=0, to=500, length=100, orient=tk.HORIZONTAL)
        self.track_slider.grid(row=1, column=1, columnspan=2)

    def set_track_pos(self):
        new_pos = self.track_slider.get()
        try:
            pygame.mixer.music.set_pos(new_pos)
        except:
            self.stopsong()
            self.play_pause()

    def play_pause(self):
        status = self.status.get()

        if  status == self.STATUS_PLAY:
            self.status.set(self.STATUS_PAUSE)
            pygame.mixer.music.pause()

        elif status == self.STATUS_PAUSE:
            self.status.set(self.STATUS_PLAY)
            pygame.mixer.music.unpause()

        else:
            self.status.set(self.STATUS_PLAY)
            pygame.mixer.music.load(self.track.get())
            pygame.mixer.music.play()

    def stopsong(self):
        self.status.set(self.STATUS_STOP)
        pygame.mixer.music.stop()
class View(tk.Tk):
    PAD = 0
    def __init__(self):
        super().__init__()

        self.controller = Controller()
        self.controller.model.update = lambda: self.update()

        self.menu = tk.Menu(self)
        self.make_menu()

        self.build_main_widgets()
        self.controller.clear_track = lambda: self.music_player.clear_track()

        self.value_music_directory = tk.StringVar(value=self.controller.model.main_directory)
    
        self.title('GenreSort')
        self.resizable(0,0)

        self.mainloop()

    def update(self):
        self.file_view.listbox_songs.delete(0)
        self.music_player.update_mp(self.controller.model.get_path_curr_song())

    def build_main_widgets(self):
        self.make_file_view()
        self.make_genre_sort()
        self.make_music_player()

    def make_menu(self):
        start_menu = tk.Menu(self.menu, tearoff = 0)
        start_menu.add_command(label='Settings', command=self.open_settings)

        self.menu.add_cascade(label='Start', menu=start_menu)
        self.config(menu=self.menu)

    def make_file_view(self):
        self.file_view = FileView(self, self.controller.model.song_list)
        self.file_view.grid(row=0, column=0, padx=self.PAD, pady=self.PAD, sticky='n')

    def make_music_player(self):
        self.music_player = MusicPlayer(self)
        self.music_player.track.set(self.controller.model.get_path_curr_song())
        self.music_player.grid(row=2, column=0, padx=self.PAD, pady=self.PAD)

    def make_genre_sort(self):
        genre_sort = GenreSort(self, self.controller)
        genre_sort.grid_forget()
        genre_sort.grid(row=1, column=0, padx=self.PAD, pady=self.PAD)

    def open_settings(self):
        settings = tk.Toplevel()
        settings.lift()
        settings.grab_set()
        settings.resizable(0,0)

        self.entry_music_directory = tk.Entry(settings, width=50, textvariable=self.value_music_directory, state='readonly')
        self.entry_music_directory.grid(row=0, column=0, padx=self.PAD, pady=self.PAD)

        tk.Button(settings, text='select directory', width=50, command= lambda: self.value_music_directory.set(self.controller.open_directory())).grid(row=0, column=1, padx=self.PAD, pady=self.PAD)
        tk.Button(settings, text='add genre', width=50, command= lambda: self.open_add_genre()).grid(row=1, column=0, columnspan=2, padx=self.PAD, pady=self.PAD, sticky='e')
        tk.Button(settings, text='exit', width=50, command= lambda: self.exit_settings(settings)).grid(row=2, column=0, columnspan=2, padx=self.PAD, pady=self.PAD, sticky='e')

    def exit_settings(self, settings):
        settings.destroy()
        self.controller.model.update_genre_dict()
        self.controller.model.update_song_list()
        self.build_main_widgets()

    def open_add_genre(self):
        add_genre = tk.Toplevel()
        add_genre.lift()
        add_genre.grab_set()
        add_genre.resizable(0,0)

        value_new_genre = tk.StringVar()

        entry_new_genre = tk.Entry(add_genre, width=50, textvariable=value_new_genre)
        entry_new_genre.grid(row=0, column=0, columnspan=2, padx=self.PAD, pady=self.PAD)

        tk.Button(add_genre, text='add', width=40, command= lambda: value_new_genre.set(self.controller.add_genre(value_new_genre.get()))).grid(row=1, column=1, padx=self.PAD, pady=self.PAD)
        tk.Button(add_genre, text='save changes and exit', width=40, command=add_genre.destroy).grid(row=1, column=0, padx=self.PAD, pady=self.PAD)

def main():
    GenreSort = View()

if __name__ == '__main__':
    main()