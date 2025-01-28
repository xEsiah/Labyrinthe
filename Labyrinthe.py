from tkinter import *
from dicCoffres import dictionnaire_coffres
from dicPieges import dictionnaire_pieges
import random

""" VARIABLES """

largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30
entree_random = [90,180,330,480,840] # Pour pouvoir plus tard définir l'entrée aléatoirement
sortie_random = [90,180,330,480,840] # Pour pouvoir plus tard définir la sortie aléatoirement


''' FONCTIONS & PROGRAMMES '''

# Création et paramétrage de la fenètre
fenetre_jeu = Tk()
fenetre_jeu.attributes("-fullscreen", True)
fenetre_jeu.title("Labyrinthe")
fond_fenetre = Frame(
    fenetre_jeu,
    background="orangered4",
    border= 10,
    relief="sunken",
)
fond_fenetre.pack(fill=BOTH, expand=True)

# Création et positionnement de la base du labyrinthe (Dimensions et murs extérieurs)
dimension_labyrinthe = Canvas( 
    fenetre_jeu,
    width=largeur_ecran,
    height=hauteur_ecran,
    background="black",
    border= -1,
       relief="sunken",
)
dimension_labyrinthe.place(relx=0.5, rely=0.5, anchor=CENTER) # Placement du labyrinthe au centre de la fenètre 
    
for y in range(0, hauteur_ecran, taille_cellule):  # y = lignes
    for x in range(0, largeur_ecran, taille_cellule):  # x = colonnes
        if x == 0 or x == largeur_ecran-taille_cellule or y == 0 or y == hauteur_ecran-taille_cellule:
            dimension_labyrinthe.create_rectangle(
            x, y,
            x + taille_cellule, y + taille_cellule,
               fill="gray3", outline="gray33",      
        ) 

entree = random.choice(entree_random)
sortie = random.choice(sortie_random)

def dessin_mur_et_sol(soloumur): # fonction pour dessiner les cases murs et les cases sols
    if soloumur == 0:
        dimension_labyrinthe.create_rectangle(
            mursy, mursx,
            mursy + taille_cellule, mursx + taille_cellule,
            fill="black", outline="darkgrey", 
        )
    else: 
        dimension_labyrinthe.create_rectangle(
            mursy, mursx,
            mursy + taille_cellule, mursx + taille_cellule,
            fill="white", outline="darkgrey", 
        )
    return 
    
def genereation_murs_interns(x,proba): # fonction pour déterminer les probabilité de générer une case mur ou une case sol
    if x < proba:
        dessin_mur_et_sol(1)
    else:
        dessin_mur_et_sol(0)
        
for mursy in range(30, hauteur_ecran-30, taille_cellule):  # y = lignes
    for mursx in range(30, largeur_ecran-30, taille_cellule):  # x = colonnes
        nombre = random.randint(0,100)
        genereation_murs_interns(nombre, 55)
        dimension_labyrinthe.create_rectangle( # configuration entree
            entree, 0,
            entree + taille_cellule, taille_cellule*2,
            fill="white", outline="darkgrey",      
        )
        dimension_labyrinthe.create_rectangle( # configuration sortie
            sortie, hauteur_ecran,
            sortie + taille_cellule, hauteur_ecran-taille_cellule*2,
            fill="white", outline="darkgrey",      
        )
             
""" APPELS FONCTIONS """

fenetre_jeu.mainloop()
