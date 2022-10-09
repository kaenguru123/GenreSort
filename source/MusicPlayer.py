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
        self.track_slider = tk.Scale(self, from_=0, to=500, length=300, orient=tk.HORIZONTAL)
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