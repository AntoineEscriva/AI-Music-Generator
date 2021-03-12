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
	
	print(listeFichiers)
	
	listeMorceaux = []
	for files in listeFichiers:
		listeMorceaux.append(extraire.Morceau(parametres["URL_Dossier"]+'/'+files))
	
	#RNN.rnn()
	
	
	
if __name__ == "__main__":
	main()