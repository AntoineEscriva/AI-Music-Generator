# -*- coding:utf-8 -*-

#code pour extraire les données d'un morceau de musique depuis un fichier MIDI CSV et les mettre dans un objet


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
        self.tsNotesQ = None

        # Key signature information
        self.ksKey = None
        self.ksMinMaj = None

        # Tempo information
        self.tempoList = []

        # Tracks information
        self.trackList = []

        #m1.get_info()
        # décommenter pour un parsing automatique

    def __str__(self):
        return "\nFILE INFO :\nfilename =\t{0}\nformat =\t{1}\nnbTracks =\t{2}\ndivision =\t{3}\n\nSMPTE INFO :\nsmpteHour =\t{4}\nsmpteMinute =\t{5}\nsmpteSecond =\t{6}\nsmpteFrame =\t{7}\nsmpteFracFrame = {8}\n\nTIME SIGNATURE INFO :\ntsNum =\t\t{9}\ntsDenom =\t{10}\ntsClick =\t{11}\ntsNotesQ =\t{12}\nself.ksKey =\t{13}\nself.ksMinMaj =\t{14}".format(self.filename,
                self.format,
                self.nbTracks,
                self.division,
                self.smpteHour,
                self.smpteMinute,
                self.smpteSecond,
                self.smpteFrame,
                self.smpteFracFrame,
                self.tsNum,
                self.tsDenom,
                self.tsClick,
                self.tsNotesQ,
                self.ksKey,
                self.ksMinMaj)

    def get_info(self):
        file = open(self.filename, 'r')
        lines = file.readlines()
        file.close()
        rest = self.get_header(lines)
        if rest == None:
            print("No Header found, stopping\n")
        else:
            self.get_tracks(rest)

    def get_header(self, lines):
        header = lines[0].upper()
        if 'HEADER' not in header:
            print("No Header found\n")
            return None
        else:
            h = header.split(",") # on transforme la ligne en tableau
            self.format = int(h[3])
            self.nbTracks = int(h[4])
            self.division = int(h[5])
            self.trackList = [[] for k in range(self.nbTracks)]
            return lines[1:]

    def get_tracks(self, lines):
        for line in lines:
            if "TIME_SIGNATURE" in line.upper():
                self.get_time_signature(line)
            elif "KEY_SIGNATURE" in line.upper():
                self.get_key_signature(line)
            elif "SMPTE_OFFSET" in line.upper():
                self.get_smpte_offset(line)
            elif "TEMPO" in line.upper():
                self.tempoList.append(line)
            elif "NOTE_" in line.upper() :
                h = line.split(",") # on transforme la ligne en tableau
                no_track = int(h[0]) # string vers entier
                self.trackList[no_track - 1].append(line)
            
            # filtrer tous les trucs du genre Start_track, title, copyright, text_t, SMPTE, Time_Sig.... etc dans un truc à part ?

    def get_time_signature(self, line):
        line = line.split(",")
        self.tsNum = int(line[3])
        self.tsDenom = int(line[4])
        self.tsClick = int(line[5])
        self.tsNotesQ = int(line[6])

    def get_key_signature(self, line):
        line = line.split(",")
        self.ksKey = int(line[3])
        self.ksMinMaj = line[4]
        
    def get_smpte_offset(self, line):
        line = line.split(",")
        self.smpteHour = int(line[3])
        self.smpteMinute = int(line[4])
        self.smpteSecond = int(line[5])
        self.smpteFrame = int(line[6])
        self.smpteFracFrame = int(line[7])
        

    def get_track(self, numero):
        if numero > 0 and numero <= self.nbTracks:
            return self.trackList[numero-1]
        else:
            print("Incorrect track number\n")
            return None


    def preparer_track(self, numero):
        L = self.get_track(numero)  # on récupère la piste
        prepared = [] #liste de retour
        
        while L != []:
            line1 = L[0].split(",") # transformation en liste
            time1 = int(line1[1]) # récupérer le Time
            note = int(line1[4]) # récupérer la Note
            
            b = 0
            line2 = [-1,-1,-1,-1,-1]
            while int(line2[4]) != note : # on cherche la note qui termine
                b += 1
                line2 = L[b].split(",")

            time2 = int(line2[1]) # récupération deuxième temps
            prepared.append([time1, time2-time1, note]) # ajout des données
            L = L[1:b]+L[b+1:] # on enleve les deux lignes
        return prepared
