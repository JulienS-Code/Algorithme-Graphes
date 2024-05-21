from mots_langages_automates import *
from determinisation import *
from complémentation import *
from automate_produit import *
from fermeture import *
from minimisation import *

#### Automates de tests ####

auto0 ={"alphabet":['a','b'],"etats": [0,1,2,3],
"transitions":[[0,'a',1],[1,'a',1],[1,'b',2],[2,'a',3]], "I":[0],"F":[3]}

auto1 ={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'b',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}

auto2={"alphabet":['a','b'],"etats": [0,1],
"transitions":[[0,'a',0],[0,'a',1],[1,'b',1],[1,'a',1]], "I":[0],"F":[1]}

auto3 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',1],[0,'a',0],[1,'b',2],[1,'b',1]], "I":[0],"F":[2]}

auto4 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',1],[1,'b',2],[2,'b',2],[2,'a',2]], "I":[0],"F":[2]}

auto5 ={"alphabet":['a','b'],"etats": [0,1,2],
"transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',2],[2,'a',2],[2,'b',0]],
"I":[0],"F":[0,1]}

auto6 ={"alphabet":['a','b'],"etats": [0,1,2,3,4,5],
"transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],[3,'a',1],[3,'b',0],
[4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]], "I":[0],"F":[0,1,2,5]}

auto_test = {"alphabet":['a','b'],"etats": [1,2,3,4],
"transitions":[[1,'a',2],[2,'b',2],[2,'a',4],[3,'b',2]], "I":[1],"F":[4]}

auto_test2 = {"alphabet":['a','b'], "etats": [1,2,3,4], 
"transitions":[[1,'a',2],[2,'b',2],[2,'a',4],[2,'b',3]], "I":[1], "F":[4]}

auto_emonde = {"alphabet":['a','b'],"etats": [1,2,3],
"transitions":[[1,'a',2],[1,'b',1],[2,'a',2],[2,'b',3],[3,'a',2],[3,'b',1]],"I":[1],"F":[3]}

auto_exo4 = {"alphabet":['a','b'],"etats": [0,1,2,3,4,5,6,7],
"transitions":[[0, 'a', 1], [0, 'b', 2], [1, 'a', 3], [1, 'b', 1], [2, 'a', 4], [2, 'b', 2], [3, 'a', 5], 
[3, 'b', 3], [4, 'a', 2], [4, 'b', 4], [5, 'a', 6], [5, 'b', 1], [6, 'a', 7], [6, 'b', 2], [7, 'a', 6], [7, 'b', 7]],
"I":[0],"F":[1,2,3,6]}


#### Variables disponibles ####

## Alphabet ##
ab = ['a', 'b']
abc = ['a', 'b', 'c']

## Etats ##
etat_nb3 = [0, 1, 2]
etat_nb4 = [0, 1, 2, 3]
etat_nb5 = [0, 1, 2, 3, 4]



if __name__ == '__main__':

    #### Test à réaliser durant la soutenance si besoin ####

    # print(auto_exo4)

    automate_min_exo4 = minimise(auto_exo4)
    # print(automate_min_exo4)

    pass