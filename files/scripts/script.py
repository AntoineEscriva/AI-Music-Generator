# !/usr/bin/python3
#coding: utf-8

import time
from files.scripts import RNN, extraire, importExportParam as iep 
from os import walk

def main():
	parametres = iep.importFromCSV()
	
	#on recupere les fichiers du repertoire
	listeFichiers = []
	for (repertoire, sousRepertoires, fichiers) in walk(parametres["URL_Dossier"]):
		listeFichiers.extend(fichiers)
	print(listeFichiers)
	#On filtre les fichiers pour n'avoir que du .mid
	listeFichiers = [i for i in listeFichiers if ".mid" in i]
	
	print(listeFichiers)
	
	listeMorceaux = []
	for files in listeFichiers:
		listeMorceaux.append(extraire.Morceau(parametres["URL_Dossier"]+'/'+files))
	
	#RNN.rnn()
	
	
	
if __name__ == "__main__":
	main()