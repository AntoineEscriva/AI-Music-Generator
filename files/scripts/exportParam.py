# !/usr/bin/python3
#coding: utf-8


def export(parametres):
	fichier = open("params.txt", "w")
	
	fichier.write(str(parametres))
	
	fichier.close()
	print("Fichier de paramètres exporté")
	return