from Model import Model

class Controller():
    def __init__(self):
        self.model = Model()

    def move_song_to(self, destination, song):
        song = self.model.selected_song
        print(destination + ' <- ' + song)