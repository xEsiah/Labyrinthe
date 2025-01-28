from tkinter import *
from dicCoffres import dictionnaire_coffres
from dicPieges import dictionnaire_pieges
import random

''' FONCTIONS '''

def InterfaceLabyrinthe():
    # Fenetre principale 
    fenetre = Tk()
    fenetre.attributes("-fullscreen", True)
    fenetre.title("Labyrinthe")
    
    return fenetre

def BaseLabyrinthe(largeur, hauteur, cellules, support):
    canvas_base_labyrinthe = Canvas(
        support,
        width=largeur,
        height=hauteur,
        bg="darkgray"
    )
    canvas_base_labyrinthe.pack(fill=BOTH, expand=True)
    
    entree_random = [30,180,330,480,870]
    sortie_random = [30,180,330,480,870]
    entree = random.choice(entree_random)
    sortie = random.choice(sortie_random)
    print(entree,sortie)

    for y in range(0, hauteur+cellules, cellules):  # Parcours des lignes
        for x in range(0, largeur+cellules, cellules):  # Parcours des colonnes
            canvas_base_labyrinthe.create_rectangle(
                x, y,
                x + cellules, y + cellules,
                fill="silver", outline="gray",     
            )
            if x == 0 or x == largeur or y == 0 or y == hauteur:
                canvas_base_labyrinthe.create_rectangle(
                x, y,
                x + cellules, y + cellules,
                fill="black", outline="gray",      
            )       
    canvas_base_labyrinthe.create_rectangle(
        entree, 0,
        entree + cellules, cellules,
        fill="red", outline="gray",      
    )      
    canvas_base_labyrinthe.create_rectangle(
        sortie, hauteur + cellules,
        sortie + cellules, hauteur,
        fill="blue", outline="gray",      
    )
    return 

""" VARIABLES """

fenetre = InterfaceLabyrinthe()
largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30
entree = [30,180,330,480,870]
sortie = [30,180,330,480,870]
print(largeur_ecran,hauteur_ecran)

""" APPELS FONCTIONS"""

BaseLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)
print(taille_cellule)

fenetre.mainloop()
