import tkinter as tk
from Controller import Controller
from FileView import FileView
from GenreSort import GenreSort

class View(tk.Tk):
    def __init__(self):

        self.PAD = 5

        super().__init__()

        self.controller = Controller()

        self.menu = tk.Menu(self)
        self.make_menu()

        self.build_main_widgets()

        self.value_music_directory = tk.StringVar(value=self.controller.model.main_directory)
    
        self.title('GenreSort')
        self.minsize(1500,750)
        self.resizable(0,0)

        self.mainloop()

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
        self.file_view = FileView(self, self.controller.model.main_directory)
        self.file_view.grid(row=0, column=0, rowspan=15, padx=self.PAD, pady=self.PAD, sticky='n')
        tk.Button(self, text='select first', width=50, command= lambda: self.file_view.select_first()).grid(row=2, column=2, padx=self.PAD, pady=self.PAD)

    def make_music_player(self):
        pass

    def make_genre_sort(self):
        self.genres = self.controller.model.genre_dict

        columnIndex = 1
        rowIndex = 0
        alphabetic_keys = sorted(self.genres.keys())
        for genre in alphabetic_keys:
            if rowIndex == 15: 
                columnIndex += 1
                rowIndex = 0
            tk.Button(self, text=genre, width=20, command= lambda dest=self.genres[genre], song=self.file_view.get_selected(): self.controller.move_song_to(dest, song)).grid(row=rowIndex, column=columnIndex, padx=self.PAD, pady=self.PAD)
            rowIndex +=1

    def open_settings(self):
        settings = tk.Toplevel()
        settings.lift()
        settings.grab_set()

        self.entry_music_directory = tk.Entry(settings, width=100, textvariable=self.value_music_directory, state='readonly')
        self.entry_music_directory.grid(row=0, column=0, padx=self.PAD, pady=self.PAD)

        tk.Button(settings, text='select directory', width=50, command= lambda: self.value_music_directory.set(self.controller.model.open_directory())).grid(row=0, column=1, padx=self.PAD, pady=self.PAD)
        tk.Button(settings, text='add genre', width=50, command= lambda: self.open_add_genre()).grid(row=1, column=0, columnspan=2, padx=self.PAD, pady=self.PAD, sticky='e')
        tk.Button(settings, text='exit', width=50, command= lambda: self.exit_settings(settings)).grid(row=2, column=0, columnspan=2, padx=self.PAD, pady=self.PAD, sticky='e')

    def exit_settings(self, settings):
        settings.destroy()
        self.build_main_widgets()

    def open_add_genre(self):
        add_genre = tk.Toplevel()
        add_genre.lift()
        add_genre.grab_set()

        value_new_genre = tk.StringVar()

        entry_new_genre = tk.Entry(add_genre, width=100, textvariable=value_new_genre)
        entry_new_genre.grid(row=0, column=0, columnspan=2, padx=self.PAD, pady=self.PAD)

        tk.Button(add_genre, text='add', width=40, command= lambda: value_new_genre.set(self.controller.model.add_genre(value_new_genre.get()))).grid(row=1, column=1, padx=self.PAD, pady=self.PAD)
        tk.Button(add_genre, text='save changes and exit', width=40, command= lambda: self.exit_add_genre(add_genre)).grid(row=1, column=0, padx=self.PAD, pady=self.PAD)

    def exit_add_genre(self, add_genre):
        self.controller.model.update_genre_dict()
        add_genre.destroy()

def main():
    GenreSort = View()

if __name__ == '__main__':
    main()