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
    # Centrer le canevas dans la fenêtre
    frame = Frame(support)
    frame.pack(fill=BOTH, expand=True)

    # Canevas
    canvas_base_labyrinthe = Canvas(
        frame,
        width=largeur,
        height=hauteur,
        bg="darkgray"
    )
    
    canvas_base_labyrinthe.place(relx=0.5, rely=0.5, anchor=CENTER)

    entree_random = [90,180,330,480,840]
    sortie_random = [90,180,330,480,840]
    entree = random.choice(entree_random)
    sortie = random.choice(sortie_random)

    for y in range(0, hauteur, cellules):  # y = lignes
        for x in range(0, largeur, cellules):  # x = colonnes
            canvas_base_labyrinthe.create_rectangle(
                x, y,
                x + cellules, y + cellules,
                fill="silver", outline="gray",     
            )
            if x == 0 or x == largeur-cellules or y == 0 or y == hauteur-cellules:
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
        sortie, hauteur-cellules,
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

""" APPELS FONCTIONS """

BaseLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)
fenetre.mainloop()
