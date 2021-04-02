# !/usr/bin/python3
#coding: utf-8

import time
from files.scripts import RNN, extraire, importExportParam as iep 
import os

def lire_fichier(nom):
	file = open(nom, 'r')
	lines = file.readlines()
	file.close()
	return "".join(lines) #on retourne la concaténation des lignes du fichier

def ecrire_fichier(nom, donnees):
	with open(nom, 'w') as file :
		for a in donnees:
		    file.write(a)


def main():
	parametres = iep.importFromCSV()

	os.makedirs(parametres["URL_Dossier"]+os.sep+"CSV",exist_ok=True)
	os.makedirs(parametres["URL_Dossier"]+os.sep+"Conversion_rythme",exist_ok=True)
	os.makedirs(parametres["URL_Dossier"]+os.sep+"Conversion_melodie",exist_ok=True)
	os.makedirs(parametres["URL_Dossier"]+os.sep+"Resultat",exist_ok=True)
	
	#on récupère tous les noms des fichiers .mid du dossier
	listeFichiers = [i for i in os.listdir(parametres["URL_Dossier"]) if ".mid" in i]	
	
	if (parametres["TypeGeneration"] == "Rythme seulement"):
		#on récupère tous les noms des fichiers du dossier /Conversion_rythme pour ne pas avoir à reconvertir des fichiers
		listeFichiersConvertis = [i for i in os.listdir(parametres["URL_Dossier"]+os.sep+"Conversion_rythme")]
	

	if (parametres["TypeGeneration"] == "Rythme et mélodie"):
		#on récupère tous les noms des fichiers du dossier /Conversion_melodie pour ne pas avoir à reconvertir des fichiers
		listeFichiersConvertis = [i for i in os.listdir(parametres["URL_Dossier"]+os.sep+"Conversion_melodie")]


	listeFichiersAConvertir = [listeFichiers[0]] #totalement artificiel, pour avoir au moins 1 objet morceau pour plus tard
	for nom_mid in listeFichiers:
		nom = nom_mid.replace(".mid",".format") #en admettant que notre extension sera ".format"
		if nom not in listeFichiersConvertis:
			listeFichiersAConvertir.append(nom_mid)


	#on tranforme les fichiers midi non convertis en objets Morceau
	listeMorceaux = [] # liste d'objets de type Morceau
	for files in listeFichiersAConvertir:
		listeMorceaux.append(extraire.Morceau(parametres["URL_Dossier"]+os.sep+files))
		print(files, " a besoin d'etre converti !")
	
	
	## A CHANGER ##

	#on prépare les morceaux pour le RNN
	liste_textes = []
	for m in listeMorceaux:
		if(m.format == 1 and m.nbTracks > 1 ):
			if (parametres["TypeGeneration"] == "Rythme seulement"):
				nom = parametres["URL_Dossier"]+os.sep+"Conversion_rythme"+os.sep+m.filename+".format"
				content = m.preparer_track_rythme(2)
				ecrire_fichier(nom, [content]) #on récupère la piste 2 du morceau
				liste_textes.append(content)
			if (parametres["TypeGeneration"] == "Rythme et mélodie"):
				nom = parametres["URL_Dossier"]+os.sep+"Conversion_melodie"+os.sep+m.filename+".format"
				content = m.preparer_track(2)
				ecrire_fichier(nom, [content]) #on récupère la piste 2 du morceau
				liste_textes.append(content)


	for m in listeFichiersConvertis:
		if (parametres["TypeGeneration"] == "Rythme seulement"):
			content = lire_fichier(parametres["URL_Dossier"]+os.sep+"Conversion_rythme"+os.sep+m)
			liste_textes.append(content) #recuperation des donnees

		if (parametres["TypeGeneration"] == "Rythme et mélodie"):
			content = lire_fichier(parametres["URL_Dossier"]+os.sep+"Conversion_melodie"+os.sep+m)
			liste_textes.append(content) #recuperation des donnees

	
	# en fonction des paramètres de génération, on appelle différents RNN
	if (parametres["TypeGeneration"] == "Rythme seulement"):
		out = RNN.rnn_rythme(liste_textes) #on envoie au RNN et on récupère la sortie
	elif (parametres["TypeGeneration"] == "Rythme et mélodie"):
		out = RNN.rnn_rythme_melodie(liste_textes)

	temp = int(time.time())

	for index in range(len(out)):
		if (parametres["TypeGeneration"] == "Rythme seulement"):
			listeMorceaux[0].format_to_csv_rythme(out[index], str(temp)+" "+str(index)) # enregistre le morceau sous format MIDI
		elif (parametres["TypeGeneration"] == "Rythme et mélodie"):
			listeMorceaux[0].format_to_csv(out[index], str(temp)+" "+str(index)) # enregistre le morceau sous format MIDI


if __name__ == "__main__":
	main()
