from tkinter import *
import random


"""--------- VARIABLES ---------"""


largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30

ouvertures = [90,180,270,360,840] # Pour pouvoir définir l'entrée et la sortie
entree = random.choice(ouvertures) 
sortie = random.choice(ouvertures)

"""--------- DICTIONNAIRES ET LISTES ---------"""


dictionnaire_pieges = [["Piques"],["Trappes"],["Pièges à ours"],["Flèches empoisonnées"],["Plaques piégées"]]
dictionnaire_coffres = [["Carte"], ["Potion de soin"], ["Plaque d'armure"]]
liste_evenements = []
case_mystere = [dictionnaire_coffres, dictionnaire_pieges]
inventaire_du_personnage = {
    "Points de vie": 10,
    "Rapidité": 0,
    "Vision": 0,
    "Plaque d'armure" : 0,
    "Potion de soin" : 0,
}
lc_murs = [[0, y] for y in range(0, 901, taille_cellule)] + [[x, 0] for x in range(0, 901, taille_cellule)] + [[870, y] for y in range(0, 901, taille_cellule)] + [[x, 900] for x in range(0, 901, taille_cellule)]  # murs extérieurs du labyrinthe


'''--------- FONCTIONS & PROGRAMMES ---------'''


''' Création et paramétrage de la fenètre '''
fenetre_jeu = Tk()
fenetre_jeu.attributes("-fullscreen", True)
fenetre_jeu.title("Labyrinthe")
fond_fenetre = Frame(
    fenetre_jeu,
    background="thistle4",
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

for y in range(0, hauteur_ecran, taille_cellule):
    for x in range(0, largeur_ecran, taille_cellule): 
        if x == 0 or x == largeur_ecran-taille_cellule or y == 0 or y == hauteur_ecran-taille_cellule:
            dimension_labyrinthe.create_rectangle(
            x, y,
            x + taille_cellule, y + taille_cellule,
               fill="grey2", outline="darkgrey",      
        ) 


''' Fonction de création des 3 types de cases du labyrinthe '''
def création_des_trois_types_de_terrain(terrain_à_générer): # fonction pour dessiner les cases murs et les cases sols
    if terrain_à_générer == 0: # sols
        dimension_labyrinthe.create_rectangle(
            mursx, mursy,
            mursx + taille_cellule, mursy + taille_cellule,
            fill="ivory4", outline="darkgrey", 
        ) 
    elif terrain_à_générer == 1: # objets/pièges
        dimension_labyrinthe.create_rectangle(
            mursx, mursy,
            mursx + taille_cellule, mursy + taille_cellule,
            fill="purple", outline="darkgrey", 
        ) 
    else: # murs
        dimension_labyrinthe.create_rectangle(
            mursx, mursy,
            mursx + taille_cellule, mursy + taille_cellule,
            fill="grey2", outline="darkgrey", 
        ) 
    
''' Fonction de generation aléatoire des cases du terrain (fait appel à la fonction de création des cases) '''  
def generation_terrain(nombre_aléatoire,x,y,mystere): # fonction pour déterminer les probabilité de générer une case mur ou une case sol
    global lc_murs
    if nombre_aléatoire <= 4: # sols
        création_des_trois_types_de_terrain(0)
    elif nombre_aléatoire > 5 and nombre_aléatoire < 7: # objets/pièges
        création_des_trois_types_de_terrain(1)
        # randomizer les pieges et le nombre 
        choix_case_mystere = random.choice(mystere)
        random.shuffle(choix_case_mystere)
    else: # murs
        création_des_trois_types_de_terrain(2)
        lc_murs.append([x,y])
    return lc_murs

''' Appel de la fonction de génération de terrain sur la grille du labyrinthe (grille située entre les 4 murs donc double parcours) '''
for mursx in range(taille_cellule, hauteur_ecran-taille_cellule, taille_cellule):  
    for mursy in range(taille_cellule, largeur_ecran-taille_cellule, taille_cellule): 
    # Gestion des probabilités de génération et appel de la fonction
        nombre = random.randint(0,10) 
        generation_terrain(nombre, mursx, mursy,case_mystere)       
    # Dessin de l'entrée et de la sortie sur 2 cases (voir entree_random & sortie_random)
        dimension_labyrinthe.create_rectangle( 
            entree, 0,
            entree + taille_cellule, taille_cellule*2,
            fill="ivory4", outline="darkgrey",      
        ) 
        dimension_labyrinthe.create_rectangle( 
            sortie, hauteur_ecran,
            sortie + taille_cellule, hauteur_ecran-taille_cellule*2,
            fill="ivory4", outline="darkgrey",      
        )
    # Gestion des murs qui peuvent être générés "dans" l'entrée et la sortie
        if [entree, 30] in lc_murs:
            lc_murs.remove([entree, 30]) # Vide la case entrée+1 de la liste des murs
        elif [sortie, 870] in lc_murs: 
            lc_murs.remove([sortie, 870]) # Permettre au joueur d'aller sur la case sortie pour valider la victoire, pas de réciproque sur l'entrée pour bloquer le joueur
        elif [sortie, 840] in lc_murs: 
            lc_murs.remove([sortie, 840]) # Vide la case sortie-1 de la liste des murs

# def voisins(x, y):
#     """Retourne les voisins valides pour le creusement."""
#     directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
#     random.shuffle(directions)
#     return [(x+dx, y+dy, x+dx//2, y+dy//2) for dx, dy in directions if 0 <= x+dx < largeur and 0 <= y+dy < hauteur and labyrinthe[y+dy][x+dx] == 1]

# def generer_labyrinthe(x, y):
#     """Génère un labyrinthe parfait en creusant des chemins."""
#     labyrinthe[y][x] = 0
#     pile = [(x, y)]
#     while pile:
#         cx, cy = pile[-1]
#         voisins_valides = voisins(cx, cy)
#         if voisins_valides:
#             nx, ny, mx, my = voisins_valides[0]
#             labyrinthe[my][mx] = 0
#             labyrinthe[ny][nx] = 0
#             pile.append((nx, ny))
#         else:
#             pile.pop()

'''--------- INSERTION ET DEPLACEMENT DU PERSONNAGE ---------'''


''' Design du personnage et position de départ '''
personnage = dimension_labyrinthe.create_rectangle(
    entree + 5, 5,  
    entree + taille_cellule - 5, taille_cellule - 5,
    # Réduction et centrage du personnage par rapport à tailles_cellules
    fill="aqua", outline="black"
)

def deplacement_personnage(event):
    x1, y1, _, _ = dimension_labyrinthe.coords(personnage)
    dx, dy = 0, 0
    
    if event.keysym == "Up":
        dy = -taille_cellule

    elif event.keysym == "Down":
        dy = taille_cellule

    elif event.keysym == "Left":
        dx = -taille_cellule

    elif event.keysym == "Right":
        dx = taille_cellule
    dimension_labyrinthe.itemconfig(personnage, fill="aqua")
    dimension_labyrinthe.move(personnage, dx, dy)
    
    x1, y1, _, _ = dimension_labyrinthe.coords(personnage)
    nouvelles_coord = [int(x1) - 5, int(y1) - 5]
    if nouvelles_coord in lc_murs:
        dimension_labyrinthe.itemconfig(personnage, fill="red")
        dimension_labyrinthe.move(personnage, -dx, -dy)
    # if nouvelles_coord == [sortie, 840]:
    #     print('you won')
        
   
"""--------- APPELS FONCTIONS ---------"""

fenetre_jeu.bind("<Up>", deplacement_personnage)
fenetre_jeu.bind("<Down>", deplacement_personnage)
fenetre_jeu.bind("<Left>", deplacement_personnage)
fenetre_jeu.bind("<Right>", deplacement_personnage)  
fenetre_jeu.mainloop()