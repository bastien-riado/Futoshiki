
var_dict = {}
pos_dict = {}


def pos_vers_variable(pos):
    """
    Cette fonction regarde si le tuple contenant une position est dans le dictionnaire var_dict. 
    Si ce tuple n'est pas déjà présente, la fonction lui assigne une variable libre et renvoie cette variable.
    Si le tuple est déjà présent, la fonction renvoie alors la variable assignée auparavant.    
    """
    global var_dict
    if (pos not in var_dict):
        var_dict[pos] = str(len(var_dict) + 1)
    return var_dict[pos]


def variable_vers_pos(variable):
    """
    Cette fonction est l'inverse de la fonction pos_vers_variable(), elle renvoie la position associer a une variable
    assignée dans la fonction pos_vers_variable().
    """
    global var_dict
    return pos_dict[variable]

# transforme la position d'une grille contenant les signes en une position d'une grille avec seulement les nombres


def pos_grille_chiffre(i, j):
    if (i % 2 == 1):
        u = int((i-1)/2)
    else:
        u = int(i/2)
    if (j % 2 == 1):
        v = int((j-1)/2)
    else:
        v = int(j/2)
    return (u, v)


def creer_clause(nbLignes, f, grille):
    global var_dict
    var_dict = {}
    print('', file=f)

    # chaque nombre présent au moins 1 fois dans chaque Ligne
    for nombre in range(nbLignes):
        for ligne in range(nbLignes):
            for colonne in range(nbLignes):
                print(pos_vers_variable(
                    (nombre+1, ligne, colonne)), end=' ', file=f)
            print(' 0', file=f)

    # chaque nombre présent au moins 1 fois dans chaque Colonne
    for nombre in range(nbLignes):
        for ligne in range(nbLignes):
            for colonne in range(nbLignes):
                print(pos_vers_variable(
                    (nombre+1, colonne, ligne)), end=' ', file=f)
            print('0', file=f)

    # pas plus d'un nombre dans chaque case
    for ligne in range(nbLignes):
        for colonne in range(nbLignes):
            for nombre in range(nbLignes):
                for nombre2 in range(nombre+1, nbLignes):
                    print('-'+pos_vers_variable((nombre+1, ligne, colonne))+' -' +
                          pos_vers_variable((nombre2+1, ligne, colonne)) + ' 0', file=f)

    # pas plus d'un meme nombre dans chaque Ligne
    for nombre in range(nbLignes):
        for ligne in range(nbLignes):
            for colonne in range(nbLignes):
                for colonne2 in range(colonne+1, nbLignes):
                    print('-'+pos_vers_variable((nombre+1, ligne, colonne2))+' -' +
                          pos_vers_variable((nombre+1, ligne, colonne)) + ' 0', file=f)

    # pas plus d'un meme nombre dans chaque Colonne
    for nombre in range(nbLignes):
        for ligne in range(nbLignes):
            for colonne in range(nbLignes):
                for colonne2 in range(colonne+1, nbLignes):
                    print('-'+pos_vers_variable((nombre+1,
                          colonne2, ligne)), end=' ', file=f)
                    print('-'+pos_vers_variable((nombre+1,
                          colonne, ligne)), end=' ', file=f)
                    print('0', file=f)

    # ajout des nombres et inferieurs qui sont sur la grille a la base
    print(grille)

    for i in range(nbLignes*2-1):
        for j in range(nbLignes*2-1):

            (u, v) = pos_grille_chiffre(i, j)

            if (grille[i][j] not in ['┃', '━', '╋', '<', '>', 'ʌ', 'v', '0']):
                print(pos_vers_variable(
                    (int(grille[i][j]), u, v)) + ' 0', file=f)
            elif (grille[i][j] == '<'):
                for nombre1 in range(nbLignes):
                    for nombre2 in range(nombre1+1, nbLignes):
                        print('-' + pos_vers_variable((nombre2+1, u, v)) + ' -' +
                              pos_vers_variable((nombre1+1, u, v+1)) + ' 0', file=f)
            elif (grille[i][j] == '>'):
                for nombre1 in range(nbLignes):
                    for nombre2 in range(nombre1+1, nbLignes):
                        print('-' + pos_vers_variable((nombre1+1, u, v)) +
                              ' -' + pos_vers_variable((nombre2+1, u, v+1)) + ' 0', file=f)
            elif (grille[i][j] == 'ʌ'):
                for nombre1 in range(nbLignes):
                    for nombre2 in range(nombre1+1, nbLignes):
                        print('-' + pos_vers_variable((nombre2+1, u, v)) +
                              ' -' + pos_vers_variable((nombre1+1, u+1, v)) + ' 0', file=f)
            elif (grille[i][j] == 'v'):
                for nombre1 in range(nbLignes):
                    for nombre2 in range(nombre1+1, nbLignes):
                        print('-' + pos_vers_variable((nombre1+1, u, v)) + ' -' +
                              pos_vers_variable((nombre2+1, u+1, v)) + ' 0', file=f)

    # print(var_dict)

    global pos_dict
    pos_dict = dict((v, k) for k, v in var_dict.items())
