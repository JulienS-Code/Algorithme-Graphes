import doctest
from determinisation import *
from complémentation import *

auto6 ={"alphabet":['a','b'],"etats": [0,1,2,3,4,5],
"transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0],
[4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]], "I":[0],"F":[0,1,2,5]}


def minimise(automate: dict) -> dict:
    """
    Fonction minimise qui étant donné un automate complet et déterministe renvoie
    l’automate minimisé.
    >>> print(minimise(auto6))
    {'alphabet': ['a', 'b'], 'etats': [[0], [1, 2, 5], [3], [4]], 'transitions': [[[0], 'a', [4]], [[0], 'b', [3]], [[1, 2, 5], 'a', [1, 2, 5]], [[1, 2, 5], 'b', [1, 2, 5]], [[3], 'a', [1, 2, 5]], [[3], 'b', [0]], [[4], 'a', [1, 2, 5]], [[4], 'b', [1, 2, 5]]], 'I': [[0]], 'F': [[0], [1, 2, 5]]}
    >>> print(renommage(minimise(auto6)))
    {'alphabet': ['a', 'b'], 'etats': [0, 1, 2, 3], 'transitions': [[0, 'a', 3], [0, 'b', 2], [1, 'a', 1], [1, 'b', 1], [2, 'a', 1], [2, 'b', 0], [3, 'a', 1], [3, 'b', 1]], 'I': [0], 'F': [0, 1]}
    """
    if not deterministe(automate) or not complet(automate): # l'automate doit être déterministe et complet
        assert("Automate non déterministe ou non complet")
    
    # initialisation des variables
    alphabet = automate["alphabet"]
    etats = automate["etats"]
    old_transitions = automate["transitions"]
    etats_finaux = set(automate["F"])
    etats_non_finaux = set(etats) - etats_finaux

    classes = [etats_finaux, etats_non_finaux] # initialisation de la classe à l'étape 0
    classe_finales = []

    while classes != classe_finales: # si l'étape n-1 est équivalent à l'étape n, l'automate est minimisé
        classe_finales = classes[:] # mise à jour par la copie de 'classes' de l'étape n-1
        new_classes = []

        for c in classes:
            blocs = {} # pour chaque état de classe, on construit un set 'bloc' qui regroupe les états en fonction de leur signature
            for etat in c:
                # la signature d'un état est un tuple contenant les transitions sortantes vers d'autres classes
                signature = tuple( 
                    (lettre, next(
                        (i for i, p in enumerate(classes) if any(e == dest for e in p)), None))
                    for lettre in alphabet
                    for _, l, dest in old_transitions if _ == etat and l == lettre
                )
                # les états aux signatures identiques sont regroupés
                if signature not in blocs: 
                    blocs[signature] = []
                blocs[signature].append(etat)
            new_classes.extend(blocs.values())

        classes = new_classes # les nouvelles classes sont formées à partir de ces 'blocs.values()'

    # construction du nouvel automate
    etat_minimise = {etat: index for index, c in enumerate(classes) for etat in c} # dictionnaire qui associe chaque état à son nouvel indice de classe
    new_etats = classes
    new_transitions = []
    for init, lettre, dest in old_transitions:
        for c in classes:
            if init in c:
                new_init = c
            if dest in c:
                new_dest = c

        new_transition = [new_init, lettre, new_dest] # construction des transitions par les classes d'états
        if new_transition not in new_transitions:
            new_transitions.append(new_transition)
    
    new_I = []
    for c in classes:
        if any(item in c for item in automate["I"]): 
            new_I.append(c) # ajout de la classe contenant l'état initial de l'automate original

    dico_f = {} # dictionnaire qui associe chaque classe à ses états finaux
    for etat, classe in etat_minimise.items():
        if etat in etats_finaux: # on vérifie d'abord si l'état actuel est dans les états finaux d'origine
            if classe not in dico_f:
                dico_f[classe] = [] # création au préalable d'une liste vide pour éviter les erreurs
            dico_f[classe].append(etat)

    new_F = [etat for etat in dico_f.values()] # ajout des classes des états finaux

    return {
        "alphabet": alphabet,
        "etats": new_etats,
        "transitions": new_transitions,
        "I": new_I,
        "F": new_F
    }
        
if __name__ == '__main__':
    doctest.testmod()
