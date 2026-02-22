"""

"""
from tkinter import *
import random
class mastermind(Frame):
    def __init__(self,boss=None):
        Frame.__init__(self,boss)
        self.pack()
        self.couleurs=['#ffffff','#000000','#ff0000','#00ff00','#0000ff','#ffff00']#,'#00aaee','#ffaaee']
        self.couleur_vide='#553823'
        self.nb_emplacements=4
        self.emplacements=[]
        self.emplacement_actif=0
        self.essais = -1
        self.prec_essai = []
        self.dico_reponce = {0:'#ffffff',1: '#000000'}
        self.emplacements_prec_essai=[]
        self.master.title('codage')

        self.nb_couleurs=len(self.couleurs)
        self.nb_max=max(self.nb_emplacements,self.nb_couleurs-1)
        self.endroit_emplacement=abs(self.nb_couleurs - self.nb_emplacements) // 2

        for i in range(self.nb_emplacements):
            self.emplacements_prec_essai.append(Frame(self, height=75,width=75))
            self.emplacements_prec_essai[-1].grid(row=1, column=self.endroit_emplacement + i, sticky=NSEW)
            self.emplacements.append(Frame(self, height=75,width=75, bg=self.couleur_vide))
            self.emplacements[-1].grid(row=0, column=self.endroit_emplacement + i, sticky=EW)

        for i,c in enumerate(self.couleurs):
            Button(self, background=c,width=10,height=2,command=lambda couleur=i:self.jouer(couleur)).grid(row=2, column=i, sticky=EW)

        Button(self,text='annuler', command=self.annuler).grid(row=3, column=self.nb_max//2,columnspan=1 if self.nb_max%2 else 2)
        Button(self, text='rejouer', command=self.rejouer).grid(row=3, column=0)
        Button(self, text='quiter', command=self.quit).grid(row=3, column=self.nb_max)
        self.ale=Button(self,text='code aléatoire', command=self.rand)
        self.ale.grid(row=4,column=self.nb_max//2,columnspan=1 if self.nb_max%2 else 2)
    def jouer(self,couleur):
        self.emplacements[self.emplacement_actif].configure(bg=self.couleurs[couleur])
        self.emplacement_actif+=1
        self.prec_essai.append(couleur)
        if self.emplacement_actif != self.nb_emplacements: return

        self.emplacement_actif=0
        self.essais+=1
        if self.essais:
            for e in range(self.nb_emplacements):
                self.emplacements_prec_essai[e].configure(bg=self.couleurs[self.prec_essai[e]])
            if self.reponce==self.prec_essai:
                Label(Tk(),text=f'gagné en {self.essais} essais').pack()
            rep=[]
            for i,e in enumerate(self.prec_essai):
                if self.reponce[i]==e:
                    rep.append(1)
                elif e in self.reponce:
                    rep.append(0)
                else:rep.append(None)
            self.can.delete(ALL)
            coins=(10,55)
            random.shuffle(rep)
            for i,p in enumerate(rep):
                if p!=None:
                    self.can.create_oval(coins[i%2],coins[i//2],coins[i%2]+10,coins[i//2]+10,fill=self.dico_reponce[p])
        else:
            self.enregister_reponce(self.prec_essai)
        self.wipe_prec_essai()

    def annuler(self):
        if self.emplacement_actif==0: return
        self.emplacement_actif -= 1
        self.emplacements[self.emplacement_actif].configure(bg=self.couleur_vide)
        self.prec_essai.pop()
    def rejouer(self):
        if self.essais==-1:return
        self.emplacement_actif = 0
        self.essais = -1
        self.prec_essai = []
        self.master.title('codage')
        self.can.destroy()
        self.ale = Button(self, text='code aléatoire', command=self.rand)
        self.ale.grid(row=4, column=0, columnspan=self.nb_couleurs)
        for ep,e in zip(self.emplacements_prec_essai,self.emplacements):
            ep.configure(bg='#eeeeee')
            e.configure(bg=self.couleur_vide)
    def rand(self):
        self.enregister_reponce([random.randint(0,self.nb_couleurs-1) for _ in range(len(self.emplacements))])
        self.wipe_prec_essai()
        self.essais = 0
    def enregister_reponce(self,reponse):
        self.master.title('jeu')
        self.reponce = reponse
        self.can = Canvas(self, height=75, bg='#aaaaaa', width=75)
        self.can.grid(row=1, column=self.endroit_emplacement-1, sticky=EW)
        self.ale.destroy()
    def wipe_prec_essai(self):
        for e in self.emplacements:
            e.configure(bg=self.couleur_vide)
        self.prec_essai = []
if __name__ == '__main__':
    f = Tk()
    #f.resizable(width=0,height=0)
    mastermind(f)
    f.mainloop()