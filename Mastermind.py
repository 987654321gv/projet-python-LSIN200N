
"""

"""
from tkinter import *
import random
from math import sqrt, ceil
from collections import Counter


class Mastermind(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.pack()
        #### valeurs arbitraires ####
        self.couleurs = ['#ffffff', '#000000', '#ff0000', '#00ff00', '#0000ff', '#ffff00','#00aaee','#ffaaee']
        self.couleur_vide = '#553823'
        self.nb_emplacements = 4
        self.dico_reponce = {0: '#ffffff', 1: '#000000'}
        self.version_alt = False
        self.chaos_degree=2
        self.essais_max=10
        #### initialisations ####
        self.canvases = [] 
        self.row_offset = 5 
        self.emplacements = []
        self.emplacement_actif = 0
        self.essais = -1
        self.prec_essai = []
        self.emplacements_prec_essai = []
        self.master.title('codage')
        #### valeurs précalculées ####
        self.nb_couleurs = len(self.couleurs)
        self.nb_max = max(self.nb_emplacements, self.nb_couleurs - 1)
        self.endroit_emplacement = max((self.nb_couleurs - self.nb_emplacements) // 2, 1)
        self.endroit_couleurs = max((self.nb_emplacements - self.nb_couleurs) // 2, 0)
        if self.nb_couleurs <= self.nb_emplacements: self.endroit_couleurs += 1
        self.fin_couleurs = self.endroit_couleurs + self.nb_couleurs - 1
        self.side = ceil(sqrt(self.nb_emplacements))
        self.coins = (10, 55)
        if self.side > 2:
            self.coins = tuple(10 + (((55 - self.side * 5) * i) // (self.side - 1)) for i in range(self.side))
        #### intialisation GUI ####
        for i in range(self.nb_emplacements):
            self.emplacements_prec_essai.append(Frame(self, height=75, width=75))
            self.emplacements_prec_essai[-1].grid(row=1, column=self.endroit_emplacement + i, sticky=NSEW)
            self.emplacements.append(Frame(self, height=75, width=75, bg=self.couleur_vide))
            self.emplacements[-1].grid(row=0, column=self.endroit_emplacement + i, sticky=EW)
        for i, c in enumerate(self.couleurs):
            Button(self, background=c, width=10, height=2, command=lambda couleur=i: self.jouer(couleur)) \
                .grid(row=self.row_offset + self.essais_max + 1, column=i + self.endroit_couleurs, sticky=EW)
        Button(self, text='annuler', command=self.annuler).grid(row=self.row_offset + self.essais_max + 2, column=self.nb_max // 2,
                                                                columnspan=1 if self.nb_couleurs % 2 else 2)
        Button(self, text='rejouer', command=self.rejouer).grid(row=self.row_offset + self.essais_max + 2, column=self.endroit_couleurs)
        Button(self, text='quiter', command=self.quit).grid(row=self.row_offset + self.essais_max + 2, column=self.fin_couleurs)
        self.ale = Button(self, text='code aléatoire', command=self.rand)
        self.ale.grid(row=self.row_offset + self.essais_max + 3, column=self.nb_max // 2, columnspan=1 if self.nb_couleurs % 2 else 2)

    def jouer(self, couleur):
        self.emplacements[self.emplacement_actif].configure(bg=self.couleurs[couleur])
        self.emplacement_actif += 1
        self.prec_essai.append(couleur)
        if self.emplacement_actif != self.nb_emplacements: return
        self.emplacement_actif = 0
        self.essais += 1
        if self.essais:
            row = self.row_offset + self.essais
            for i, couleur in enumerate(self.prec_essai):
                case = Frame(self,
                            height=75,
                            width=75,
                            bg=self.couleurs[couleur])
                case.grid(row=row,
                        column=self.endroit_emplacement + i,
                        sticky=NSEW)
            if self.reponse == self.prec_essai:
                Label(Tk(), text=f'gagné en {self.essais} essais').pack()
            if self.essais>=self.essais_max:
                Label(Tk(), text='perdu !').pack()
                for e,r in zip(self.emplacements,self.reponse):
                    e.configure(bg=self.couleurs[r])
                return
            rep = []
            if not self.version_alt:
                rep=[0]*sum((Counter(self.prec_essai)&self.count_reponse).values())
            for i, e in enumerate(self.prec_essai):
                if self.reponse[i] == e:
                    rep.append(1)
                    if not self.version_alt:
                        rep.remove(0)
                elif e in self.reponse and self.version_alt:
                    rep.append(0)
            if self.chaos_degree==2:
                rep.extend([None] * ((self.side ** 2) - len(rep)))
            
            can = Canvas(self, height=75, bg='#aaaaaa', width=75)
            can.grid(row=self.row_offset + self.essais,
                     column=self.endroit_emplacement - 1,
                     sticky=EW)
            self.canvases.append(can)

            if self.chaos_degree!=0:
                random.shuffle(rep)
            elif self.version_alt:
                rep.sort()
            print(self.prec_essai,rep)
            for i, p in enumerate(rep):
                if p is not None:
                    can.create_oval(self.coins[i % self.side], self.coins[i // self.side],
                                         self.coins[i % self.side] + self.side * 5,
                                         self.coins[i // self.side] + self.side * 5,
                                         fill=self.dico_reponce[p])
        else:
            self.enregister_reponce(self.prec_essai)
        self.wipe_prec_essai()

    def annuler(self):
        if self.emplacement_actif == 0: return
        self.emplacement_actif -= 1
        self.emplacements[self.emplacement_actif].configure(bg=self.couleur_vide)
        self.prec_essai.pop()

    def rejouer(self):
        if self.essais == -1: return
        self.emplacement_actif = 0
        self.essais = -1
        self.prec_essai = []
        self.master.title('codage')
        for can in self.canvases:
            can.destroy()
        self.canvases = []
        self.ale = Button(self, text='code aléatoire', command=self.rand)
        self.ale.grid(row=self.row_offset + self.essais_max + 3, column=0, columnspan=self.nb_couleurs)
        for ep, e in zip(self.emplacements_prec_essai, self.emplacements):
            ep.configure(bg='#eeeeee')
            e.configure(bg=self.couleur_vide)

    def rand(self):
        self.enregister_reponce([random.randint(0, self.nb_couleurs - 1) for _ in range(len(self.emplacements))])
        self.wipe_prec_essai()
        self.essais = 0
        self.emplacement_actif = 0

    def enregister_reponce(self, reponse):
        self.master.title('jeu')
        self.reponse = reponse
        self.count_reponse = Counter(reponse)
        self.can = Canvas(self, height=75, bg='#aaaaaa', width=75)
        self.can.grid(row=1, column=self.endroit_emplacement - 1, sticky=EW)
        self.ale.destroy()

    def wipe_prec_essai(self):
        for e in self.emplacements:
            e.configure(bg=self.couleur_vide)
        self.prec_essai = []


if __name__ == '__main__':
    f = Tk()
    f.resizable(width=0, height=0)
    Mastermind(f)
    f.mainloop()
