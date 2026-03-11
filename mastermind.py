"""

"""
from tkinter import *
import random
from math import sqrt, ceil
from collections import Counter
import IA_draft
from json import load, dump
import re
from tkinter import messagebox


class Mastermind(Frame):
    def __init__(self, boss=None):
        Frame.__init__(self, boss)
        self.pack()
        self.parametres_vars = {"version alt": BooleanVar(),
                                "IA active": BooleanVar(),
                                "nb emplacements": IntVar(),
                                "essais max": IntVar(),
                                "chaos degree": bounded_IntVar(3),
                                "couleur vide": ColorVar(),
                                "couleurs": ListVar()}
        self.parametres = {"version alt": False,
                           "IA active": True,
                           "nb emplacements": 4,
                           "essais max": 10,
                           "chaos degree": 2,
                           "couleur vide": '#553823',
                           "couleurs": ['#ffffff', '#000000', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00aaee',
                                        '#ffaaee']}
        try:
            with open("parametres.txt", "r") as parametres:
                self.parametres |= load(parametres)
        except FileNotFoundError:
            open("parametres.txt", "w").close()
        self.setup_menu()

        #### valeurs arbitraires ####
        self.couleurs = self.parametres["couleurs"]
        self.couleur_vide = self.parametres["couleur vide"]
        self.nb_emplacements = self.parametres["nb emplacements"]
        self.version_alt = self.parametres["version alt"]
        self.chaos_degree = self.parametres["chaos degree"]
        self.essais_max = self.parametres["essais max"]
        self.IA_active = self.parametres["IA active"]
        self.dico_reponce = ('#ffffff', '#000000')
        #### initialisations ####
        self.canvases: list[Canvas] = []
        self.emplacements: list[Frame] = []
        self.historique: list[Frame] = []
        self.boutons_couleurs: list[Button] = []
        self.destroy_on_replay = []
        self.historique_ints = []
        self.IA_2nd_try_opti = False
        self.rep_hist = []
        self.emplacement_actif = 0
        self.essais = -1
        self.prec_essai = []
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
            self.emplacements.append(Frame(self, height=75, width=75, bg=self.couleur_vide))
            self.emplacements[-1].grid(row=0, column=self.endroit_emplacement + i, sticky=EW)
        for i, c in enumerate(self.couleurs):
            self.boutons_couleurs.append(
                Button(self, background=c, width=10, height=2, command=lambda couleur=i: self.jouer(couleur)))
            self.boutons_couleurs[-1].grid(row=self.essais_max + 1, column=i + self.endroit_couleurs, sticky=EW)
        Button(self, text='annuler', command=self.annuler).grid(row=self.essais_max + 2, column=self.nb_max // 2,
                                                                columnspan=1 if self.nb_couleurs % 2 else 2)
        Button(self, text='rejouer', command=self.rejouer).grid(row=self.essais_max + 2, column=self.endroit_couleurs)
        Button(self, text='quiter', command=self.master.destroy).grid(row=self.essais_max + 2, column=self.fin_couleurs)
        self.ale = Button(self, text='code aléatoire', command=self.rand)
        self.ale.grid(row=self.essais_max + 3, column=self.nb_max // 2, columnspan=1 if self.nb_couleurs % 2 else 2)

    def jouer(self, couleur):
        self.emplacements[self.emplacement_actif].configure(bg=self.couleurs[couleur])
        self.emplacement_actif += 1
        self.prec_essai.append(couleur)
        self.historique_ints.append(couleur)
        if self.emplacement_actif != self.nb_emplacements: return
        self.emplacement_actif = 0
        self.essais += 1
        if self.essais:
            if self.IA_active:
                if self.essais == 1 and self.prec_essai == [0, 1, 2, 3]:
                    self.IA_2nd_try_opti = True
                else:
                    self.IA_2nd_try_opti = False
            if self.IA_active:
                IA_draft.update_solutions(self.reponse, self.prec_essai)
            row = self.essais_max - self.essais
            for i, couleur in enumerate(self.prec_essai):
                case = Frame(self, height=75, width=75, bg=self.couleurs[couleur])
                case.grid(row=row, column=self.endroit_emplacement + i, sticky=NSEW)
                self.historique.append(case)
            if self.winfo_screenheight() * 3 < self.winfo_reqheight() * 4:
                for e in self.historique:
                    e.configure(height=e.winfo_reqwidth() // 2)
                for c, (r0, r1) in zip(self.canvases[::-1], self.rep_hist[::-1]):
                    if r1 or r0:
                        self.destroy_on_replay.append(Frame(self, background=self.couleur_vide))
                        self.destroy_on_replay[-1].grid(row=c.grid_info()['row'],
                                                        column=self.endroit_emplacement - 1, sticky=NSEW)
                    if r0:
                        self.destroy_on_replay.append(Label(self, text=str(r0), foreground='#ffffff',
                                                            background=self.couleur_vide))
                        self.destroy_on_replay[-1].grid(row=c.grid_info()['row'],
                                                        column=self.endroit_emplacement - 1, sticky=W)
                    if r1:
                        self.destroy_on_replay.append(Label(self, text=str(r1), background=self.couleur_vide))
                        self.destroy_on_replay[-1].grid(row=c.grid_info()['row'],
                                                        column=self.endroit_emplacement - 1, sticky=E)

                    c.destroy()
                self.canvases = []
            if self.reponse == self.prec_essai:
                Label(Toplevel(), text=f'gagné en {self.essais} essais').pack()
            elif self.essais >= self.essais_max:
                Label(Toplevel(), text='perdu !').pack()
                for e, r in zip(self.emplacements, self.reponse):
                    e.configure(bg=self.couleurs[r])
                return
            r0 = 0
            r1 = 0
            if not self.version_alt:
                r0 = sum((Counter(self.prec_essai) & self.count_reponse).values())
            for i, e in enumerate(self.prec_essai):
                if self.reponse[i] == e:
                    r1 += 1
                    if not self.version_alt:
                        r0 -= 1
                elif e in self.reponse and self.version_alt:
                    r0 += 1

            self.rep_hist.append((r0, r1))
            rep = [0] * r0 + [1] * r1
            if self.chaos_degree == 2:
                rep.extend([None] * ((self.side ** 2) - len(rep)))

            can = Canvas(self, height=75, bg='#aaaaaa', width=75)
            can.grid(row=row, column=self.endroit_emplacement - 1, sticky=EW)
            self.canvases.append(can)

            if self.chaos_degree != 0:
                random.shuffle(rep)
            elif self.version_alt:
                rep.sort()
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
        self.historique_ints.pop()

    def saugarder_les_option(self):
        dico_params = {e: self.parametres_vars[e].get() for e in self.parametres_vars}
        with open("parametres.txt", "w") as parametres:
            dump(dico_params, parametres)

    def rejouer(self):
        if self.essais == -1: return
        self.emplacement_actif = 0
        self.essais = -1
        self.prec_essai = []
        self.historique_ints = []
        self.master.title('codage')
        for can in self.canvases:
            can.destroy()
        self.canvases = []
        self.ale = Button(self, text='code aléatoire', command=self.rand)
        self.ale.grid(row=self.essais_max + 3, column=0, columnspan=self.nb_couleurs)
        for ep in self.historique:
            ep.destroy()
        for e in self.emplacements:
            e.configure(bg=self.couleur_vide)
        for e in self.destroy_on_replay:
            e.destroy()
        self.historique = []
        self.destroy_on_replay = []
        if self.IA_active:
            IA_draft.set_solutions_possibles = IA_draft.set_solutions.copy()
            self.IA_2nd_try_opti = False

    def rand(self):
        self.enregister_reponce([random.randint(0, self.nb_couleurs - 1) for _ in range(len(self.emplacements))])
        self.historique_ints.extend(self.reponse)
        self.wipe_prec_essai()
        self.essais = 0
        self.emplacement_actif = 0

    def enregister_reponce(self, reponse):
        self.master.title('jeu')
        self.reponse = reponse
        self.count_reponse = Counter(reponse)
        self.ale.destroy()
        if self.IA_active:
            self.destroy_on_replay.append(Button(self, text='suggestion', command=self.suggestion))
            self.destroy_on_replay[-1].grid(row=self.essais_max + 3, column=self.endroit_couleurs)
            self.destroy_on_replay.append(Button(self, text="coup de l'IA", command=self.IA))
            self.destroy_on_replay[-1].grid(row=self.essais_max + 3, column=self.fin_couleurs)

    def wipe_prec_essai(self):
        for e in self.emplacements:
            e.configure(bg=self.couleur_vide)
        self.prec_essai = []

    def suggestion(self):
        e = IA_draft.set_solutions_possibles.pop()
        IA_draft.set_solutions_possibles.add(e)
        for c in e:
            self.boutons_couleurs[c].flash()

    def IA(self):
        if self.IA_2nd_try_opti:
            for e in IA_draft.IA(True)[0]:
                self.jouer(e)
        else:
            for e in IA_draft.IA()[0]:
                self.jouer(e)

    def setup_menu(self):
        self.master.option_add('*tearOff', FALSE)
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        menubar.add_command(label='Sauvegarder les options', command=self.saugarder_les_option, underline=0)
        menu_parametres = Menu(menubar)
        menubar.add_cascade(label='Parametres', menu=menu_parametres)
        for i, (param, var) in enumerate(self.parametres_vars.items()):
            self.setup_param(menu_parametres, i, param, var)
        menubar.add_command(label="Sauvegarder la partie", command=self.sauvegarder_partie)
        menubar.add_command(label="Charger la partie", command=self.charger_partie)

    def setup_param(self, menu: Menu, i: int, param: str, var: Variable):
        if param:
            var.set(self.parametres[param])
        if isinstance(var, BooleanVar):
            menu.insert_checkbutton(i, label=param, variable=var)
        if isinstance(var, IntVar):
            new_menu = Menu(menu)
            menu.insert_cascade(i, label=f'{param} : {var.get()}', menu=new_menu)
            new_menu.add_command(label='+', command=lambda v=var, n=i, p=param, m=menu:
            (v.set(v.get() + 1), m.entryconfigure(n, label=f'{p} : {v.get()}')))
            new_menu.add_command(label='-', command=lambda v=var, n=i, p=param, m=menu:
            (v.set(v.get() - 1), m.entryconfigure(n, label=f'{p} : {v.get()}')))
        if isinstance(var, ColorVar):
            if param:
                menu.insert_command(i, label=f'{param} : {var.get()}', foreground=var.get(),
                                    command=lambda v=var, n=i, p=param, m=menu: v.set_color(m, n, p))
            else:
                menu.insert_command(i, label=var.get(), foreground=var.get(),
                                    command=lambda v=var, n=i, p=param, m=menu: v.set_color(m, n, p))

        if isinstance(var, ListVar):
            new_menu = Menu(menu)
            menu.insert_cascade(i, label=param, menu=new_menu)
            for n, v in enumerate(var.liste):
                self.setup_param(new_menu, n, '', v)
            new_menu.add_separator()
            new_menu.add_command(label='-', command=lambda v=var, m=new_menu: (v.pop(), m.delete(len(v))))
            new_menu.add_command(label='+', command=lambda v=var, m=new_menu:
            (v.append(type(v[-1])()), self.setup_param(m, len(v) - 1, '', v[-1])))

    def sauvegarder_partie(self):
        sauv_fenetre = Toplevel(self)
        sauv_fenetre.title("Sauvegarder une partie")
        Label(sauv_fenetre, text="Nom de la partie :").pack(padx=50, pady=50)
        nom_var = StringVar()
        entry = Entry(sauv_fenetre, textvariable=nom_var)
        entry.pack(padx=10, pady=5)

        def sauvegarder():
            nom_partie = nom_var.get().strip()
            
            # Lire le fichier existant
            try:
                with open("save.txt", "r") as f:
                    data = load(f)
            except FileNotFoundError:
                data = {}

            data[nom_partie] = self.historique_ints # Ajouter la nouvelle partie
            # Écrire dans le fichier
            with open("save.txt", "w") as f:
                dump(data, f)
            sauv_fenetre.destroy()
            messagebox.showinfo("Sauvegarde", "Partie sauvegardée avec succès !")
        Button(sauv_fenetre, text="Sauvegarder", command=sauvegarder).pack(padx=70, pady=50)

    def charger_partie(self):
        try:
            with open("save.txt", "r") as f:
                data = load(f)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Aucune partie sauvegardée trouvée !")
            return

         # Créer la fenêtre pour choisir la partie
        choix_fenetre = Toplevel(self)
        choix_fenetre.title("Charger une partie")

        nom_var = StringVar()
        noms_parties = list(data.keys())
        nom_var.set(noms_parties[0])  # valeur par défaut

        menu = OptionMenu(choix_fenetre, nom_var, *noms_parties)
        menu.pack(padx=100, pady=100)

        def charger_selection():
            partie = nom_var.get()
            self.rejouer()  # réinitialiser le plateau

            for e in data[partie]:
                self.jouer(e)  # reconstruire le plateau avec les essais sauvegardés

            choix_fenetre.destroy()
            messagebox.showinfo("Chargement", f"Partie '{partie}' rechargée avec succès !")

        bouton_charger = Button(choix_fenetre, text="Charger", command=charger_selection)
        bouton_charger.pack(padx=10, pady=10)


class bounded_IntVar(IntVar):
    def __init__(self, max_value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max = max_value

    def set(self, value):
        super().set(value % self.max)


class ColorVar(StringVar):
    _default = '#000000'

    def set_color(self, menu: Menu, index, param):
        def func():
            if not re.match("#[0-9a-f]{6}$", e.get()): return
            self.set(e.get())
            new_f.destroy()
            if param:
                menu.entryconfigure(index, label=f'{param} : {self.get()}', foreground=self.get())
            else:
                menu.entryconfigure(index, label=self.get(), foreground=self.get())

        new_f = Toplevel()
        e = Entry(new_f)
        e.grid(row=0, column=1, sticky=NSEW)
        e.insert(0, self.get())
        Label(new_f, text='Entrez la valeur :').grid(row=0, column=0, sticky=NSEW)
        Button(new_f, text='OK', command=func).grid(row=1, column=0, columnspan=2, sticky=NSEW)


class ListVar(Variable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.liste = []

    def set(self, value):
        res = []
        for e in value:
            if isinstance(e, list): res.append(ListVar(e))
            if isinstance(e, int): res.append(IntVar(value=e))
            if isinstance(e, bool): res.append(BooleanVar(value=e))
            if isinstance(e, str) and re.match("#[0-9a-f]{6}$", e): res.append(ColorVar(value=e))

        self.liste[:] = res

    def get(self):
        return [e.get() for e in self.liste]

    def pop(self):
        return self.liste.pop().get()

    def append(self, item):
        self.liste.append(item)

    def __getitem__(self, index):
        return self.liste[index]

    def __len__(self):
        return len(self.liste)

    def __setitem__(self, key, value):
        self.liste[key].set(value)


if __name__ == '__main__':
    f = Tk()
    f.resizable(width=0, height=0)
    Mastermind(f)
    f.mainloop()
