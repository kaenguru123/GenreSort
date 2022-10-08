import tkinter as tk
import pygame

class MusicPlayer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        pygame.init()
        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()