from tkinter import *
from dicCoffres import dictionnaire_coffres
from dicPieges import dictionnaire_pieges

''' FONCTIONS '''

def InterfaceLabyrinthe():
    # Fenetre principale 
    fenetre = Tk()
    fenetre.title("Labyrinthe")
    fenetre.attributes("-fullscreen", True)
    return fenetre

def BaseLabyrinthe(largeur, hauteur, cellules, support):
    canvas_base_labyrinthe = Canvas(
        support,
        width=largeur,
        height=hauteur,
        bg="darkgray"
    )
    canvas_base_labyrinthe.pack(fill=BOTH, expand=True)
    

    for y in range(cellules, hauteur-cellules, cellules):  # Parcours des lignes
        for x in range(cellules*20, largeur-cellules*2, cellules):  # Parcours des colonnes
            canvas_base_labyrinthe.create_rectangle(
                x, y,
                x + cellules, y + cellules,
                fill="silver", outline="gray",     
            )
            if x == cellules*20 or x == cellules*69 or y == (cellules*38) or y == cellules:
                canvas_base_labyrinthe.create_rectangle(
                x, y,
                x + cellules, y + cellules,
                fill="black", outline="gray",      
            )
            
    return 

            
# def MursLabyrinthe(largeur, hauteur, cellules, support):
    
    



""" VARIABLES """

fenetre = InterfaceLabyrinthe()
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()
taille_cellule = min(largeur_ecran, hauteur_ecran) // 40


""" APPELS FONCTIONS"""


BaseLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)
# MursLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)
coins = BaseLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)


fenetre.mainloop()
