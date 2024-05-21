import doctest
import copy
from determinisation import *

auto3 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',1],[0,'a',0],[1,'b',2],[1,'b',1]], "I":[0],"F":[2]}

def complet(automate: dict) -> bool:
    """
    Fonction complet qui étant donné un automate passé en paramètre renvoie
    True s’il est complet et False sinon.
    >>> print(complet(auto0))
    False
    >>> print(complet(auto1))
    True
    """
    for etat in automate["etats"]:
        for lettre in automate["alphabet"]:
            transition_trouvee = False # initialisation d'une variable de repère 
            for transition in automate["transitions"]: # pour chaque transition
                if transition[0] == etat and transition[1] == lettre: # s'il existe un état source et une lettre de la transition actuelle, 
                    transition_trouvee = True # on trouve une transition
                    break
            if not transition_trouvee: # transition non trouvé : il n'existe pas de transition pour un état src et une lettre (= non complet)
                return False
    return True

def complete(automate: dict) -> dict:
    """
    Fonction complete qui complète l’automate passé en paramètre en ajoutant
    un état puits.
    >>> print(complete(auto0))
    {'alphabet': ['a', 'b'], 'etats': [0, 1, 2, 3, 4], 'transitions': [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 3], [0, 'b', 4], [2, 'b', 4], [3, 'a', 4], [3, 'b', 4], [4, 'a', 4], [4, 'b', 4]], 'I': [0], 'F': [3]}
    """
    if complet(automate): # il n'est pas nécessaire d'exécuter le programme si l'automate est déjà complet
        return automate
        
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    etat_puits = sorted(automate["etats"])[len(automate_copy["etats"]) - 1] + 1 # ajout d'un état puits en respectant l'ordre des états
    automate_copy["etats"].append(etat_puits) 

    for etat in automate_copy["etats"]:
        for lettre in automate_copy["alphabet"]:
            transition_trouvee = False # initialisation d'une variable de repère 
            for transition in automate_copy["transitions"]: # pour chaque transition
                if transition[0] == etat and transition[1] == lettre: # s'il existe un état source et une lettre de la transition actuelle, 
                    transition_trouvee = True # on trouve une transition
                    break
            if not transition_trouvee:
                # transition non trouvé : ajout de la transition constitué de l'état source actuel, la lettre, et l'état puits
                automate_copy["transitions"].append([etat, lettre, etat_puits])
    return automate_copy

def complement(automate: dict) -> dict:
    """
    Fonction complement qui étant donné un automate passé en paramètre
    acceptant un langage L renvoie un automate acceptant le complement  ̄L. 
    >>> print(complement(auto3))
    {'alphabet': ['a', 'b'], 'etats': [0, 1, 2, 3], 'transitions': [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'b', 2], [0, 'b', 3], [2, 'a', 3], [3, 'a', 3], [3, 'b', 3]], 'I': [0], 'F': [0, 1, 3]}
    """
    automate_copy = copy.deepcopy(automate) # Création d'une copie de l'automate pour modifier seulement la copie
    # (Cours) Pour obtenir le complément : on déterminise, on complète puis on échange les états terminaux
    if not deterministe(automate_copy): # déterminiser l'automate si ce n'est pas la cas
        automate_copy = determinise(automate_copy)
        automate_copy = renommage(automate_copy) # permet de retourner un automate propre
    automate_copy = complete(automate_copy)
    automate_copy["F"] = [etat for etat in automate_copy["etats"] if etat not in automate_copy["F"]] # échange des états terminaux en excluant ceux actuels
    return automate_copy


if __name__ == '__main__':
    doctest.testmod()