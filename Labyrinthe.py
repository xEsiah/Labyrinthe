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
case_mystere = [dictionnaire_coffres, dictionnaire_pieges]
murs = []

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

def dessin_terrain(terrain_à_générer): # fonction pour dessiner les cases murs et les cases sols
    if terrain_à_générer == 0:
        dimension_labyrinthe.create_rectangle(
            mursy, mursx,
            mursy + taille_cellule, mursx + taille_cellule,
            fill="white", outline="darkgrey", 
        ) 
    elif terrain_à_générer == 1:
        dimension_labyrinthe.create_rectangle(
            mursy, mursx,
            mursy + taille_cellule, mursx + taille_cellule,
            fill="purple", outline="darkgrey", 
        ) 
    else: 
        dimension_labyrinthe.create_rectangle(
            mursy, mursx,
            mursy + taille_cellule, mursx + taille_cellule,
            fill="black", outline="darkgrey", 
        )
    return 
    
def generation_terrain(nombre_aléatoire,y,x): # fonction pour déterminer les probabilité de générer une case mur ou une case sol
    if nombre_aléatoire < 50:
        dessin_terrain(0)
    elif nombre_aléatoire > 50 and nombre_aléatoire < 60:
        dessin_terrain(1)
        murs.append([x,y])
    else:
        dessin_terrain(2)

for mursy in range(30, hauteur_ecran-30, taille_cellule):  # y = lignes
    for mursx in range(30, largeur_ecran-30, taille_cellule):  # x = colonnes
        nombre = random.randint(0,100)
        generation_terrain(nombre, mursy, mursx)
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
print(murs)    
    # for i in range (30, largeur_ecran-30, taille_cellule): 
        
    #     murs.append[i]
    #     print(murs)


# choix_case_mystere = random.choice(case_mystere)
# print(choix_case_mystere)
# choix_element_case_mystere = random.randint(choix_case_mystere)
# print(choix_element_case_mystere)
# dimension_labyrinthe.create_rectangle(
#     mursy, mursx,
#     mursy + taille_cellule, mursx + taille_cellule,
#     fill="black", outline="darkgrey", 
# )   
        
        
        
""" APPELS FONCTIONS """

fenetre_jeu.mainloop()
