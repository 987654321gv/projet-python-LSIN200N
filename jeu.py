"""

"""
from tkinter import *

class glob():
    longeur=6
    largeur=7
    table=dict()
    table_active=True
    table_locale=True
def binarisation(liste, dictionaire):
    return sum(dictionaire[liste[i]] * (len(dictionaire) ** i) for i in range(len(liste)))


def debinarisation(binaire, liste, longueur):
    b2 = binaire
    res = []
    for _ in range(longueur):
        res.append(liste[b2 % len(liste)])
        b2 -= b2 % len(liste)
        b2 //= len(liste)
    return res


def f2(b):
    l = 7
    s = 0
    for i in range(len(b)):
        if b[i] == 0:
            l = i
            break
        s += {-1: 0, 1: 1}[b[i]] * (2 ** i)
    return (s, l)


def f(a):return tuple(f2(b) for b in a)




if glob.table_active and not(glob.table_locale):
    with open('source_IA_puissance4(2).txt') as source:
        i=0
        for l in source:
            i+=1
            print(f'initialitation {i}/43')
            if l=='':continue
            try:
                d = eval(l)
                for cle in d:
                    glob.table[cle] = d[cle]
                    glob.table[cle]['d'] = debinarisation(d[cle]['d'], [True, False], 7)
                    glob.table[cle]['d2'] = debinarisation(d[cle]['d2'], [True, False], 7)
            except:
                print('raté')
class position():
    alligements=[[[a for a in [(x-i,y+i),(x  ,y+i),(x+i,y+i),
                                (x-i,y  ),          (x+i,y  ),
                                (x-i,y-i),(x  ,y-i),(x+i,y-i)] ]for i in range(4)]
                 for x in range(glob.largeur) for y in range(glob.longeur)]
    alligements=[[[l[i][i2] for i in range(4) if l[i][i2][0] in range(glob.largeur) and l[i][i2][1] in range(glob.longeur)] for i2 in range(8)] for l in alligements]
    alligements=[a for l in alligements for a in l if len(a)==4]
    alligements3 = [[[a for a in [(x - i, y + i), (x, y + i), (x + i, y + i),
                                 (x - i, y), (x + i, y),
                                 (x - i, y - i), (x, y - i), (x + i, y - i)]] for i in range(3)]
                   for x in range(glob.largeur) for y in range(glob.longeur)]
    alligements3 = [
        [[l[i][i2] for i in range(3) if l[i][i2][0] in range(glob.largeur) and l[i][i2][1] in range(glob.longeur)] for i2 in range(8)] for l
        in alligements3]
    alligements3 = [a for l in alligements3 for a in l if len(a) == 3]

    alligements2 = [[[a for a in [(x - i, y + i), (x, y + i), (x + i, y + i),
                                  (x - i, y), (x + i, y),
                                  (x - i, y - i), (x, y - i), (x + i, y - i)]] for i in range(3)]
                    for x in range(glob.largeur) for y in range(glob.longeur)]
    alligements2 = [
        [[l[i][i2] for i in range(3) if l[i][i2][0] in range(glob.largeur) and l[i][i2][1] in range(glob.longeur)] for
         i2 in range(8)] for l
        in alligements2]
    alligements2 = [a for l in alligements2 for a in l if len(a) == 3]
    vide=0
    valeurs_possible=[-1,1]
    ordre_par_defaut=[int(((-1)**i)*i//2+3) for i in range(7)]

    profondeurIA=4

    def __init__(self,grille,tour):
        self.grille=[[c for c in l] for l in grille]
        self.tour=tour
        self.vict=0
        self.evalu=0
        self.evalu2=0
    def __call__(self, x, y):return self.grille[y][x]
    def poser(self,x):
        if self(x,0):return True
        for y in range(glob.longeur):
            if y==5 or self(x,y+1)!=self.vide:
                self.grille[y][x]=self.tour
                break
        als=[[self(*c) for c in a] for a in self.alligements]
        [self.victoire(v) for v in self.valeurs_possible if [v]*4 in als]
        self.tour*=-1
        return False

    def copy(self):return position(self.grille,self.tour)
    def get_tuple(self):return tuple(tuple(l) for l in self.grille) if glob.table_locale else f(self.grille)
    def IA(self,profondeur=profondeurIA,evaluations=False,evaluations2=False,ordre=True,table=glob.table_active):
        res=3
        args=[evaluations,evaluations2,ordre,table]
        d= [False for _ in range(glob.largeur)]
        d2= [False for _ in range(glob.largeur)]
        self.vict=-self.tour
        if evaluations:evalus=[0 for _ in range(glob.largeur)]
        if evaluations2: evalus2 = [0 for _ in range(glob.largeur)]
        ok=True
        if table:
            t = self.get_tuple()
            if t in glob.table.keys():
                p=glob.table[t]
                if p['profondeur']>=profondeur:
                    if evaluations:self.evalu=p['evalu']
                    if evaluations2:self.evalu2=p['evalu2']
                    self.vict=p['vict']
                    d = p['d']
                    d2 = p['d2']
                    ok=False

        if ok:
            for x in range(glob.largeur):
                p2=self.copy()
                if p2.poser(x):
                    d2[x]=True
                    continue
                if p2.vict:
                    res=x
                    self.vict=p2.vict
                    if p2.vict != self.tour:d[x] = True
                    break
                elif profondeur:
                    p2.IA(profondeur-1,*args)
                    if evaluations:evalus[x]=p2.evalu
                    if evaluations2: evalus2[x] = p2.evalu2
                else:
                    if evaluations:evalus[x]=p2.evaluation()
                    if evaluations2:evalus2[x] = p2.evaluation2()
                if p2.vict:
                    if p2. vict==self.tour:
                        self.vict=self.tour
                        res=x
                        break
                    else:d[x]=True
                elif self.vict==-self.tour:self.vict=0
            if evaluations:self.evalu=min(evalus)
            if evaluations2: self.evalu2 = min(evalus2)
            if table:
                if t in glob.table.keys():ok= (glob.table[t]['profondeur']<profondeur)
                else:ok=True
                if ok:
                    p=dict()
                    if evaluations:
                        p['evalu']=self.evalu
                        p['evalus']=evalus
                    if evaluations2:
                        p['evalu2'] = self.evalu2
                        p['evalus2'] = evalus2
                    p['vict']=self.vict
                    p['d']=d
                    p['d2']=d2
                    p['profondeur']=profondeur
                    glob.table[t]=p
                    self.amelioration()
        if profondeur==self.profondeurIA:
            if self.vict==self.tour:return res
            evalusi=self.ordre_par_defaut.copy() if ordre else [(i+3)%glob.largeur for i in range(glob.largeur)]
            if self.vict == 0:
                if evaluations2: evalusi.sort(key=lambda i: evalus2[i])
                if evaluations:evalusi.sort(key=lambda i:evalus[i])
                evalusi.sort(key=lambda i: d[i])
            evalusi.sort(key=lambda i: d2[i])
            return evalusi[0]
    def victoire(self,t):self.vict=t
    def amelioration(self):pass
    def evaluation(self):
        res=0
        als = [[self(*c) for c in a] for a in self.alligements3]
        for v in self.valeurs_possible:
            if [v] * 3 in als:
                res-=v*self.tour
        return res
    def evaluation2(self):
        res=0
        als = [[self(*c) for c in a] for a in self.alligements2]
        for v in self.valeurs_possible:
            if [v] * 2 in als:
                res-=v*self.tour
        return res



class puissance_4(Frame):
    def __init__(self,boss=None):
        Frame.__init__(self,boss,background='#c3c3c3')
        self.pack()
        self.dernier=[]
        self.li = []
        self.grille = []
        self.color_dict = {'R': '#ff0000', 'J': '#ffff00', 'V': '#ffffff'}
        self.can = Canvas(self, width=450, height=350,background='#0000ff')
        self.can.grid(row=2, column=0, columnspan=9, rowspan=glob.longeur)
        self.choixligne=IntVar()
        self.tour=0
        Button(self,text='quitter',command=self.master.quit).grid(row=8, column=2)
        Button(self,text='rejouer',command=self.rejouer).grid(row=8, column=6)
        Button(self, text='annuler', command=self.annuler).grid(row=8, column=4)
        Button(self, text='sauve\ngarder', command=self.sauvegarder).grid(row=9, column=3)
        Button(self, text='charger', command=self.charger).grid(row=9, column=5)
        Button(self, text='passer', command=self.passer).grid(row=9, column=4)
        for line in range(glob.largeur):
            l2 = []
            l3 = []
            for p in range(glob.longeur):
                l2[0:0]=[self.can.create_oval(24+57 * line,50+50 * p,74 + 57 * line,100 + 50 * p, fill=self.color_dict['V'])]
                l3[0:0]=['V']
            self.li.append(l2)
            self.grille.append(l3)
            Radiobutton(self, text='', variable=self.choixligne, value=line,background='#c3c3c3').grid(row=1, column=1+line)
        Button(self, text='Jouer', command=self.placer).grid(row=0, column=3)
        Button(self, text="Jouer\ncontre\nl'IA", command=self.jouer_contre_IA).grid(row=0, column=4)
        Button(self, text="Laisser\nl'IA\njouer", command=self.IA).grid(row=0, column=5)
    def annuler(self):
        if self.dernier!=[]:
            self.grille[self.dernier[-1][0]][self.dernier[-1][1]] = 'V'
            self.can.itemconfig(self.li[self.dernier[-1][0]][self.dernier[-1][1]], fill=self.color_dict['V'])
            self.tour=not(self.tour)
            self.dernier[-1:len(self.dernier)]=[]
    def rejouer(self):
        self.dernier=[]
        for colonne in range(glob.largeur):
            for l in range(glob.longeur):
                self.grille[colonne][l] ='V'
                self.can.itemconfig(self.li[colonne][l], fill=self.color_dict[self.grille[colonne][l]])
    def placer_pion(self,couleur, colonne, grille):
        ok=False
        r=grille
        for l in range(glob.longeur):
            if grille[colonne][l]== 'V'and not(ok):
                ok=True
                r[colonne][l]=couleur
                self.can.itemconfig(self.li[colonne][l],fill=self.color_dict[self.grille[colonne][l]])
                self.dernier.append((colonne,l))
        return ((ok,r))
    def placer(self):
        if self.tour:
            a,self.grille=self.placer_pion('R',self.choixligne.get(),self.grille)
            if a:
                self.tour = 0
        else:
            a,self.grille=self.placer_pion('J',self.choixligne.get(),self.grille)
            if a:
                self.tour = 1
        g=self.gagnant(self.grille)
        if g!=None:
            if g=='R':
                print('le joueur rouge a gagné!')
                f_2=Tk()
                Label(f_2, text='bravo au joueur rouge!').pack(side=TOP)
                Button(f_2, text='quitter', command=f_2.quit).pack(side=BOTTOM)
            else:
                print('bravo au joueur jaune !')
                f_2 = Tk()
                Label(f_2, text='le joueur jaune a gagné!').pack(side=TOP)
                Button(f_2, text='quitter', command=f_2.quit).pack(side=BOTTOM)
    def gagnant(self,grille):
        def test_g(grille,c,x,y,dx,dy):
            test=0
            for step in range(1,4):
                try:
                    if grille[y+dy*step][x+dx*step]==c:
                        test=test+1
                except:
                    pass
            return test==3
        y=0
        for l in grille:
            x=0
            for p in l:
                if p!='V':
                    g=x>2
                    d=x<4
                    for a in range(g*-1,d+1):
                        if y>2:
                            if test_g(grille,p,x,y,a,-1):
                                return p
                        else:
                            if test_g(grille,p,x,y,a,1):
                                return p
                    if g:
                        if test_g(grille, p, x, y, -1, 0):
                            return p
                    if d:
                        if test_g(grille, p, x, y, 1, 0):
                            return p
                x=x+1
            y=y+1
        return None
    def IA(self):
        grille=[[{'R':-1,'V':0,'J':1}[self.grille[i][-i2-1]] for i in range(len(self.grille))] for i2 in range(len(self.grille[0]))]
        if self.tour:
            a,self.grille=self.placer_pion('R',position(grille,-1).IA(),self.grille)
            if a:self.tour = 0
        else:
            a,self.grille=self.placer_pion('J',position(grille,1).IA(),self.grille)
            if a:self.tour = 1
        g=self.gagnant(self.grille)
        if g!=None:
            if g=='R':
                print('le joueur rouge a gagné!')
                f_2=Tk()
                Label(f_2, text='bravo au joueur rouge!').pack(side=TOP)
                Button(f_2, text='quitter', command=f_2.quit).pack(side=BOTTOM)
            else:
                print('bravo au joueur jaune !')
                f_2 = Tk()
                Label(f_2, text='le joueur jaune a gagné!').pack(side=TOP)
                Button(f_2, text='quitter', command=f_2.quit).pack(side=BOTTOM)
    def jouer_contre_IA(self):
        self.placer()
        self.IA()
    def sauvegarder(self):
        c=''
        for d in self.dernier:c+=str(d[0])
        print('code:',c)
    def charger(self):
        self.rejouer()
        for d in input('code:'):
            self.placer_pion('R' if self.tour else 'J',int(d),self.grille)
            self.tour=not(self.tour)
    def passer(self):self.tour=not(self.tour)

def sauvegarder():
    if glob.table_active and not(glob.table_locale):
        glob.liste=[dict() for _ in range(43)]
        for cle in glob.table:
            l=ligne(cle)
            glob.liste[l][cle]=glob.table[cle]
            glob.liste[l][cle]['d']=binarisation(glob.liste[l][cle]['d'],{True: 1, False: 0})
            glob.liste[l][cle]['d2'] = binarisation(glob.liste[l][cle]['d2'], {True: 1, False: 0})
        with open('source_IA_puissance4(2).txt', 'w') as source:
            for l in glob.liste: source.write(str(l) + '\n')

def ligne(a):return sum(b[1] for b in a)
if __name__ == '__main__':
    fen=Tk()
    fen.resizable(width=0, height=0)
    puissance_4(fen)
    fen.mainloop()
    sauvegarder()