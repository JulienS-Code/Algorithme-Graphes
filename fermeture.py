import doctest
import copy
from mots_langages_automates import auto


auto_test = {"alphabet":['a','b'],"etats": [1,2,3,4],
"transitions":[[1,'a',2],[2,'b',2],[2,'a',4],[3,'b',2]], "I":[1],"F":[4]}

def accessible(automate: dict) -> bool:
    """
    Fonction qui prend en paramètre un automate et renvoi True s'il est accessible,
    et False sinon.
    >>> print(accessible(auto))
    True
    >>> print(accessible(auto_test))
    False
    """
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    etats_a_visiter = automate_copy["I"]
    etats_visites = set(automate_copy["I"])

    while etats_a_visiter: # boucle sur les états à visités s'il y en reste
        etats_a_visiter.pop(0) # supprimer l'état dont la boucle à commencer
        for transition in automate_copy["transitions"]:
            next_etat = transition[2] # enregistre l'état destinataire
            if next_etat not in etats_visites:
                etats_visites.add(next_etat)
                etats_a_visiter.append(next_etat) # ajoute l'état à vérifier dans la boucle

    # si tous les états de l'automate ont été visités, return True (méthode issubset)
    return set(automate_copy["etats"]).issubset(etats_visites)

auto_test2 = {"alphabet":['a','b'], "etats": [1,2,3,4], 
"transitions":[[1,'a',2],[2,'b',2],[2,'a',4],[2,'b',3]], "I":[1], "F":[4]}

def coaccessible(automate: dict) -> bool:
    """
    Fonction qui prend en paramètre un automate et renvoi True s'il est coaccessible, 
    et False sinon.
    >>> print(coaccessible(auto_test2))
    False
    >>> print(coaccessible(auto))
    True
    """
    transitions_inversees = []
    for (init, lettre, dest) in automate["transitions"]:
        transitions_inversees.append([dest, lettre, init]) # inversion du sens de la transition (source en destinaire et inversement)

    automate_inverse = {
        "alphabet": automate["alphabet"],
        "etats": automate["etats"],
        "transitions": transitions_inversees,
        "I": automate["F"],
        "F": automate["I"]
    }
    # être coaccessible peut être traduit par une inversion des transitions, des états initiaux et finaux, 
    # puis de voir s'il est accessible
    return accessible(automate_inverse) 

auto_emonde = {"alphabet":['a','b'],"etats": [1,2,3],"transitions":[[1,'a',2],[1,'b',1],[2,'a',2],[2,'b',3],[3,'a',2],[3,'b',1]],"I":[1],"F":[3]}

def emonde(automate: dict) -> bool:
    """
    Fonction qui prend en paramètre un automate et renvoi True s'il est émondé, c'est-à-dire
    accessible et coaccessible, et False sinon.
    >>> print(emonde(auto_emonde))
    True
    >>> print(emonde(auto_test))
    False
    >>> print(emonde(auto_test2))
    False
    """
    return accessible(automate) and coaccessible(automate) # définition d'émondé : l'automate est émondé s'il est accessible et coaccessible

def prefixe(automate: dict) -> dict:
    """
    Fonction prefixe qui étant donné un automate émondé acceptant L renvoie
    un automate acceptant l’ensemble des préfixes des mots de L.
    >>> print(prefixe(auto_emonde))
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3], 'transitions': [[1, 'a', 2], [1, 'b', 1], [2, 'a', 2], [2, 'b', 3], [3, 'a', 2], [3, 'b', 1]], 'I': [1], 'F': [1, 2, 3]}
    """
    if not emonde(automate): # l'automate doit être émondé
        assert("Automate non émondé")

    # il suffit d'avoir le même automate et tous les états en finaux
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    for etat in automate_copy["etats"]:
        if etat not in automate_copy["F"]: # évite d'ajouter les états déjà présents
            automate_copy["F"].append(etat)
    automate_copy["F"].sort() 
    return automate_copy


def suffixe(automate: dict) -> dict:
    """
    Fonction suffixe qui étant donné un automate émondé acceptant Lrenvoie
    un automate acceptant l’ensemble des suffixes des mots de L.
    >>> print(suffixe(auto_emonde))
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3], 'transitions': [[1, 'a', 2], [1, 'b', 1], [2, 'a', 2], [2, 'b', 3], [3, 'a', 2], [3, 'b', 1]], 'I': [1, 2, 3], 'F': [3]}
    """
    if not emonde(automate): # l'automate doit être émondé
        assert("Automate non émondé")
    
    # il suffit d'avoir le même automate et tous les états en initiaux
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    for etat in automate_copy["etats"]:
        if etat not in automate_copy["I"]: # évite d'ajouter les états déjà présents
            automate_copy["I"].append(etat)
    automate_copy["I"].sort()
    return automate_copy

def facteur(automate: dict) -> dict:
    """
    Fonction facteur qui étant donné un automate émondé acceptant L renvoie
    un automate acceptant l’ensemble des facteurs des mots de L.
    >>> print(facteur(auto_emonde))
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3], 'transitions': [[1, 'a', 2], [1, 'b', 1], [2, 'a', 2], [2, 'b', 3], [3, 'a', 2], [3, 'b', 1]], 'I': [1, 2, 3], 'F': [1, 2, 3]}
    """
    if not emonde(automate): # l'automate doit être émondé
        assert("Automate non émondé")
    
    # il suffit d'avoir le même automate et tous les états en initiaux et en finaux
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    auto_pref = prefixe(automate_copy)
    auto_suff = suffixe(auto_pref)
    return auto_suff

def miroir(automate: dict) -> dict:
    """
    Fonction miroir qui étant donné un automate émondé acceptant Lrenvoie
    un automate acceptant l’ensemble des miroirs des mots de L.
    >>> print(miroir(auto_emonde))
    {'alphabet': ['a', 'b'], 'etats': [1, 2, 3], 'transitions': [[2, 'a', 1], [1, 'b', 1], [2, 'a', 2], [3, 'b', 2], [2, 'a', 3], [1, 'b', 3]], 'I': [3], 'F': [1]}
    """
    if not emonde(automate): # l'automate doit être émondé
        assert("Automate non émondé")

    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    # il suffit d'avoir le même automate, d'inverser les états initiaux et terminaux ainsi que le sens des transitions
    temp = automate_copy["I"] # stockage des données dans une variable temporaire 
    automate_copy["I"] = automate_copy["F"]
    automate_copy["F"] = temp

    for i in range(len(automate["transitions"])):
        automate_copy["transitions"][i][0] = automate["transitions"][i][2] # inversion des états init en dest
        automate_copy["transitions"][i][2] = automate["transitions"][i][0] # inversion des états dest en init
        
    return automate_copy

if __name__ == '__main__':
    doctest.testmod()
