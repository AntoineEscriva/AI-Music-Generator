# !/usr/bin/python3
#coding: utf-8

import tkinter
import tkinter.font as tkFont
from tkinter import filedialog 
from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk

largeurBout = 15
hauteurBout = 2
margeX = 0
margeY = 0

#######################################################

class Lecteur(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self.frame = None
		self.title("Génération musique aléatoire")
		self.geometry("600x400")
		self.switch_frame(Menu)

	def switch_frame(self, frame_class):
		newFrame = frame_class(self)
		if(self.frame is not None):
			self.frame.grid_remove()
		self.frame = newFrame
		self.frame.grid(padx = 20, pady = 20, sticky = "ewsn")
		
#######################################################

class Menu(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		
		tkinter.Label(self, text="Résultat de la",height = hauteurBout).grid(row = 0, column = 0, sticky="NESW") 
		tkinter.Label(self, text="génération:",height = hauteurBout).grid(row = 0, column = 1, sticky="NESW")
		
		self.skip_left = PhotoImage(file="./buttons_resize/skip_left.png")
		self.skip_left_button = tkinter.Button(self)
		self.skip_left_button.grid(row = 1, column = 1, sticky="EW")
		self.skip_left_button.config(image = self.skip_left)
		
		self.play = PhotoImage(file="./buttons_resize/play.png")
		self.play_button = tkinter.Button(self)
		self.play_button.grid(row = 1, column = 2, sticky="EW")
		self.play_button.config(image = self.play)
		
		self.pause = PhotoImage(file="./buttons_resize/pause.png")
		self.pause_button = tkinter.Button(self)
		self.pause_button.grid(row = 1, column = 3, sticky="EW")
		self.pause_button.config(image = self.pause)
		
		self.skip_right = PhotoImage(file="./buttons_resize/skip_right.png")
		self.skip_right_button = tkinter.Button(self)
		self.skip_right_button.grid(row = 1, column = 4, sticky="EW")
		self.skip_right_button.config(image = self.skip_right)
		
		tkinter.Label(self, text="",height = hauteurBout).grid(row = 2, column = 0, sticky="NESW") 
		tkinter.Label(self, text="Télécharger :").grid(row = 3, column = 0, sticky="NESW") 
		tkinter.Label(self, text="Extension ?",height = hauteurBout).grid(row = 4, column = 0, sticky="NESW") 
		
		self.extension = ttk.Combobox(self,state='readonly', values = [".midi",".wav"],width="5")
		self.extension.current(0)
		self.extension.grid(row=4, column=1)
		
		tkinter.Label(self, text="Sélectionner",height = hauteurBout).grid(row = 5, column = 0, sticky="NESW")
		tkinter.Label(self, text="un dossier :",height = hauteurBout).grid(row = 5, column = 1, sticky="W")
		
		self.UF = tkinter.Button(self, text="Ouvrir",command = lambda:[master.switch_frame(self.Browser())])
		self.UF.grid(row = 6, column = 0, sticky="EW")

		self.download = PhotoImage(file="./buttons_resize/download.png")
		self.download_button = tkinter.Button(self)
		self.download_button.grid(row = 7, column = 2, sticky="EW")
		self.download_button.config(image = self.download)
	
	def Browser(self):
		filename = filedialog.askdirectory(initialdir = "/")
		new_text = "Ici le chemin"
		self.entry_text.set(new_text)		
if __name__ == "__main__":

	app = Lecteur()	
	app.mainloop()
	




