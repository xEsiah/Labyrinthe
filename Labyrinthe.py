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
    
    canvas = Canvas(
        support,
        width=largeur,
        height=hauteur,
        bg="darkgray"
    )
    canvas.pack(fill=BOTH, expand=True)
    
    for background1 in range(cellules, hauteur-cellules, cellules):  # Parcours des lignes
        for background2 in range(cellules*20, largeur-cellules*2, cellules):  # Parcours des colonnes
            canvas.create_rectangle(
                background2, background1,
                background2 + cellules, background1 + cellules,
                fill="silver", outline="gray"
            )
            


""" VARIABLES """

fenetre = InterfaceLabyrinthe()
largeur_ecran = fenetre.winfo_screenwidth()
hauteur_ecran = fenetre.winfo_screenheight()
taille_cellule = min(largeur_ecran, hauteur_ecran) // 40


""" APPELS FONCTIONS"""

BaseLabyrinthe(largeur_ecran, hauteur_ecran, taille_cellule, fenetre)

fenetre.mainloop()
