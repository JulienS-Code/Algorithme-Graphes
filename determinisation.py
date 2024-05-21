import doctest

auto0 ={"alphabet":['a','b'],"etats": [0,1,2,3],
"transitions":[[0,'a',1],[1,'a',1],[1,'b',2],[2,'a',3]], "I":[0],"F":[3]}
auto1 ={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'b',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}
auto2={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'a',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}

def deterministe(automate: dict) -> bool:
    """
    Fonction deterministe qui étant donné un automate passé en paramètre
    renvoie True s’il est déterministe et False sinon.
    >>> print(deterministe(auto0))
    True
    >>> print(deterministe(auto2))
    False
    """
    save_transitions = {} # dictionnaire qui va sauvegarder les transitions ((état initial, lettre) : état dest)
    if len(automate["I"]) > 1: # l'automate doit avoir qu'un seul état initial
        return False
    for (etat, lettre, dest) in automate["transitions"]: # boucle sur toutes les transitions existantes de l'automate
        if (etat, lettre) in save_transitions: # si une transition par un même état init et lettre est déjà sauvegardé, l'automate n'est pas déterministe
            return False
        save_transitions[(etat, lettre)] = dest # On stocke notre transition dans notre dico
    return True

def determinise(automate: dict) -> dict:
    """
    Fonction determinise qui déterminise l’automate passé en paramètre.
    >>> print(determinise(auto2))
    {'alphabet': ['a', 'b'], 'etats': [[0], [0, 1], [1]], 'transitions': [[[0], 'a', [0, 1]], [[0, 1], 'a', [0, 1]], [[0, 1], 'b', [1]], [[1], 'a', [1]], [[1], 'b', [1]]], 'I': [[0]], 'F': [[0, 1], [1]]}
    """
    if deterministe(automate): # Vérification que notre automate est deterministe pour éviter de le determiniser
        return automate
    
    # initialisation des variables
    alphabet = automate['alphabet']
    transitions = automate['transitions']
    I = automate['I']
    F = automate['F']

    # Création d'un nouvel automates vide
    automate_det = {
        'alphabet': alphabet,
        'etats': [],
        'transitions': [],
        'I': [I],
        'F': []
    }

    # Utiliser une file pour explorer les états
    queue = list([I]) # file d'exploration des états, initialisée avec l'état initial 
    etat_map = {tuple(I): I} # dictionnaire pour mapper les tuples d'états aux états 

    while queue: # boucle sur les états à explorer
        etats_courants = queue.pop(0) # sauvegarde et suppression de la file de l'état de la boucle actuelle

        for lettre in alphabet: 
            next_etat = set()
            for etat in etats_courants:
                for (init, l, dest) in transitions: 
                    if init == etat and l == lettre: # s'il existe une transition avec l'état source actuel et la lettre, 
                        next_etat.add(dest) # on ajoute l'état destinaire 

            next_etat = sorted(next_etat) # on trie nos prochains états
            next_tuple = tuple(next_etat) # conversion en tuple pour faciliter les comparaisons
            
            if not next_etat: # on vérifie si nous avons un prochain état
                continue

            if next_tuple not in etat_map:   # si 'next_etat' n'a pas encore été rencontré on le sauvegarde
                etat_map[next_tuple] = next_etat 
                queue.append(next_etat) # on l'ajoute à la file pour l'explorer ensuite

            automate_det['transitions'].append([etats_courants, lettre, next_etat]) # On ajoute la transition existante à l'automate
        
    automate_det['etats'] = list(etat_map.values()) # tous les états rencontrés sont ajoutés à l'automate déterministe

    for new_etat in automate_det['etats']: 
        if any(etat_original in F for etat_original in new_etat): # On vérifie si au moins un état original inclus dans cet état est un état final
            automate_det['F'].append(new_etat) # On ajoute cet état à la liste des états finaux

    return automate_det

def renommage(automate: dict) -> dict:
    """
    Fonction renommage qui étant donné un automate passé en paramètre re-
    nomme ses états avec les premiers entiers.
    >>> print(renommage(determinise(auto2)))
    {'alphabet': ['a', 'b'], 'etats': [0, 1, 2], 'transitions': [[0, 'a', 1], [1, 'a', 1], [1, 'b', 2], [2, 'a', 2], [2, 'b', 2]], 'I': [0], 'F': [1, 2]}
    """
    old_etats = automate["etats"]
    new_etats = list(range(len(automate["etats"]))) # Création de nouveaux états numérotés de 0 à N-1 où N est le nombre total d'anciens états
    etats_map = dict(zip(new_etats, old_etats)) # création d'un dictionnaire qui associe chaque nouvel état en clé à son ancien état en valeur

    new_transitions = automate["transitions"] # On enregistre les transitions pour les modifier
    for i in range(len(new_transitions)): 
        for index, etat in etats_map.items():
            if new_transitions[i][0] == etat: # On vérifie que l'état source de la transition i est bien le même que l'état
                new_transitions[i][0] = index # On le modifie par son index (son nouvel état)
            if new_transitions[i][2] == etat: # On vérifie que l'état destination de la transition i est bien le même que l'état
                new_transitions[i][2] = index # On le modifie par son index (son nouvel état)
    
    new_etats_init = automate["I"] # On enregiste les états initiaux pour les modifier
    for i in range(len(new_etats_init)): 
        for index, etat in etats_map.items():
            if new_etats_init[i] == etat: # On vérifie que l'état initial i est bien le même que l'état
                new_etats_init[i] = index # On le modifie par son index (son nouvel état)

    new_etats_fin = automate["F"] # On enregiste les états finaux pour les modifier
    for i in range(len(new_etats_fin)): 
        for index, etat in etats_map.items():
            if new_etats_fin[i] == etat: # On vérifie que l'état finaux i est bien le même que l'état
                new_etats_fin[i] = index # On le modifie par son index (son nouvel état)
    
    automate["etats"] = new_etats # mise à jour des nouveaux états
    automate["transitions"] = new_transitions # mise à jour des nouvelles transitions
    return automate



if __name__ == '__main__':
    doctest.testmod()
