from formeNormalConjonctive import variable_vers_pos
from z3 import *
from time import *




def donner_solution():
    """
    Cette fonction donne la solution de l'ensemble de clause contenu dans le fichier
    'clauses.dimacs' en utilisant le sat solveur z3.
    Si il n'y a pas de solution, la fonction renvoie un dictionnaire vide sinon la fonction
    traduit et renvoie la solution donnée par z3 en un dictionnaire avec en clé la position 
    et en valeur le nombre à cette position.
    """

    s = Solver()
    s.from_file("clauses.dimacs")
    if(s.check() != sat):
        return []
    solution = s.model()
    pos_dict = {}
    for x in solution:
        if (solution[x] == True):
            (nombre, ligne, colone) = (variable_vers_pos(str(x).lstrip(' k!')))
            pos_dict[ligne, colone] = nombre

    return pos_dict
