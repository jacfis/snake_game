#!/usr/bin/python3

import random  # Bibliotheken werden importiert
import tkinter
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.43.123', 123)) # IP Adresse: 192.168.43.123 Port: 123. Hier wird die Wlan Verbindung erstellt.


        

KOPF_SYMBOL = 'O' # Das Zeichen des Kopfes
ESSEN_SYMBOL = 'o' # Das Zeichen des Körpers




class Application:
    Name = 'Snake' 
    Groesse = 350, 400

    def __init__(self, haupt):
        self.haupt = haupt

        self.kopf = None
        self.kopf_position = None
        self.koerper = []
        self.koerper_positionen = []
        self.essen = None
        self.essen_position = None
        self.richtung = None
        self.bewegt = True

        self.bewegung = False
        self.init()

    def init(self):
        self.haupt.title(self.Name)

        self.canvas = tkinter.Canvas(self.haupt)
        self.canvas.grid(sticky=tkinter.NSEW) # Fläche mit den Richtungen "Norden", "Süden", "Osten", "Westen"

        self.start_knopf = tkinter.Button(self.haupt, text='Starte das Spiel', command=self.starte_spiel, font=('Arial Bold', 10), bg='royal blue', fg='white') # Einstellung des Buttons, der das Spiel startet und beendet. Hier wird die Schriftart, Größe, sowie die Farbe eingestellt
        self.start_knopf.grid(sticky=tkinter.EW) # Position des Startknopfs genau in der Mitte

        self.haupt.bind('oben', self.geh_hoch)      # Hier werden die Richtungen mit den Funktionen und den dazugehörigen Richtungen verbunden
        self.haupt.bind('links', self.geh_links)
        self.haupt.bind('unten', self.geh_runter)
        self.haupt.bind('rechts', self.geh_rechts)

        self.haupt.columnconfigure(0, weight=1) # Breite der Zeilen und Reihen
        self.haupt.rowconfigure(0, weight=1)
        self.haupt.resizable(width=False, height=False) # Größe kann nicht geändert werden
        self.haupt.geometry('%dx%d' % self.Groesse)

    def starte_spiel(self): # Funktion zum Start und Stop Knopf
        self.reset()
        if self.bewegung:
            self.bewegung = False # wenn die Schlange sich nicht bewegt soll Start stehen
            self.start_knopf.configure(text='Starte das Spiel')
        else:
            self.bewegung = True # wenn die Schlange sich bewegt soll Stop stehen
            self.start_knopf.configure(text='Beende das Spiel')
            self.start()

    def reset(self): # alles wird gelöscht, geleert, neu beginn
        self.koerper.clear()
        self.koerper_positionen.clear()
        self.canvas.delete(tkinter.ALL)

    def start(self): # Spiel wird gestartet, das Spielfeld wird aufgebaut, der Kopf bekommt eine zufällige Richtung und alle weiteren Funktionen werden angesprochen
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_rectangle(10, 10, width-10, height-10, fill='DarkSlateGray2') ##Farbe des Hintergrunds
        self.richtung = random.choice(['oben','rechts','links','unten'])
        kopf_position = [round(width // 2, -1), round(height // 2, -1)]
        self.kopf = self.canvas.create_text(tuple(kopf_position), text=KOPF_SYMBOL, fill='VioletRed3') # Farbe des Kopfes
        self.kopf_position = kopf_position
        self.auftauchendes_essen()
        self.fortbewegung()

    def auftauchendes_essen(self): # Das Essen wird initialisiert. Es wird darauf geachtet, dass das Essen nicht dort erscheint, wo der Kopf oder der Körper der Schlange sich gerade befindet.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        positionen = [tuple(self.kopf_position), self.essen_position] + self.koerper_positionen

        position = (round(random.randint(20, width-20), -1), round(random.randint(20, height-20), -1))
        while position in positionen:
            position = (round(random.randint(20, width-20), -1), round(random.randint(20, height-20), -1))

        symbol = ESSEN_SYMBOL
        self.essen = self.canvas.create_text(position, text=symbol, fill='DarkOrange2') # Farbe des Körpers
        self.essen_position = position
        self.essen_symbol = symbol

    def fortbewegung(self): # Die Funktion gibt an, dass der Körper dem Kopf der Schlange folgen soll und dass das Essen als neuer Körper der Schlange hinzugefügt wird.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        vorherige_kopf_position = tuple(self.kopf_position)

        richtung = s.recv(1024) #auskommentiert, da sonst keine GUI aufgeht
        if self.richtung == 'oben':
            self.kopf_position[1] -= 10 
        elif self.richtung == 'links':
            self.kopf_position[0] -= 10
        elif self.richtung == 'unten':
            self.kopf_position[1] += 10
        elif self.richtung == 'rechts':
            self.kopf_position[0] += 10

        kopf_position = tuple(self.kopf_position)
        if (self.kopf_position[0] < 10 or self.kopf_position[0] >= width-10 or
            self.kopf_position[1] < 10 or self.kopf_position[1] >= height-10 or
            any(koerper_position == kopf_position for koerper_position in self.koerper_positionen)):
            self.spiel_vorbei()
            return

        if kopf_position == self.essen_position:
            self.canvas.coords(self.essen, vorherige_kopf_position)
            self.koerper.append(self.essen)
            self.koerper_positionen.append(vorherige_kopf_position)
            self.auftauchendes_essen()

        if self.koerper:
            vorherige_position = vorherige_kopf_position
            for index, (koerper, position) in enumerate(zip(self.koerper, self.koerper_positionen)):
                self.canvas.coords(koerper, vorherige_position)
                self.koerper_positionen[index] = vorherige_position
                vorherige_position = position

        self.canvas.coords(self.kopf, kopf_position)
        
        self.bewegt = True

        if self.bewegung:
            self.canvas.after(800, self.fortbewegung) # Geschwindigkeit der Schlangenbewegung

    def spiel_vorbei(self): # Aussehen des Bildschirms, wenn das Spiel verloren ist.
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.bewegung = False
        self.start_knopf.configure(text='Starte das Spiel')
        punktzahl = len(self.koerper) * 10 # Punktzahl wird ermittelt durch die Körperlänge/die gegessenen 'o's.
        self.canvas.create_text((round(width // 2, -1), round(height // 2, -1)), text='Spiel vorbei! Du hast diese Punktzahl erreicht: %d' % punktzahl, fill='white') #Farbe des Schriftzugs wenn das Spiel vorbei ist

        
    def geh_hoch(self, event):   # Funktion zum nach oben gehen
        self.richtung = 'oben'

    def geh_links(self, event):  # Funktion zum nach links gehen
        self.richtung = 'links'
            
    def geh_runter(self, event): # Funktion zum nach unten gehen
        self.richtung = 'unten'
           
    def geh_rechts(self, event): # Funktion zum nach rechts gehen
        self.richtung = 'rechts'
          
  


def main():
    root = tkinter.Tk()
    Application(root)
    root.mainloop()


if __name__ == '__main__':
    main()

    
