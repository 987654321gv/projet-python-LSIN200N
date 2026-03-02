"""

"""
from collections import Counter
import random

longeur = 4
nb_couleurs = 8
liste_next = [0] * longeur
set_solutions = {tuple(liste_next)}
while liste_next:
    liste_next[-1] += 1
    if liste_next[-1] == nb_couleurs:
        liste_next.pop()
    else:
        liste_next.extend([0] * (longeur - len(liste_next)))
        set_solutions.add(tuple(liste_next))


def get_rep(solution, essai):
    r1 = 0
    for s, e in zip(solution, essai):
        if s == e:
            r1 += 1
    r0 = sum((Counter(essai) & Counter(solution)).values()) - r1
    return r0, r1


set_solutions_possibles = set_solutions


def IA(is_2nd_try=False):
    if is_2nd_try:
        essai = {256: (5, 6, 7, 5), 500: (5, 5, 4, 4), 976: (5, 5, 4, 4), 936: (1, 2, 0, 6), 224: (3, 2, 6, 2),
                 72: (0, 2, 4, 6), 660: (5, 1, 7, 3), 204: (2, 1, 1, 2), 216: (0, 2, 4, 6), 28: (0, 2, 4, 6),
                 6: (2, 1, 1, 0), 9: (3, 2, 6, 2), 8: (2, 1, 1, 0), 1: (0, 1, 2, 3)}[len(set_solutions_possibles)]
        dict_reps = {}
        for solution in set_solutions_possibles:
            rep = get_rep(solution, essai)
            if rep in dict_reps:
                dict_reps[rep].add(solution)
            else:
                dict_reps[rep] = {solution}
        return essai, dict_reps
    if len(set_solutions_possibles) == 1:
        return list(set_solutions_possibles)[0], {(0, 4): set_solutions_possibles}
    if set_solutions_possibles == set_solutions:
        essai = tuple(range(longeur))
        dict_reps = {}
        for solution in set_solutions_possibles:
            rep = get_rep(solution, essai)
            if rep in dict_reps:
                dict_reps[rep].add(solution)
            else:
                dict_reps[rep] = {solution}
        return essai, dict_reps
    best = ((), {}, set())
    for essai in set_solutions:
        dict_reps = {}
        for solution in set_solutions_possibles:
            rep = get_rep(solution, essai)
            if rep in dict_reps:
                dict_reps[rep].add(solution)
            else:
                dict_reps[rep] = {solution}
        res = max(map(len, dict_reps.values()))
        if best == ((), {}, set()) or res < best[-1]:
            best = (essai, dict_reps, res)
    return best[:-1]


def update_solutions(solution, essai):
    global set_solutions_possibles
    set_solutions_possibles = {s for s in set_solutions_possibles if get_rep(essai, s) == get_rep(solution, essai)}


def get_dict_rep(essai):
    dict_reps = {}
    for solution in set_solutions_possibles:
        rep = get_rep(solution, essai)
        if rep in dict_reps:
            dict_reps[rep].add(solution)
        else:
            dict_reps[rep] = {solution}
    return dict_reps


def play():
    global set_solutions_possibles
    solution = tuple(random.randint(0, 7) for _ in range(4))
    print(f'la solution est : {solution}')
    nb_essais = 1
    while len(set_solutions_possibles) > 1:
        coup_IA, dict_IA = IA()
        print(f"l'IA joue : {coup_IA}")
        rep = get_rep(solution, coup_IA)
        print(f"réponse : {rep}")
        set_solutions_possibles = dict_IA[rep]
        print(f"il reste {len(set_solutions_possibles)}/{len(set_solutions)} possibilités")
        nb_essais += 1
    print(f"l'IA joue : {tuple(set_solutions_possibles)[0]}")
    print(f"réponse : {(4, 4)}")
    print(f"l'IA à trouvé la solution en {nb_essais} essais !")


def voir_2e_coups():
    global set_solutions_possibles
    dict_reps = IA()[1]
    dict_essais = {}
    for rep in dict_reps:
        set_solutions_possibles = dict_reps[rep]
        dict_essais[len(set_solutions_possibles)] = IA()[0]
        print(rep, dict_essais[len(set_solutions_possibles)], len(set_solutions_possibles))
    print(dict_essais)


def pire_scenario():
    global set_solutions_possibles
    nb_essais = 1
    while len(set_solutions_possibles) > 1:
        coup_IA, dict_IA = IA()
        print(f"l'IA joue : {coup_IA}")
        solution = tuple(max(dict_IA.values(), key=len))[0]
        rep = get_rep(solution, coup_IA)
        print(f"réponse : {rep}")
        set_solutions_possibles = dict_IA[rep]
        print(f"il reste {len(set_solutions_possibles)}/{len(set_solutions)} possibilités")
        nb_essais += 1
    print(f"l'IA joue : {tuple(set_solutions_possibles)[0]}")
    print(f"réponse : {(4, 4)}")
    print(f"l'IA à trouvé la solution en {nb_essais} essais !")


def vs1():
    global set_solutions_possibles
    solution = tuple(map(int, input("entrez la solution : ").split()))
    nb_essais = 1
    while len(set_solutions_possibles) > 1:
        coup_IA, dict_IA = IA()
        print(f"l'IA joue : {coup_IA}")
        rep = get_rep(solution, coup_IA)
        print(f"réponse : {rep}")
        set_solutions_possibles = dict_IA[rep]
        print(f"il reste {len(set_solutions_possibles)}/{len(set_solutions)} possibilités")
        nb_essais += 1
    print(f"l'IA joue : {tuple(set_solutions_possibles)[0]}")
    print(f"réponse : {(4, 4)}")
    print(f"l'IA à trouvé la solution en {nb_essais} essais !")


def vs2():
    global set_solutions_possibles
    nb_essais = 1
    while 1:
        coup = tuple(map(int, input("entrez votre coup : ").split()))
        dict_IA = get_dict_rep(coup)
        solution = tuple(max(dict_IA.values(), key=len))[0]
        if coup == solution:
            if len(set_solutions_possibles) > 1:
                for e in dict_IA.values():
                    if e != coup:
                        solution = e
                        break

            else:
                print("bravo, c'est la solution !")
                break
        rep = get_rep(solution, coup)
        print(f"réponse : {rep}")
        set_solutions_possibles = dict_IA[rep]
        nb_essais += 1
    print(f"tu as mis {nb_essais} essais")


if __name__ == '__main__':
    vs1()
    vs2()
