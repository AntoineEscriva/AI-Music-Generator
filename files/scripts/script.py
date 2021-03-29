# !/usr/bin/python3
#coding: utf-8
import time
from files.scripts import RNN as RNN 
from files.scripts import importExportParam as iep 
from files.scripts import extraire as extraire
from os import walk, listdir,sep
import os


def main():
	parametres = iep.importFromCSV()

	os.makedirs(parametres["URL_Dossier"]+'/'+"CSV",exist_ok=True)
	os.makedirs(parametres["URL_Dossier"]+'/'+"Conversion",exist_ok=True)
	os.makedirs(parametres["URL_Dossier"]+'/'+"Resultat",exist_ok=True)
	
	#on récupère tous les fichiers .mid du dossier
	listeFichiers = [i for i in os.listdir(parametres["URL_Dossier"]) if ".mid" in i]
	print(listeFichiers)

	#on récupère tous les fichiers du dossier /Conversion pour ne pas avoir à reconvertir des fichiers
	listeFichiersConvert = [i for i in os.listdir(parametres["URL_Dossier"]+os.sep+'Conversion')]
	
	#on tranforme les fichiers midi en objet Morceau
	listeMorceaux = [] # liste d'objets de type Morceau
	for files in listeFichiers:
		listeMorceaux.append(extraire.Morceau(parametres["URL_Dossier"]+'/'+files))
	print(listeMorceaux[0].filename)
	
	
	## A CHANGER ##

	#on prépare les morceaux pour le RNN
	liste_textes = []
	for m in listeMorceaux:
		if(m.format == 1 and m.nbTracks > 1 ):
			if (parametres["TypeGeneration"] == "Rythme seulement"):
				liste_textes.append(m.preparer_track_rythme(2)) #on récupère la piste 2 du premier morceau qu'on trouve
			if (parametres["TypeGeneration"] == "Rythme et mélodie"):
				liste_textes.append(m.preparer_track(2)) #on récupère la piste 2 du premier morceau qu'on trouve
	
	#print(liste_textes)
	
	if (parametres["TypeGeneration"] == "Rythme seulement"):
		out = RNN.rnn_rythme(liste_textes[0]) #on envoie au RNN et on récupère la sortie
	elif (parametres["TypeGeneration"] == "Rythme et mélodie"):
		out = RNN.rnn_rythme_melodie(liste_textes[0])

	for index in range(len(out)):
		if (parametres["TypeGeneration"] == "Rythme seulement"):
			listeMorceaux[index].format_to_csv_rythme(out[index]) # enregistre le morceau sous format MIDI
		elif (parametres["TypeGeneration"] == "Rythme et mélodie"):
			listeMorceaux[index].format_to_csv(out[index]) # enregistre le morceau sous format MIDI


if __name__ == "__main__":
	main()
