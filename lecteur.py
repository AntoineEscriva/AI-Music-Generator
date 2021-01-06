# !/usr/bin/python3
#coding: utf-8

import tkinter
import tkinter.font as tkFont
from tkinter import filedialog 
from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import simpledialog
import musique as musique


LST_Types = [ ( "Fichier texte" , ".txt" ) , ( "Script python" , ".py" ) , ( "Autres types" , ".*" ) ]
largeurBout = 15
hauteurBout = 2
margeX = 0
margeY = 0
		
#######################################################

class Lecteur(tkinter.Frame):
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		
		#Réglages de la police
		self.titre = tkFont.Font(family='Helvetica', size=20)
		self.texte = tkFont.Font(family='Helvetica', size=13)
		#Couleur de fond
		self.configure(bg='white')
		
		#Titre
		tkinter.Label(self, text="Résultat de la génération", font = self.titre, height = hauteurBout, bg='white').grid(row = 0, column = 0, sticky="W", columnspan=2) 
		
		#Skip Left
		self.skip_left = PhotoImage(file="./buttons_resize/sl1.png")
		self.skip_left_button = tkinter.Button(self)
		self.skip_left_button.grid(row = 1, column = 0, sticky="W")
		self.skip_left_button.config(image = self.skip_left, bd=0,bg='white')
		
		#Play
		self.play = PhotoImage(file="./buttons_resize/pl1.png")
		self.play_button = tkinter.Button(self)
		self.play_button.grid(row = 1, column = 0)
		self.play_button.config(image = self.play, bd=0,bg='white')
		
		#Pause
		self.pause = PhotoImage(file="./buttons_resize/pa1.png")
		self.pause_button = tkinter.Button(self)
		self.pause_button.grid(row = 1, column =0, sticky="E")
		self.pause_button.config(image = self.pause, bd=0, bg='white')
		
		#Skip Right
		self.skip_right = PhotoImage(file="./buttons_resize/sr1.png")
		self.skip_right_button = tkinter.Button(self)
		self.skip_right_button.grid(row = 1, column = 1)
		self.skip_right_button.config(image = self.skip_right, bd=0,bg='white')
		
		#Some Labels
		#Un label vide pour faire de l'espace
		tkinter.Label(self, text="",height = hauteurBout,bg='white').grid(row = 2, column = 0, sticky="NESW") 
		tkinter.Label(self, text="Enregistrement",bg='white', font = self.titre).grid(row = 2, column = 0, sticky="W") 
		tkinter.Label(self, text="Choix de l'extension :", font = self.texte, height = hauteurBout,bg='white').grid(row = 3, column = 0, sticky="W") 
		
		#Combobox
		self.extension = ttk.Combobox(self,state='readonly', values = [".midi",".wav"],width="5")
		self.extension.current(0)
		self.extension.grid(row=4, column=0, sticky = "EW")
		
		#Zone pour l'affichage du chemin
		#self.entry_text = tkinter.StringVar()
		#self.usr_input = ttk.Entry(self, state='readonly', textvariable=self.entry_text)
		#self.usr_input.grid(row=4,column=3, sticky='EW')
		
		#Enregistrement
		self.download_button = tkinter.Button(self, text="Enregistrer sous", font = self.texte,  command = lambda:[self.FNC_Selection(self.extension.get())])
		self.download_button.grid(row = 4, column =2, sticky="E")
		self.download_button.config(bg='white')
		#self.download_button.config(image = self.download,bg='white')
		
		
		#Bouton Retour
		self.retour = tkinter.Button(self, text="Retour", font = self.texte, command=lambda : [master.switch_frame(musique.Menu)])
		self.retour.grid(row=7,column=0, sticky="WS")
		self.retour.config(bd=1, bg="white")
		
		#tkinter.Label(self, text="  ", bg="white").grid(row=6, column=0)
			
	
	#Fonction d'enregistrement de fichier
	def FNC_Selection(self, formatChoisi) :
		if(formatChoisi==".midi"):
			extension = [("fichier MIDI",".midi")]
			defaut = '".midi"'
		else:
			extension = [("fichier WAV",".wav")]
			defaut = '".wav"'
		file = tkinter.filedialog.asksaveasfile(filetypes = extension, title="Choisissez le nom de fichier", defaultextension = defaut)

	#Fonction de l'explorateur de fichier
	def BrowserFile(self):
		filename = filedialog.askdirectory(initialdir = "/")
		self.entry_text.set(filename)		
	




