from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from functools import partial
import sys
from formeNormalConjonctive import *
from SatSolveur import *
from grilleFichier import *

taille = 0

grille = []
variable = []
choices = []
frame_canvas = 0

style = 0


def fermer(fenetre):
    fenetre.destroy()


def remplacer_boutton_grille(root):
    global frame_canvas, taille, variable, choices, style
    if frame_canvas != 0:
        frame_canvas.destroy()

    frame_canvas = Frame(root)
    frame_canvas.pack(side='bottom', fill='both', expand=1)
    grid_canvas = Canvas(frame_canvas)
    grid_canvas.configure(borderwidth=0)
    grid_canvas.pack(expand=1)
    grid_canvas.configure(bg='#535353', borderwidth=0, highlightthickness=0)

    style.configure('A.TMenubutton', font=('calibri', int(20/(taille/7)), 'bold'),
                    foreground="green", background="#636363", relief='flat', sticky='news')
    style.configure('B.TMenubutton', font=('calibri', int(20/(taille/7)), 'bold'),
                    foreground="blue", background="#636363", relief='flat', sticky='news')

    for i in range(taille * 2 - 1):
        for j in range(taille * 2 - 1):
            print(variable[i][j].get())
            if ((i % 2 == 1) and (j % 2 == 1)):
                box = Label(
                    grid_canvas, text=' ')
            else:
                if ((i % 2 == 0) and (j % 2 == 1)):
                    box = OptionMenu(
                        grid_canvas, variable[i][j], *choices[1], style="B.TMenubutton")
                elif ((i % 2 == 1) and (j % 2 == 0)):
                    box = OptionMenu(
                        grid_canvas, variable[i][j], *choices[2], style="B.TMenubutton")
                else:
                    box = OptionMenu(
                        grid_canvas, variable[i][j], *choices[0], style="A.TMenubutton")
                box.grid(row=i, column=j, sticky='ewns',
                         pady=(2.5, 2.5), padx=(2.5, 2.5))
            box.config(cursor='xterm')


def initialiser_grille(root, taille):
    global variable, choices, grille

    variable = []

    choices = [[0] + [x for x in range(taille+1)],
               ['┃', '┃', '<', '>'],
               ['━', '━', 'v', 'ʌ']]

    for i in range(taille * 2 - 1):
        ligne = []
        for j in range(taille * 2 - 1):
            temp = StringVar(root)
            if ((i % 2 == 1) and (j % 2 == 1)):
                temp.set('╋')
            elif ((i % 2 == 0) and (j % 2 == 1)):
                temp.set(choices[1][0])
            elif ((i % 2 == 1) and (j % 2 == 0)):
                temp.set(choices[2][0])
            else:
                temp.set(choices[0][0])
            ligne.append(temp)
        variable.append(ligne)
    grille = update_grille()

    remplacer_boutton_grille(root)


def charger_grille(root, IntSize):
    global variable, taille, choices

    nom_fichier = filedialog.askopenfilename(
        defaultextension='.txt', filetypes=[("Fichier Texte", "*.txt")])
    print('Ouverture du fichier : ' + nom_fichier)
    fichier = open(nom_fichier, 'r', encoding="utf-8")
    (grille_sauvegarder, taille) = lire_grille_fichier(fichier)
    fichier.close()

    IntSize.set(taille)

    print(grille_sauvegarder)

    choices = [[0] + [x for x in range(taille+1)],
               [0, '┃', '<', '>'],
               [0, '━', 'v', 'ʌ']]

    variable = []

    for i in range(taille * 2 - 1):
        ligne = []
        for j in range(taille * 2 - 1):
            temp = StringVar(root)
            temp.set(grille_sauvegarder[i][j])
            ligne.append(temp)
        variable.append(ligne)

    remplacer_boutton_grille(root)


def sauvegarder_grille():
    global grille, taille
    grille = update_grille()
    nom_fichier = filedialog.asksaveasfilename(
        defaultextension='.txt', filetypes=[("Fichier Texte", "*.txt")])
    print('Grille sauivegarder dans le fichier : ' + nom_fichier)
    fichier = open(nom_fichier, 'w', encoding="utf-8")
    ecrire_grille_fichier(fichier, grille, taille)
    fichier.close()


def afficher_nouvelle_grille(IntSize, root):
    global taille
    taille = (IntSize.get())
    print("Création d'une nouvelle grille de taille " + str(taille))
    initialiser_grille(root, taille)


def main():

    global style

    root = Tk()
    root.title("Grille")
    root.configure(bg="#535353")

####################
    style = Style(master=root)

    style.configure('TButton', font=('calibri', 20, 'bold'),
                    foreground="black", background="#535353")

    style.map("TButton",
              foreground=[('active', 'black'), ('pressed', 'white')],
              background=[('pressed', 'black'),
                          ('active', '#535353')])

    style.configure('TLabel', font=('calibri', 20, 'bold'),
                    foreground="white", background="#535353")

    style.configure('TMenubutton', font=('calibri', 20, 'bold'),
                    foreground="white", background="#636363")

    style.configure('TFrame', background="#333333")

####################

    boutton_canvas = Canvas(root)
    boutton_canvas.pack(fill='both')
    boutton_canvas.configure(bg='#535353', borderwidth=0, highlightthickness=0)

    IntSize = IntVar(root)
    txt = Label(
        boutton_canvas, text='Taille de la grille : ')
    IntSize.set(5)

    verifier = Button(boutton_canvas,
                      text='Verifier', command=print_cnf)
    verifier.pack(side='left')

    sauvegarder = Button(boutton_canvas,
                         text='Enregistrer', command=sauvegarder_grille)
    sauvegarder.pack(side='left')

    charger = Button(boutton_canvas,
                     text='Charger', command=partial(charger_grille, root, IntSize))
    charger.pack(side='left')

    quitter = Button(boutton_canvas,
                     text='Quitter', command=partial(fermer, root))
    quitter.pack(side='left')

    txt.pack(side='left')
    box = OptionMenu(
        boutton_canvas, IntSize, *[x for x in range(14)], style='TMenubutton')
    box.pack(side='left')

    valider = Button(boutton_canvas, text='Générer', command=partial(
        afficher_nouvelle_grille, IntSize, root))
    valider.pack(side='left')

    afficher_nouvelle_grille(IntSize, root)

    root.mainloop()


def afficher_solution(solution, grille):
    solutionW = Tk()
    solutionW.title("Solution")
    solutionW.configure(bg="#535353")

####################

    style = Style(master=solutionW)

    style.configure('TLabel', font=('calibri', 20, 'bold'),
                    foreground="white", background="#535353", width=1, pady=(0.25, 0.25), padx=(0.25, 0.25))

####################

    if solution == []:
        box = Label(
            solutionW, text="⊥")
        box.pack()
        return
    box = Label(
        solutionW, text=" Solution :")
    box.pack(fill='both')
    canvas = Canvas(solutionW)
    canvas.pack(side='bottom', expand=1)

    style.configure('A.TLabel', font=('calibri', int(20/(len(grille)/15)), 'bold'),
                    foreground="green", background="#535353", width=1, pady=(0.25, 0.25), padx=(0.25, 0.25))
    style.configure('B.TLabel', font=('calibri', int(20/(len(grille)/15)), 'bold'),
                    foreground="#333333", background="#535353", width=1, pady=(0.25, 0.25), padx=(0.25, 0.25))

    for i in range(len(grille)):
        for j in range(len(grille)):
            u = int(i/2)
            v = int(j/2)
            if (((u, v) in solution) and (i % 2 == 0) and (j % 2 == 0) and grille[i][j] == '0'):
                box = Label(
                    canvas, text=solution[(u, v)], style='A.TLabel')
            elif grille[i][j] in ['━', '┃', '╋']:
                box = Label(
                    canvas, text=' ', style='B.TLabel')
            else:
                box = Label(
                    canvas, text=grille[i][j], style='B.TLabel')
            box.grid(row=i, column=j)


def update_grille():
    global grille, variable
    grille = []
    for i in range(len(variable)):
        ligne = []
        for j in range(len(variable)):
            ligne.append(variable[i][j].get())
        grille.append(ligne)
    return grille


def print_cnf():
    global taille, variable, grille
    grille = update_grille()
    nom_fichier = "clauses.dimacs"

    with open(nom_fichier, 'w', encoding="utf-8") as f:
        creer_clause(taille, f, grille)

    with open(nom_fichier, 'r') as fichier:
        liste_lignes = fichier.readlines()
        liste_lignes[0] = ("p cnf " + str(taille**3) + " " +
                           str(len(liste_lignes)-1) + "\n")

    with open(nom_fichier, 'w') as fichier:
        fichier.writelines(liste_lignes)
        fichier.close
    solution = donner_solution()
    afficher_solution(solution, grille)


main()
