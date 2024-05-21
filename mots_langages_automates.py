import doctest
from itertools import product

######## 1.1 Mots ########

def pref(mot: str) -> list:
    """
    Fonction pref qui étant donné un mot u passé en paramètre renvoie la
    liste des préfixes de u.
    >>> print(pref("coucou"))
    ['', 'c', 'co', 'cou', 'couc', 'couco', 'coucou']
    """
    lst = []
    resultat = ""
    vide = ""
    lst.append(vide)
    for i in mot: # Pour chaque lettre du mot
        resultat += i # On ajoute la lettre i à notre resultat
        lst.append(resultat) # On ajoute notre résultat à notre liste (le résultat se verra grandir avec les lettres du mot, on ne le réinitialise pas)
    return lst

def suf(mot: str) -> list:
    """
    Fonction suf qui étant donné un mot u passé en paramètre renvoie la
    liste des suffixes de u.
    >>> print(suf("coucou"))
    ['coucou', 'oucou', 'ucou', 'cou', 'ou', 'u', '']
    """
    lst = [] 
    for i in range(len(mot), -1, -1): # On parcourt notre mot à l'envers
        resultat = mot[i:] # On ajoute les mots après notre i
        lst.append(resultat) # On ajoute notre résultat à notre liste (le résultat se verra grandir avec les lettres du mot, on ne le réinitialise pas)
    lst.reverse() # On inverse la liste pour qu'elle soit dans le bon sens
    return lst

def fact(mot: str) ->list:
    """
    Fonction fact qui étant donné un mot u passé en paramètre renvoie la
    liste sans doublons des facteurs de u.
    >>> print(fact("coucou"))
    ['', 'c', 'co', 'cou', 'couc', 'couco', 'coucou', 'o', 'ou', 'ouc', 'ouco', 'oucou', 'u', 'uc', 'uco', 'ucou']
    """
    set_fact = set() 
    size = len(mot)
    for i in range(size): # On parcours la taille du mot
        for j in range(i, size + 1): # On parcours tous les indices possibles
            set_fact.add(mot[i:j]) # On ajoute la sous-chaine à notre set
    lst = sorted(set_fact) # On trie nos éléments
    return lst

def miroir(mot: str) -> list:
    """
    Fonction miroir qui étant donné un mot u passé en paramètre renvoie le
    mot miroir de u.
    >>> print(miroir("coucou"))
    uocuoc
    """
    return mot[::-1] # inversion du mot

######## 1.2 Langages ########

def concatene(L1: list, L2: list) -> list:
    """
    Fonction concatene qui étant donnés deux langages L1 et L2 renvoie le
    produit de concaténation (sans doublons) de L1 et L2.
    >>> L1=['aa','ab','ba','bb']
    >>> L2=['a', 'b', '']
    >>> print(concatene(L1,L2))
    ['aaa', 'aab', 'aa', 'aba', 'abb', 'ab', 'baa', 'bab', 'ba', 'bba', 'bbb', 'bb']
    """
    lst = []
    for i in L1 : # On parcourt les mots de L1
        for j in L2: # On parcourt les mots de L2
            fusion = i + j # concaténation des deux mots
            if fusion not in lst: # On vérifie qu'il n'est pas déja dans nôtre liste
                lst.append(fusion)
    return lst

def puis(L1: list, n: int) -> list:
    """
    Fonction puis qui étant donnés un langage L et un entier n renvoie le
    langage Ln(sans doublons).
    >>> L1 = ['aa','ab','ba','bb']
    >>> print(puis(L1,2))
    ['aaaa', 'aaab', 'aaba', 'aabb', 'abaa', 'abab', 'abba', 'abbb', 'baaa', 'baab', 'baba', 'babb', 'bbaa', 'bbab', 'bbba', 'bbbb']
    """
    set_puis = {''.join(comb) for comb in product(L1, repeat=n)} # on génère toutes les combinaisons possible de longueur n
    result = sorted(set_puis) # on trie dans l'ordre alphabétique
    return result       

# 1.2.3 : L'étoile d'un langage est de taille infinit, impossible donc à représenter

def tousmots(A: list, n: int) -> list: 
    """
    Fonction tousmots qui étant donné un alphabet A passé en paramètre
    renvoie la liste de tous les mots de A∗ de longueur inférieure à n.
    >>> print(tousmots(['a','b'],3))
    ['a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb', '']
    """
    lst = []
    for lenght in range(1, n + 1):
        for p in product(A, repeat=lenght): # On parcourt toutes les combinaisons de longueur lenght possibles
            lst.append(''.join(p)) # On les ajoute à la liste
    lst.append('') # ajout du mot vide prit en compte
    return lst

######## 1.3 Automates ########

def defauto():
    """
    Fonction defauto qui permet de faire la saisie `depuis la console` d’un automate (sans doublon).
    """
    # Création d'un automate vide
    auto = {"alphabet": [],
            "etats": [], 
            "transitions": [],
            "I": [],
            "F": []} 
    alphabet = input("Entrez l'alphabet de l'automate (séparé par des espaces): ").split() 
    auto["alphabet"] = list(set(alphabet)) # liste d'un set pour éviter les doublons

    nb_etats = int(input("Entrez le nombre total d'états : "))
    # auto["etats"] = list(range(nb_etats)) # Création des états de O à N où N est le nombre d'états
    auto["etats"] = list(range(1, nb_etats + 1)) # pour des états commençant par 1

    print("Saisie des transitions")
    while True: # permet de boucle jusqu'à coupure par l'utilisateur
        etat = int(input("Entrez l'état initial de la transition (-1 pour terminer): "))
        if etat == -1: # l'utilisateur quitte la boucle
            break
        if etat not in auto["etats"]: # on vérifie si l'état est valide (présent dans la liste d'états)
            print("Etat initial invalide, retranscrire la transition.")
            continue
        
        lettre = input("Entrez la lettre de la transition : ")
        if lettre not in auto["alphabet"]: # on vérifie si la lettre est valide (présente dans l'alphabet)
            print("Lettre invalide, veuillez retranscrire la transition.")
            continue

        dest = int(input("Entrez l'état final de la transition : "))
        if dest not in auto["etats"]: # on vérifie si l'état est valide (présent dans la liste d'états)
            print("Etat invalide, veuillez retranscrire la transition.")
            continue

        auto["transitions"].append([etat, lettre, dest]) # on créer la transition 
    
    while True: 
        etats_init = input("Entrez les états initiaux de l'automate (séparés par des espaces): ").split()
        etats_init = set(map(int, etats_init)) # Création d'un set d'entiers pour les états initiaux
        if etats_init.issubset(auto["etats"]): # si les états initiaux sont tous inclus dans la liste d'états,
            auto["I"] = list(etats_init) # on ajoute la liste d'états_init dans auto["I"]
            break
        else:
            print("Certains états initiaux ne sont pas valides, veuillez réessayez.")

    while True:
        etats_fin = input("Entrez les états finaux de l'automate (séparés par des espaces): ").split()
        etats_fin = set(map(int, etats_fin)) # Création d'un set d'entiers pour les états finaux
        if etats_fin.issubset(auto["etats"]): # si les états finaux sont tous inclus dans la liste d'états,
            auto["F"] = list(etats_fin) # on ajoute la liste d'états_init dans auto["F"]
            break
        else:
            print("Certains états finaux ne sont pas valides, veuillez réessayez.")

    return auto
    

auto = {"alphabet":['a','b'],"etats": [1,2,3,4],"transitions":[[1,'a',2],[2,'a',2],[2,'b',3],[3,'a',4]],"I":[1],"F":[4]}


def defauto2(alphabet: list, etats: list, transitions: list, I: list, F: list) -> dict:
    """
    Fonction defauto qui permet de faire la saisie d’un automate (sans doublon). Elle
    prend en paramètre un alphabet, une liste états, une liste de transitions, une liste d'états 
    initiaux, une liste d'états finaux et retourne un automate sous forme de dictionnaire.
    """
    return {
        "alphabet": alphabet,
        "etats": etats,
        "transitions": transitions,
        "I": I,
        "F": F
    }


def lirelettre(T: list, E: list, lettre: str ) -> list:
    """
    Fonction lirelettre qui étant donnés en paramètres une liste de transitions T, 
    une liste d’états E et une lettre a, renvoie la liste des états dans lesquels on peut
    arriver en partant d’un état de E et en lisant la lettre a.
    >>> print(lirelettre(auto["transitions"],auto["etats"],'a'))
    [2, 4]
    """
    lst=[]
    for i in T:
        if i[0] in E and i[1] == lettre and i[2] not in lst: # s'il existe un état source, par lequel on peut lire la lettre en paramètre et arrivé sur un état dest non enregistré 
            lst.append(i[2]) # on ajoute la destination à notre liste
    return lst

def liremot(T: list, E: list, mot: str) -> list :
    """
    Fonction liremot qui étant donnés en paramètres une liste de transitions
    T, une liste d’états E et un mot m, renvoie la liste des états dans lesquels on peut arriver
    en partant d’un état de E et en lisant le mot m.
    >>> print(liremot(auto["transitions"],auto["etats"],'aba'))
    [4]
    """
    lst = list(E)  
    for lettre in mot:
        sauvegarde = []  
        for transition in T:
            if transition[1] == lettre and transition[0] in lst: # s'il existe une transition d'un état source compris dans E par lequel on peut lire la lettre du mot en paramètre
                sauvegarde.append(transition[2]) # on ajoute la destination à notre liste
        lst = sauvegarde  # On mets à jour
    return lst

def accepte(automate: dict, m: str) -> bool:
    """
    Fonction accepte qui prend en paramètres un automate et un mot m et
    renvoie True si le mot m est accepté par l’automate.
    >>> print(accepte(auto, "aaaba"))
    True
    >>> print(accepte(auto, "b"))
    False
    """
    etats_courants = set(automate["I"]) # On crée une copie de tout nos états initiaux
    for lettre in m:
        if lettre not in auto["alphabet"]: # si la lettre n'est pas dans l'alphabet, s'arrêter là car le mot est refusé
            return False
        next_etat = set() # Création d'un set des prochains états possibles
        for (init, l, dest) in automate["transitions"]: 
            if init in etats_courants and l == lettre: # s'il existe une transition avec un des états courants en source et la lettre actuelle du mot, 
                next_etat.add(dest) # on ajoute la destinationn pour poursuivre le chemin
        etats_courants = next_etat # On mets à jour les états explorer sur lesquels on peut repartir
    return any(etat in automate["F"] for etat in etats_courants) # Vérifie si au moins un des états actuels est un état final 


def generer_mots(alphabet, longueur):
    """
    Fonction qui prend en paramètre un alphabet et une longueur et renvoie 
    tous les mots possibles de taille inférieur ou égale à la longueur
    """
    if longueur == 0:
        return [""]
    mots = generer_mots(alphabet, longueur - 1) # On rappelle la même fonction mais de longueur -1
    return [mot + lettre for mot in mots for lettre in alphabet] # Génère une liste de toutes les combinaisons possibles en ajoutant chaque lettre de l'alphabet à chaque mot dans la liste de mots donnée

def langage_accept(automate: dict, n: int) -> list:
    """
    Fonction langage_accept qui prend en paramètres un automate et un
    entier n et renvoie la liste des mots de longueur inférieure à n acceptés par l’automate.
    >>> print(langage_accept(auto, 3))
    ['aba']
    >>> print(langage_accept(auto, 2))
    []
    >>> print(langage_accept(auto, 4))
    ['aba', 'aaba']
    """
    mots_acceptes = []
    for longueur in range(1, n + 1):
        mots = generer_mots(automate["alphabet"], longueur) # On appelle la fonction generer_mot
        for mot in mots:
            if accepte(automate, mot): # Vérification que l'automate accepte le mot
                mots_acceptes.append(mot)
    return mots_acceptes

# 1.3.6 On ne peut pas faire de fonction qui renvoie le langage accepté par un automate
# car il pourrait être infinit (exemple avec A*)
            

if __name__ == '__main__':
    doctest.testmod()
