# !/usr/bin/python3
#coding: utf-8


def export(parametres, filename="params.csv"):
	'''
	fichier = open(filename, "w")
	
	fichier.write(str(parametres))
	
	fichier.close()
	'''
	
	with open(filename, 'w') as f:
		w = csv.DictWriter(f, parametres.keys())
		w.writeheader()
		w.writerow(parametres)
	print("Fichier de paramètres exporté")
	return
