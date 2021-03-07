# !/usr/bin/python3
#coding: utf-8

import tkinter
import tkinter.font as tkFont
from tkinter import filedialog 
from tkinter import ttk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import simpledialog
from files import musique as musique
import pygame
from os import walk

hauteurBout = 10
largeurBout = 15
hauteurBout = 2
margeX = 0
margeY = 0

#######################################################
# Classe du lecteur de musique
#######################################################

class Lecteur(tkinter.Frame):
	def __init__(self, master):
		#Initialisation du Cadre du lecteur MP3
		tkinter.Frame.__init__(self, master)
		
		#Réglages de la police du titre puis du texte
		self.titre = tkFont.Font(family='Helvetica', size=20)
		self.texte = tkFont.Font(family='Helvetica', size=13)
		#Couleur de fond
		self.configure(bg='white')
		
		#Titre
		tkinter.Label(self, text="Résultat de la génération", font = self.titre, height = hauteurBout, bg='white').grid(row = 0, column = 0, sticky="W", columnspan=2) 
		
		#Bouton Skip Left
		#Affectation d'une image de bouton à une variable
		self.skip_left = PhotoImage(file="./buttons_resize/sl1.png")
		#Création du bouton
		self.skip_left_button = tkinter.Button(self)
		#Placement du bouton
		self.skip_left_button.grid(row = 1, column = 0, sticky="W")
		#Quelques réglages d'apparence : couleur du background, épaisseur des bordures, et affectation de l'image au bouton
		self.skip_left_button.config(image = self.skip_left, bd=0,bg='white')
		
		#Bouton Play
		#Ajout d'un compteur au bouton play
		self.comptePlay = 0
		#Affectation d'une image de bouton à une variable
		self.play = PhotoImage(file="./buttons_resize/pl1.png")	
		#Création du bouton
		self.play_button = tkinter.Button(self)
		#Placement du bouton
		self.play_button.grid(row = 1, column = 0)
		#Quelques réglages d'apparence : couleur du background, épaisseur des bordures, et affectation de l'image au bouton
		self.play_button.config(image = self.play, bd=0,bg='white', command= lambda: [self.playUnPause()])
		
		
		#Bouton Pause
		#Affectation d'une image de bouton à une variable
		self.pause = PhotoImage(file="./buttons_resize/pa1.png")
		#Création du bouton
		self.pause_button = tkinter.Button(self)
		#Placement du bouton
		self.pause_button.grid(row = 1, column =0, sticky="E")
		#Quelques réglages d'apparence : couleur du background, épaisseur des bordures, et affectation de l'image au bouton
		self.pause_button.config(image = self.pause, bd=0, bg='white', command = lambda: [pygame.mixer.music.pause()])
		
		#Bouton Skip Right
		#Affectation d'une image de bouton à une variable
		self.skip_right = PhotoImage(file="./buttons_resize/sr1.png")
		#Création du bouton
		self.skip_right_button = tkinter.Button(self)
		#Placement du bouton
		self.skip_right_button.grid(row = 1, column = 1)
		#Quelques réglages d'apparence : couleur du background, épaisseur des bordures, et affectation de l'image au bouton
		self.skip_right_button.config(image = self.skip_right, bd=0,bg='white', command = lambda: [pygame.mixer.music.set_endevent()])
		
		#Some Labels
		#Un label vide pour faire de l'espace
		tkinter.Label(self, text="",height = hauteurBout,bg='white').grid(row = 2, column = 0, sticky="NESW") 
		#Création et placement du Label Enregistrement, avec background blanc
		tkinter.Label(self, text="Enregistrement",bg='white', font = self.titre).grid(row = 2, column = 0, sticky="W") 
		#Création et placement du label Choix de l'Extension
		tkinter.Label(self, text="Choix de l'extension :", font = self.texte, height = hauteurBout,bg='white').grid(row = 3, column = 0, sticky="W") 
		
		#Création d'une Combobox pour le choix de l'extension
		self.extension = ttk.Combobox(self,state='readonly', values = [".midi",".wav"],width="5")
		#Selection de l'item par défaut
		self.extension.current(0)
		#Placement
		self.extension.grid(row=4, column=0, sticky = "EW")
		
		#Bouton Enregistrement
		#Création du bouton, relié à une fonction de sélection du chemin d'enregistrement (FNC_selection)
		self.download_button = tkinter.Button(self, text="Supprimer les fichiers", font = self.texte,  command = lambda:[self.supprimerFichiers()])
		#Placement
		self.download_button.grid(row = 4, column =2, sticky="E")
		#Réglage du background
		self.download_button.config(bg='white')
			
		#Bouton Retour
		#Creation du bouton retour, relié la classe menu 
		self.retour = tkinter.Button(self, text="Retour", font = self.texte, command=lambda : [pygame.mixer.music.pause(),master.switch_frame(musique.Menu)])
		#Placement
		self.retour.grid(row=7,column=0, sticky="WS")
		#Réglage de la bordure du bouton et du background
		self.retour.config(bd=1, bg="white")
		
		#Initialisation des musiques lecteur 
		self.initLecteur()
		
		
	def playUnPause(self):
		if(self.comptePlay ==0):
			pygame.mixer.music.play()
			self.comptePlay +=1
		else:
			pygame.mixer.music.unpause()
		return 
		
	def supprimerFichiers(self):
		print("Code effectif à écrire")
	
	'''#Fonction d'enregistrement de fichier, pas grand chose à expliquer, le code se comprend tout seul
	def FNC_Selection(self, formatChoisi) :
		if(formatChoisi==".midi"):
			extension = [("fichier MIDI",".midi")]
			defaut = '".midi"'
		else:
			extension = [("fichier WAV",".wav")]
			defaut = '".wav"'
		file = tkinter.filedialog.asksaveasfile(filetypes = extension, title="Choisissez le nom de fichier", defaultextension = defaut)
	'''
	#Fonction de l'explorateur de fichier
	def BrowserFile(self):
		filename = filedialog.askdirectory(initialdir = "/")
		self.entry_text.set(filename)		
	
	def initLecteur(self):
		pygame.init()
		pygame.mixer.init()

		listeMusiques = []
		for (repertoire, sousRepertoires, fichiers) in walk("./files/midi/"):
			listeMusiques.extend(fichiers)
		
		listeMusiques = [i for i in listeMusiques if ".mid" in i]
		print(str(listeMusiques[0]))
		try:
			pygame.mixer.music.load("./files/midi/"+str(listeMusiques[0]))
			for musique in listeMusiques:
				if(musique == listeMusiques[0]):
					pass
				pygame.mixer.music.queue("./files/midi/"+str(musique))
		except pygame.error:
			print("Echec de chargement du fichier midi\n")






















