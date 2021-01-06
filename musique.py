#coding: utf-8

import tkinter
import tkinter.font as tkFont
from tkinter import filedialog 
from tkinter import ttk
from tkinter import *
from ctypes import windll

import lecteur as lecteur 

largeurBout = 15
hauteurBout = 2
margeX = 0
margeY = 0

#######################################################

class Musique(tkinter.Tk):
	def __init__(self):
		tkinter.Tk.__init__(self)
		self.frame = None
		self.title("Génération musique aléatoire")
		self.geometry("420x270")
		self.switch_frame(Menu)
		self.configure(bg='white')
		#self.font = tkinter.font.Font(size=55)

	def switch_frame(self, frame_class):
		newFrame = frame_class(self)
		if(self.frame is not None):
			self.frame.grid_remove()
		self.frame = newFrame
		self.frame.grid(padx = 20, pady = 15, sticky = "ewsn")
		
#######################################################

class Menu(tkinter.Frame):
		
	def __init__(self, master):
		tkinter.Frame.__init__(self, master)
		self.UneFont = "Helvetica, 10"

		#---------Label------------#
		self.configure(bg='white')
		#titre
		self.titre = tkinter.Label(self, text="Configuration", bg='white', font ="Helvetica").grid(row=0,column=0)

		#Label sélectionner un dossier
		tkinter.Label(self, text="Sélectionner un dossier",height = hauteurBout, bg="white").grid(row = 1, column = 0, sticky="W")
		
		#Zone pour l'affichage du chemin
		self.entry_text = tkinter.StringVar()
		self.usr_input = ttk.Entry(self, state='readonly', textvariable=self.entry_text)
		self.usr_input.grid(row=1,column=1, sticky='EW')
		
		#Bouton ouvrir dossier
		self.UF = tkinter.Button(self, text="Choisir", bg = "white", bd=1, width = largeurBout-5,command = lambda:[self.Browser()])
		self.UF.grid(row = 1, column = 2, sticky="E")
		
		#Nombre de morceaux
		tkinter.Label(self, text="Nombre de morceaux",height = hauteurBout, bg='white').grid(row = 2, column =0, sticky="W")
		self.nbMorceaux = tkinter.Spinbox(self, from_=1, to=20).grid(row = 2, column =1, sticky="EW")

		# Durée de morceaux
		tkinter.Label(self, text="Durée de morceaux",height = hauteurBout, bg='white').grid(row = 3, column =0, sticky="W")
		
		#Choix de génération
		tkinter.Label(self, text="Choix de génération", width = 15, height = hauteurBout, bg='white').grid(row = 4, column =0, sticky="W")
				
		#Bouton nb morceau
		self.dureeMorceau = tkinter.Spinbox(self, from_=60,to=340)
		self.dureeMorceau.grid(row = 3, column =1, sticky="EW")
		
		#Bouton valider
		self.Valider = tkinter.Button(self, text="Valider", bg="white", bd=1, command=lambda :[master.switch_frame(lecteur.Lecteur)])
		self.Valider.grid(row=5,column = 1,sticky="EW")
		
		#Bouton Choix generation	
		self.comboboite = ttk.Combobox(self,values = ["Rythme seulement","Rythme et mélodie","Polyphonie"])
		self.comboboite.current(0)
		self.comboboite.grid(row=4, column=1)
		

	def Browser(self):
		filename = filedialog.askdirectory(initialdir = "/")
		self.entry_text.set(filename)
			
####################################################### 

##Ci-dessous, deux fonctions copiées collées de Google pour centrer la fenêtre au milieu de l'écran

def geoliste(g):
    r=[i for i in range(0,len(g)) if not g[i].isdigit()]
    return [int(g[0:r[0]]),int(g[r[0]+1:r[1]]),int(g[r[1]+1:r[2]]),int(g[r[2]+1:])]

def centrefenetre(fen):
    fen.update_idletasks()
    l,h,x,y=geoliste(fen.geometry())
    fen.geometry("%dx%d%+d%+d" % (l,h,(fen.winfo_screenwidth()-l)//2,(fen.winfo_screenheight()-h)//2))
 
# exemple d'utilisation:

if __name__ == "__main__":

	app = Musique()
	centrefenetre(app)
	app.resizable(width=False, height=False)
#	windll.shcore.SetProcessDpiAwareness(1)

	app.mainloop()
	




