#coding: utf-8

import tkinter
import tkinter.font as tkFont
from tkinter import filedialog 
from tkinter import ttk
from tkinter import *
from files import lecteur as lecteur 
from files.scripts import script as script 
from files.scripts import importExportParam
from os import walk
import time
import os
if(os.name != "posix"):
	from ctypes import windll

largeurBout = 15
hauteurBout = 2
margeX = 0
margeY = 0

#######################################################
#Classe mère de l'interface
#######################################################

class Musique(tkinter.Tk):
	def __init__(self):
		#Initialisation d'une fenetre TKinter
		tkinter.Tk.__init__(self)
		#Cette ligne là je sais plus à quoi elle sert
		self.frame = None
		#Affectation du titre de la fenêtre
		self.title("Génération musique aléatoire")
		#Réglage de la taille de la fenêtre
		self.geometry("535x420")
		#Réglage du fond en blanc
		self.configure(bg='white')
		#Appel de la methode switch_frame qui se situe ci-dessous
		self.switch_frame(Menu)
		
		
	#Cette méthode permet de supprimer le cadre actuel dans la fenetre principale par frame_class
	def switch_frame(self, frame_class):
		#On instancie un nouveau cadre
		newFrame = frame_class(self)
		#Si il y a déjà un cadre on le supprime
		if(self.frame is not None):
			self.frame.grid_remove()
		#Affectation du cadre à la fenetre
		self.frame = newFrame
		#Réglage des marges
		self.frame.grid(padx = 20, pady = 15, sticky = "ewsn")
		
#######################################################
#Classe du menu de l'interface
#######################################################

class Menu(tkinter.Frame):
		
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		
		#Réglage police du titre et du texte
		self.titre = tkFont.Font(family='Helvetica', size=20)
		self.texte = tkFont.Font(family='Helvetica', size=13)
		#Réglage police combobox
		master.option_add("*Font", "Helvetica 13")
		#Réglage arrière plan
		self.configure(bg='white')
		
		#---------Label------------#
		#Création et placement du titre du cadre
		self.titre = tkinter.Label(self, text="Configuration", bg='white', font = self.titre).grid(row=0,column=0)

		#Création de la Zone d'affichage du chemin
		self.entry_text = tkinter.StringVar()
		self.entry_text.set(os.getcwd()+"/files/midi")
		
		#Traitement affichage chemin
		self.affichageChemin = tkinter.StringVar()
		self.affichageChemin.set(self.traitementAffichage(self.entry_text.get(),29))
		
		#Placement de la zone et affectation d'un texte dans cette zone d'affichage
		self.usr_input = tkinter.Entry(self, state='readonly', text=self.affichageChemin, width =25)
		self.usr_input .grid(row=1,column=1, sticky="EW")
		
		#Création et placement du Bouton ouvrir dossier
		self.UF = tkinter.Button(self, text="Sélection Dossier", bg = "white", font = self.texte,bd=1,command = lambda:[self.Browser()])
		self.UF.grid(row = 1, column = 0, sticky="W")
		
		#Création et placement du label Nombre de morceaux
		tkinter.Label(self, text="Nombre de morceaux",height = hauteurBout, font = self.texte, bg='white').grid(row = 2, column =0, sticky="W")
		#Création et placement d'une spinbox pour choisir le nombre de morceaux
		self.nbMorceaux = tkinter.Spinbox(self, from_=1, to=20, width=10)
		self.nbMorceaux.grid(row = 2, column =1, sticky="W")
		tkinter.Label(self, text="Entre 1-20   ", bg="white").grid(row=2, column=1, sticky="e")
		
		#Création et placement du label Durée de morceaux
		tkinter.Label(self, text="Durée de morceaux",height = hauteurBout,  font = self.texte, bg='white').grid(row = 3, column =0, sticky="W")
		
		#Tonalité de morceaux
		tkinter.Label(self, text="Tonalité de morceaux",height = hauteurBout,  font = self.texte, bg='white').grid(row = 4, column =0, sticky="W")
		#Bouton Tonalite du morceau
		self.tonaliteMorceau = tkinter.Spinbox(self, values = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"), width=10)
		self.tonaliteMorceau.grid(row = 4, column =1, sticky="W")
		
		#bpm des morceaux
		tkinter.Label(self, text="Vitesse des morceaux",height = hauteurBout,  font = self.texte, bg='white').grid(row = 5, column =0, sticky="W")
		#Bouton bpm des morceau
		self.bpmMorceau = tkinter.Spinbox(self, from_=30,to=240, width=10)
		self.bpmMorceau.grid(row = 5, column =1, sticky="W")
		tkinter.Label(self, text="Entre 30-240", bg="white").grid(row=5, column=1, sticky="e")
		
		#Choix de génération
		tkinter.Label(self, text="Type de génération", width = 15, height = hauteurBout, font = self.texte, bg='white').grid(row = 6, column =0, sticky="W")
				
		#Création du spinbox de durée du morceau
		self.dureeMorceau = tkinter.Spinbox(self, from_=60,to=340, width=10)
		#Placement de la spinbox
		self.dureeMorceau.grid(row = 3, column =1, sticky="W")
		tkinter.Label(self, text="Entre 60-340", bg="white").grid(row=3, column=1, sticky="e")
		
		#Création et placement du Bouton valider
		self.textBoutonValider = StringVar()
		self.textBoutonValider.set("Valider")
		self.Valider = tkinter.Button(self, textvariable=self.textBoutonValider, bg="white", font = self.texte, bd=1, command=lambda :[self.charging(master)])
		self.Valider.grid(row=7,column = 1,sticky="EW")
		
		
		#Création de la combobox de Choix de generation	
		self.comboboite = ttk.Combobox(self, values = ["Rythme seulement","Rythme et mélodie","Polyphonie"],state="readonly")
		#Réglage de l'item actuel sur 0
		self.comboboite.current(0)
		#Placement
		self.comboboite.grid(row=6, column=1, sticky="W")
		
	def traitementAffichage(self, chemin, taille):
		if len(chemin) > taille:
			cheminCoupe = chemin[-(len(chemin)-taille):]
			return cheminCoupe
		else:
			return chemin
	
	def valide(self):
		valide = True
		if(int(self.nbMorceaux.get())>20 or int(self.nbMorceaux.get())<1):
			valide = False
			#self.valide.set(1)
		if(int(self.dureeMorceau.get())<60 or int(self.dureeMorceau.get())>340) :
			valide = False
			#self.dureeMorceau.set(60),
		if(int(self.bpmMorceau.get()) <30 or int(self.bpmMorceau.get())>240) :
			valide=False
			#self.bpmMorceau.set(30)
		if(not valide):
			self.popupmsg()
		return valide

	def popupmsg(self):
		popup = tkinter.Tk()
		centrefenetre(popup)
		popup.title("Erreur")
		popup.config(bg="white")
		label = tkinter.Label(popup, text="Attention : Le nombre de moreaux, ou \nla durée, ou les bpm est incorrect", bg="white")
		popup.geometry("315x120")
		label.pack(side="top", fill="x", pady=10)
		ok = tkinter.Button(popup, text="Ok", bg="white", command = popup.destroy, width=10)
		ok.pack()
		popup.mainloop()

	def charging(self, master):
		if(self.valide()):
			self.textBoutonValider.set("En chargement...")
			self.export()
			script.main()
			master.switch_frame(lecteur.Lecteur)
		return
		

	def export(self):
	
		self.parametres = 	{"URL_Dossier": self.entry_text.get(),
						"NombreMorceaux": self.nbMorceaux.get(),
						"DureeMorceaux": self.dureeMorceau.get(),
					 	"TonaliteMorceaux": self.tonaliteMorceau.get(),
					 	"VitesseMorceaux": self.bpmMorceau.get(),
						"TypeGeneration":self.comboboite.get()}
		importExportParam.exportInCSV(self.parametres)
		return
	
		
	#Méthode pour l'explorateur de fichier
	def Browser(self):
		filename = filedialog.askdirectory(initialdir = "./project2020-2021/files/midi/")
		print("Filename is "+filename)
		self.affichageChemin.set(self.traitementAffichage(filename,20))
		self.entry_text.set(filename)
			
####################################################### 
####################################################### 

##Ci-dessous, deux fonctions copiées collées de Google pour centrer la fenêtre au milieu de l'écran
#Récupère les infos relatives à l'écran
def geoliste(g):
	r=[i for i in range(0,len(g)) if not g[i].isdigit()]
	return [int(g[0:r[0]]),int(g[r[0]+1:r[1]]),int(g[r[1]+1:r[2]]),int(g[r[2]+1:])]

#Centre la fenetre au milieu de l'écran
def centrefenetre(fen):
	fen.update_idletasks()
	l,h,x,y=geoliste(fen.geometry())
	fen.geometry("%dx%d%+d%+d" % (l,h,(fen.winfo_screenwidth()-l)//2,(fen.winfo_screenheight()-h)//2))

##############################################################################################################
##############################################################################################################  

def start():
	#instancie la classe Musique
	app = Musique()
	#Centrage du futur affichage
	centrefenetre(app)
	#Empecher le redimensionnement
	app.resizable(width=False, height=False)
	
	#Pour la netteté de la police de caractères sur Windows
	if(os.name != "posix"):
		windll.shcore.SetProcessDpiAwareness(1)

	#Boucle principale de l'interface
	app.mainloop()
	




