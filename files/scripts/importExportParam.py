# !/usr/bin/python3
#coding: utf-8

import csv

def export(parametres):
	fichier = open("params.txt", "w")
	
	fichier.write(str(parametres))
	
	fichier.close()
	print("Fichier de paramètres exporté")
	return
	
	
def exportInCSV(parametres):
	with open('params.csv', 'w') as fichier :
		w = csv.DictWriter(fichier, parametres.keys())
		w.writeheader()
		w.writerow(parametres)
	return
	
def importFromCSV():
	with open('params.csv', newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		parametres = {}
		for row in reader:
			parametres['URL_Dossier'] = row['URL_Dossier']
			parametres['NombreMorceaux'] = row['NombreMorceaux']
			parametres['DureeMorceaux']= row['DureeMorceaux']
			parametres['TonaliteMorceaux']= row['TonaliteMorceaux']
			parametres['VitesseMorceaux']= row['VitesseMorceaux']
			parametres['TypeGeneration'] = row['TypeGeneration']
	return parametres
