# -*- coding:utf-8 -*-

#code pour extraire les notes depuis un fichier MIDI CSV et les mettre dans un format plus simple

'''
on a besoin des info sur les lignes de la forme 
Track, Time, Time_signature, Num, Denom, Click, NotesQ
Track, Time, Key_signature, Key, Major/Minor
Track, Time, Tempo, Number
le probleme est que chacune peuvent apparaitre plusieur fois, ça pose pb notament avec time_signature qui change la valeur de toutes les rythmes qu'on récupère
'''

'''
name = "elise.csv"
fichier = open(name, 'r')
lines = fichier.readlines()
fichier.close()
'''

class Morceau:
    def __init__(self, filename):
        self.filename = filename

        # Header information
        self.format = None
        self.nbTracks = None
        self.division = None

        # SMPTE_offset information
        self.smpteHour = None
        self.smpteMinute = None
        self.smpteSecond = None
        self.smpteFrame = None
        self.smpteFracFrame = None

        # Time signature information
        self.tsNum = None
        self.tsDenom = None
        self.tsClick = None
        self.tdNotesQ = None

        # Tempo information
        self.tempoList = None

        # Tracks information
        self.trackList = None
            

    def get_header(self, lines):
        if 'HEADER' in lines[0].upper():
            return lines[0].replace(' ', '').replace('\n', '')
        else:
            print("No Header found\n")
            return None


    def get_header_info(self, lines):
        header = self.get_header(lines)
        if(header == None):
            print("No Header found\n")
        else:
            h = header.split(",")
            self.format = int(h[3])
            self.nbTracks = int(h[4])
            self.division = int(h[5])
            self.trackList = [[] for k in range(self.nbTracks)]

            
    def get_info(self):
        file = open(self.filename, 'r')
        lines = file.readlines()
        self.get_header_info(lines)
        
