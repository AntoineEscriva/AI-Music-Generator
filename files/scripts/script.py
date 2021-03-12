# !/usr/bin/python3
#coding: utf-8
import time
from files.scripts import RNN as RNN 
from files.scripts import importExportParam as iep 
from files.scripts import extraire as extraire
from os import walk

def main():
	print("Je suis un script")
	parametres = iep.importFromCSV()
	
	listeFichiers = []
	for (repertoire, sousRepertoires, fichiers) in walk(parametres["URL_Dossier"]):
		listeFichiers.extend(fichiers)
	print(listeFichiers)
	listeFichiers = [i for i in listeFichiers if ".mid" in i]
	
	listeMorceaux = [] # liste d'objets de type Morceau
	for files in listeFichiers:
		listeMorceaux.append(extraire.Morceau(parametres["URL_Dossier"]+'/'+files))

	print(listeMorceaux[0].filename)
	## A CHANGER ##
	text = listeMorceaux[0].preparer_track(2) #on récupère la piste 2 du premier morceau qu'on trouve
	
	out = RNN.rnn(text) #on envoie au RNN et on récupère la sortie

	listeMorceaux[0].format_to_csv(out[0], listeMorceaux[0].filename+"-généré.mid") # enregistre le morceau sous format MIDI

if __name__ == "__main__":
	main()

	
	
	
if __name__ == "__main__":
	main()
