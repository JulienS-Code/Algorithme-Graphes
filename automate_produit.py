import doctest
from determinisation import *
from complémentation import *

auto4 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',1],[1,'b',2],[2,'b',2],[2,'a',2]], "I":[0],"F":[2]}
auto5 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',2],[2,'a',2],[2,'b',0]],
"I":[0],"F":[0,1]}


def inter(automate1: dict, automate2: dict) -> dict:
    """
    Fonction inter qui étant donnés deux automates déterministes passés
    en paramètres acceptant respectivement les langages L1 et L2, renvoie l’automate produit
    acceptant l’intersection L1 ∩ L2.
    >>> print(inter(auto4,auto5))
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (1, 0), (2, 1), (2, 2), (2, 0)], 'transitions': [[(0, 0), 'a', (1, 0)], [(1, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)]], 'I': [(0, 0)], 'F': [(2, 0), (2, 1)]}
    """
    if not deterministe(automate1) or not deterministe(automate2): # les automates doivent être déterministes
        assert("Un ou les automates ne sont pas déterministes")
    elif automate1["alphabet"] != automate2["alphabet"]: # l'alphabet des deux automates doit être le même
        assert("Les automates n'ont pas le mêmes alphabet")

    # initialisation des variables
    transitions1 = automate1["transitions"]
    transitions2 = automate2["transitions"]
    alphabet = automate1["alphabet"]
    etats_initiaux = (automate1["I"][0], automate2["I"][0]) # paire des états initiaux de chaque automate
    news_etats = [etats_initiaux] # liste des nouveaux états de l'automate produit, initialisé avec l'état initial
    new_transitions = []
    visited = set() # ensemble des états visités pour éviter les répétitions dans la recherche

    # parcours BFS (Breadth First Search) qui explore un graphe de noeuds en noeuds depuis le noeud racine
    queue = [etats_initiaux] # file du parcours en largeur avec l'état initial
    while queue:
        etat_courrant = queue.pop(0) # sauvegarde et suppression de la file de l'état de la boucle actuelle
        visited.add(etat_courrant)
        etat1, etat2 = etat_courrant

        for lettre in alphabet:
            # on cherche les états suivants dans les transitions des automates d'origine pour chaque lettre de l'alphabet, None sinon
            next_etat1 = next((dest for (init, l1, dest) in transitions1 if init == etat1 and l1 == lettre), None)
            next_etat2 = next((dest for (init, l2, dest) in transitions2 if init == etat2 and l2 == lettre), None)

            if next_etat1 is not None and next_etat2 is not None:
                next_etats = (next_etat1, next_etat2) # état produit de la paire des deux états pour la même lettre de transition
                if next_etats not in news_etats:
                    news_etats.append(next_etats)
                new_transitions.append([etat_courrant, lettre, next_etats])
                if next_etats not in visited:
                    queue.append(next_etats)

    new_etats_fin = [etat for etat in news_etats if etat[0] in automate1["F"] and etat[1] in automate2["F"]] # états produit (le ET s'applique sur les états finaux des deux automates)
    new_etats_fin.sort() 
    
    return {
        "alphabet": alphabet,
        "etats": news_etats,
        "transitions": new_transitions,
        "I": [etats_initiaux],
        "F": new_etats_fin
    }


def difference(automate1: dict, automate2: dict) -> dict:
    """
    Fonction difference qui étant donnés deux automates déterministes
    passés en paramètres acceptant respectivement les langages L1 et L2, renvoie l’automate
    produit acceptant la difference L1\L2. 
    >>> print(difference(auto4, auto5))
    {'alphabet': ['a', 'b'], 'etats': [(0, 0), (3, 1), (3, 2), (3, 0), (1, 0), (2, 1), (2, 2), (2, 0)], 'transitions': [[(0, 0), 'a', (1, 0)], [(0, 0), 'b', (3, 1)], [(3, 1), 'a', (3, 1)], [(3, 1), 'b', (3, 2)], [(3, 2), 'a', (3, 2)], [(3, 2), 'b', (3, 0)], [(3, 0), 'a', (3, 0)], [(3, 0), 'b',(3, 1)], [(1, 0), 'a', (3, 0)], [(1, 0), 'b', (2, 1)], [(2, 1), 'a', (2, 1)], [(2, 1), 'b', (2, 2)], [(2, 2), 'a', (2, 2)], [(2, 2), 'b', (2, 0)], [(2, 0), 'a', (2, 0)], [(2, 0), 'b', (2, 1)]], 'I': [(0, 0)], 'F': [(2, 2)]}
    >>> print(renommage(difference(auto4,auto5)))
    {'alphabet': ['a', 'b'], 'etats': [0, 1, 2, 3, 4, 5, 6, 7], 'transitions': [[0, 'a', 4], [0, 'b', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 3], [3, 'a', 3], [3, 'b', 1], [4, 'a', 3], [4, 'b', 5], [5, 'a', 5], [5, 'b', 6], [6, 'a', 6], [6, 'b', 7], [7, 'a', 7], [7, 'b', 5]], 'I': [0], 'F': [6]}
    """
    if not deterministe(automate1) or not deterministe(automate2): # les automates doivent être déterministe
        assert("Un ou les automates ne sont pas déterministes")
    elif automate1["alphabet"] != automate2["alphabet"]: # les automates doivent avoir le même alphabet
        assert("Les automates n'ont pas le mêmes alphabet")
    
    # la différence L1\L2 est équivalente à L1 ∩ L2(barre), où L2(barre) est le complément de L2
    automate1_copy = complete(automate1)
    automate2_copy = complete(automate2)
    automate2_complement = complement(automate2_copy)
    resultat = inter(automate1_copy, automate2_complement)
    return resultat

if __name__ == '__main__':
    doctest.testmod()
