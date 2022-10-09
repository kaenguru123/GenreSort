import tkinter as tk
from Controller import Controller
from FileView import FileView
from GenreSort import GenreSort
from MusicPlayer import MusicPlayer

class View(tk.Tk):
    PAD = 10
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
        self.music_player.grid(row=1, column=0, padx=self.PAD, pady=self.PAD)

    def make_genre_sort(self):
        genre_sort = GenreSort(self, self.controller)
        genre_sort.grid_forget()
        genre_sort.grid(row=0, column=1, padx=self.PAD, pady=self.PAD)

    def open_settings(self):
        settings = tk.Toplevel()
        settings.lift()
        settings.grab_set()
        settings.resizable(0,0)

        self.entry_music_directory = tk.Entry(settings, width=100, textvariable=self.value_music_directory, state='readonly')
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

        entry_new_genre = tk.Entry(add_genre, width=100, textvariable=value_new_genre)
        entry_new_genre.grid(row=0, column=0, columnspan=2, padx=self.PAD, pady=self.PAD)

        tk.Button(add_genre, text='add', width=40, command= lambda: value_new_genre.set(self.controller.add_genre(value_new_genre.get()))).grid(row=1, column=1, padx=self.PAD, pady=self.PAD)
        tk.Button(add_genre, text='save changes and exit', width=40, command=add_genre.destroy).grid(row=1, column=0, padx=self.PAD, pady=self.PAD)

def main():
    GenreSort = View()

if __name__ == '__main__':
    main()