import tkinter as tk
import pygame

class MusicPlayer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        pygame.init()
        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        self.build_button_frame()

    def build_button_frame(self):
        # Inserting Play Button
        playbtn = tk.Button(self,text="PLAYSONG",command=self.playsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=0,padx=10,pady=5)
        # Inserting Pause Button
        #playbtn = tk.Button(buttonframe,text="PAUSE",command=self.pausesong,width=8,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=1,padx=10,pady=5)
        # Inserting Unpause Button
        #playbtn = tk.Button(buttonframe,text="UNPAUSE",command=self.unpausesong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=2,padx=10,pady=5)
        # Inserting Stop Button
        #playbtn = tk.Button(buttonframe,text="STOPSONG",command=self.stopsong,width=10,height=1,font=("times new roman",16,"bold"),fg="navyblue",bg="pink").grid(row=0,column=3,padx=10,pady=5)

    def playsong(self):
        # Displaying Status
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.track.get())
        # Playing Selected Song
        pygame.mixer.music.play()
