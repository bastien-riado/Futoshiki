
def lire_grille_fichier(fichier):
    grille = []
    taille = int(fichier.readline().rstrip())
    for index_colone in range(taille*2-1):
        grille.append(fichier.readline().rstrip().split(" "))
    return (grille, taille)


def ecrire_grille_fichier(fichier, grille, taille):
    # print(grille)
    print(taille, file=fichier)
    for ligne in grille:
        for case in ligne:
            print(case, file=fichier, end=' ')
        print('', file=fichier)
