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

class Lecteur(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		
		#self.configure(bg='royalblue')
		tkinter.Label(self, text="Résultat de la génération",height = hauteurBout).grid(row = 0, column = 0, sticky="W", columnspan=2) 

		#Skip Left
		self.skip_left = PhotoImage(file="./buttons_resize/skip_left.png")
		self.skip_left_button = tkinter.Button(self)
		self.skip_left_button.grid(row = 1, column = 0, sticky="EW")
		self.skip_left_button.config(image = self.skip_left)
		
		#Play
		self.play = PhotoImage(file="./buttons_resize/play.png")
		self.play_button = tkinter.Button(self)
		self.play_button.grid(row = 1, column = 1, sticky="EW")
		self.play_button.config(image = self.play)
		
		#Pause
		self.pause = PhotoImage(file="./buttons_resize/pause.png")
		self.pause_button = tkinter.Button(self)
		self.pause_button.grid(row = 1, column = 2, sticky="EW")
		self.pause_button.config(image = self.pause)
		
		#Skip Right
		self.skip_right = PhotoImage(file="./buttons_resize/skip_right.png")
		self.skip_right_button = tkinter.Button(self)
		self.skip_right_button.grid(row = 1, column = 3, sticky="EW")
		self.skip_right_button.config(image = self.skip_right)
		
		#Some Labels
		tkinter.Label(self, text="",height = hauteurBout).grid(row = 2, column = 0, sticky="NESW") 
		tkinter.Label(self, text="Télécharger").grid(row = 2, column = 0, sticky="W") 
		tkinter.Label(self, text="Choix de l'extension :",height = hauteurBout).grid(row = 3, column = 0, sticky="W") 
		
		#Combobox
		self.extension = ttk.Combobox(self,state='readonly', values = [".midi",".wav"],width="5")
		self.extension.current(0)
		self.extension.grid(row=4, column=0, sticky = "w")
		
		#Sélection dossier
		tkinter.Label(self, text="Sélectionner un dossier",height = hauteurBout).grid(row = 3, column = 3, sticky="W", columnspan=2)
		self.UF = tkinter.Button(self, text="Choisir",command = lambda:[master.switch_frame(self.Browser())])
		self.UF.grid(row = 4, column = 3, sticky="W")

		#Download
		self.download = PhotoImage(file="./buttons_resize/DownloadButton.png")
		self.download_button = tkinter.Button(self)
		self.download_button.grid(row = 5, column = 1, sticky="EW")
		self.download_button.config(image = self.download)
	
	def Browser(self):
		filename = filedialog.askdirectory(initialdir = "/")
		new_text = "Ici le chemin"
		self.entry_text.set(new_text)		
	




