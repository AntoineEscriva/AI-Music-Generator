# !/usr/bin/python3
#coding: utf-8


def import(filename="params.txt"):
	fichier = open(filename, "r")
	
	parametre = fichier.read()
	
	fichier.close()
	print("Fichier de paramètres importé")
	return parametre
