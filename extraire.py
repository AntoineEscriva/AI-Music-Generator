# -*- coding:utf-8 -*-

#code pour extraire les données d'un fichier MIDI CSV


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

        # Tempo information
        self.tempoList = []

        # Tracks information
        self.trackList = None
            

    def get_header(self, lines):
        header = lines[0].upper()
        if 'HEADER' not in header:
            print("No Header found\n")
            return None
        else:
            header = header.replace(' ', '').replace('\n', '')
            h = header.split(",") # on transforme la ligne en tableau
            self.format = int(h[3])
            self.nbTracks = int(h[4])
            self.division = int(h[5])
            self.trackList = [[] for k in range(self.nbTracks)]
            return lines[1:]

    def get_tracks(self, lines):
        for line in lines:
            if not ("START_TRACK" in line.upper() or "END_TRACK" in line.upper() or "TEXT" in line.upper()):
                #HERE save the time of End_track somewhere ?
                if "TIME_SIGNATURE" in line.upper():
                    self.get_time_signature(line)
                elif "SMPTE_OFFSET" in line.upper():
                    self.get_smpte_offset(line)
                elif "TEMPO" in line.upper():
                    self.tempoList.append(line)
                else:
                    h = line.split(",") # on transforme la ligne en tableau
                    no_track = int(h[0]) # string vers entier
                    self.trackList[no_track - 1].append(line)
            
            # filtrer tous les trucs du genre Start_track, title, copyright, text_t, SMPTE, Time_Sig.... etc dans un truc à part ?

    def get_time_signature(self, line):
        line = line.replace(' ', '').replace('\n', '').split(",")
        self.tsNum = int(line[3])
        self.tsDenom = int(line[4])
        self.tsClick = int(line[5])
        self.tsNotesQ = int(line[6])

    def get_smpte_offset(self, line):
        line = line.replace(' ', '').replace('\n', '').split(",")
        self.smpteHour = int(line[3])
        self.smpteMinute = int(line[4])
        self.smpteSecond = int(line[5])
        self.smpteFrame = int(line[6])
        self.smpteFracFrame = int(line[7])
            
    def get_info(self):
        file = open(self.filename, 'r')
        lines = file.readlines()
        rest = self.get_header(lines)
        if rest == None:
            print("No Header found, stopping\n")
        else:
            self.get_tracks(rest)
            None

    def get_track(self, numero):
        if numero > 0 and numero <= self.nbTracks:
            return self.trackList[numero-1]
        else:
            print("Incorrect track number\n")
            return None

    def print_info(self):
        print("FILE INFO :")
        print("filename =\t", self.filename)
        print("format =\t", self.format)
        print("nbTracks =\t", self.nbTracks)
        print("division =\t", self.division)
        print("\nSMPTE INFO :")
        print("smpteHour =\t", self.smpteHour)
        print("smpteMinute =\t", self.smpteMinute)
        print("smpteSecond =\t", self.smpteSecond)
        print("smpteFrame =\t", self.smpteFrame)
        print("smpteFracFrame =", self.smpteFracFrame)
        print("\nTIME SIGNATURE INFO :")
        print("tsNum =\t\t", self.tsNum)
        print("tsDenom =\t", self.tsDenom)
        print("tsClick =\t", self.tsClick)
        print("tsNotesQ =\t", self.tsNotesQ)
            
m1 = Morceau("elise.csv")
m1.get_info()
