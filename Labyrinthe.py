from tkinter import *
import random

""" VARIABLES """

largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30
entree_random = [90,180,330,480,840] # Pour pouvoir plus tard définir l'entrée aléatoirement
sortie_random = [90,180,330,480,840] # Pour pouvoir plus tard définir la sortie aléatoirement

""" DICTIONNAIRES ET LISTES """

dictionnaire_pieges = [
    ["Piques",[0, 1, 2, 3, 4, 5]], 
    ["Trappes",[0, 1, 2, 3, 4, 5]], 
    ["Pièges à ours",[0, 1, 2, 3, 4, 5]], 
    ["Flèches empoisonnées",[0, 1, 2, 3, 4, 5]], 
    ["Plaques piégées",[0, 1, 2, 3, 4, 5]],
    ]
dictionnaire_coffres = [
    ["Carte",[0, 1]], 
    ["Potion de soin",[0, 1]], 
    ["Plaque d'armure",[0, 1, 2]]
]
personnage = {
    "Points de vie": 0,
    "Rapidité": 0,
    "Vision": 0,
}


""" Liste cases """

liste_murs = []
liste_cases_mystère = []
liste_case_sol = []
liste_evenements = []
case_mystere = [dictionnaire_coffres, dictionnaire_pieges]

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

''' Création et positionnement de la base du labyrinthe (Dimensions et murs extérieurs) '''
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

''' Creation murs intérieurs (randomisées) et cases sols dont cases objets '''
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
    
def generation_terrain(nombre_aléatoire,y,x,mystere): # fonction pour déterminer les probabilité de générer une case mur ou une case sol
    if nombre_aléatoire < 50:
        dessin_terrain(0)
        liste_murs.append([x,y])
    elif nombre_aléatoire > 50 and nombre_aléatoire < 60:
        dessin_terrain(1)
        
            
            # randomizer les pieges et le nombre 
        liste_cases_mystère.append([x,y])
    else:
        dessin_terrain(2)
        liste_case_sol.append([x,y])
    return 

for mursy in range(30, hauteur_ecran-30, taille_cellule):  # y = lignes
    for mursx in range(30, largeur_ecran-30, taille_cellule):  # x = colonnes
        nombre = random.randint(0,100)
        generation_terrain(nombre, mursy, mursx,case_mystere)
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

''' Fonction pour insérer et déplacer le personnage dans le labyrinthe '''
rectangle = dimension_labyrinthe.create_rectangle(
    entree + 5, 5,  # Départ légèrement à l'intérieur de l'entrée
    entree + taille_cellule - 5, taille_cellule - 5,
    fill="aqua", outline="black"
)

def move_rectangle(event):
    if event.keysym == "Up":
        dimension_labyrinthe.move(rectangle, 0, -taille_cellule)
    elif event.keysym == "Down":
        dimension_labyrinthe.move(rectangle, 0, taille_cellule)
    elif event.keysym == "Left":
        dimension_labyrinthe.move(rectangle, -taille_cellule, 0)
    elif event.keysym == "Right":
        dimension_labyrinthe.move(rectangle, taille_cellule, 0)
        
fenetre_jeu.bind("<Up>", move_rectangle)
fenetre_jeu.bind("<Down>", move_rectangle)
fenetre_jeu.bind("<Left>", move_rectangle)
fenetre_jeu.bind("<Right>", move_rectangle)


# print("MURS\n",liste_murs) 
# print("Mystere\n",liste_cases_mystère)
# print("Passage\n",liste_cases_passage)
# print(len(liste_cases_mystère+liste_cases_passage+liste_murs))

        
""" APPELS FONCTIONS """

fenetre_jeu.mainloop()
