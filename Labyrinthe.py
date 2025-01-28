from tkinter import *
from dicCoffres import dictionnaire_coffres
from dicPieges import dictionnaire_pieges
import random

""" VARIABLES """

largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30
entree_random = [90,180,330,480,840] 
sortie_random = [90,180,330,480,840]

''' FONCTIONS & PROGRAMMES '''

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
        # dimension_labyrinthe.create_rectangle(
        #     x, y,
        #     x + taille_cellule, y + taille_cellule,
        #     fill="silver", outline="gray",     
        # )
        if x == 0 or x == largeur_ecran-taille_cellule or y == 0 or y == hauteur_ecran-taille_cellule:
            dimension_labyrinthe.create_rectangle(
            x, y,
            x + taille_cellule, y + taille_cellule,
               fill="gray3", outline="gray33",      
        ) 

# 25 configurations différentes pour l'entrée et la sortie
entree = random.choice(entree_random)
sortie = random.choice(sortie_random)
dimension_labyrinthe.create_rectangle( # configuration entree
    entree, 0,
    entree + taille_cellule, taille_cellule,
    fill="white", outline="gray",      
)      
dimension_labyrinthe.create_rectangle( # configuration sortie
    sortie, hauteur_ecran-taille_cellule,
    sortie + taille_cellule, hauteur_ecran,
    fill="white", outline="gray",      
)


patternes_labyrinthe = [1,2,3,4,5,6]
match(patternes_labyrinthe):
    case 1:
        for i in range(12):
            dimension_labyrinthe.create_rectangle(
                i, i,
                i + taille_cellule, i + taille_cellule,
                fill="grey85", outline="white", 
            )
        

    
murs = [0,1]
placement_murs = random.choice(murs)

for mursy in range(30, hauteur_ecran-30, taille_cellule*4):  # y = lignes
    for mursx in range(30, largeur_ecran-30, taille_cellule*4):  # x = colonnes
        placement_murs = random.choice(murs)
        if placement_murs == 1 :
            placement_patternes = random.choices(patternes_labyrinthe)
            
        else:
            dimension_labyrinthe.create_rectangle(
                mursx, mursy,
                mursx + taille_cellule, mursy + taille_cellule,
                fill="grey85", outline="white", 
            )
            
        

""" APPELS FONCTIONS """

fenetre_jeu.mainloop()
