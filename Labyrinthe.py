from tkinter import *
import random


""" VARIABLES """

largeur_ecran = 900
hauteur_ecran = 900
taille_cellule = 30
entree_random = [90,180,330,480,840] # Pour pouvoir plus tard définir l'entrée aléatoirement
sortie_random = [90,180,330,480,840] # Pour pouvoir plus tard définir la sortie aléatoirement


""" DICTIONNAIRES ET LISTES """


dictionnaire_pieges = [["Piques"],["Trappes"],["Pièges à ours"],["Flèches empoisonnées"],["Plaques piégées"]]
dictionnaire_coffres = [["Carte"], ["Potion de soin"], ["Plaque d'armure"]]
lc_murs = []
liste_evenements = []
case_mystere = [dictionnaire_coffres, dictionnaire_pieges]
personnage = {
    "Points de vie": 10,
    "Rapidité": 0,
    "Vision": 0,
    "Plaque d'armure" : 0,
    "Potion de soin" : 0,
}


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

def dessin_des_trois_types_de_terrain(terrain_à_générer): # fonction pour dessiner les cases murs et les cases sols
    if terrain_à_générer == 0: # sols
        dimension_labyrinthe.create_rectangle(
            mursx, mursy,
            mursx + taille_cellule, mursy + taille_cellule,
            fill="white", outline="darkgrey", 
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
            fill="black", outline="darkgrey", 
        )
    return 
    
def generation_terrain(nombre_aléatoire,x,y,mystere): # fonction pour déterminer les probabilité de générer une case mur ou une case sol
    global lc_murs
    if nombre_aléatoire <= 51: # sols
        dessin_des_trois_types_de_terrain(0)
    elif nombre_aléatoire >= 52 and nombre_aléatoire < 60: # objets/pièges
        dessin_des_trois_types_de_terrain(1)
        # randomizer les pieges et le nombre 
        choix_case_mystere = random.choice(mystere)
        random.shuffle(choix_case_mystere)
    else: # murs
        dessin_des_trois_types_de_terrain(2)
        lc_murs.append([x,y])
    return lc_murs

for mursx in range(30, hauteur_ecran-30, taille_cellule):  # y = lignes
    for mursy in range(30, largeur_ecran-30, taille_cellule):  # x = colonnes
        nombre = random.randint(0,100)
        generation_terrain(nombre, mursx, mursy,case_mystere)
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

personnage = dimension_labyrinthe.create_rectangle(
    entree + 5, 5,  # Départ légèrement à l'intérieur de l'entrée
    entree + taille_cellule - 5, taille_cellule - 5,
    fill="aqua", outline="black"
)

def deplacement_personnage(event):
    if event.keysym == "Up":
        dimension_labyrinthe.move(personnage, 0, -taille_cellule)
    elif event.keysym == "Down":
        dimension_labyrinthe.move(personnage, 0, taille_cellule)
    elif event.keysym == "Left":
        dimension_labyrinthe.move(personnage, -taille_cellule, 0)
    elif event.keysym == "Right":
        dimension_labyrinthe.move(personnage, taille_cellule, 0)
        
        
""" APPELS FONCTIONS """


fenetre_jeu.bind("<Up>", deplacement_personnage)
fenetre_jeu.bind("<Down>", deplacement_personnage)
fenetre_jeu.bind("<Left>", deplacement_personnage)
fenetre_jeu.bind("<Right>", deplacement_personnage)
print(lc_murs,len(lc_murs))
fenetre_jeu.mainloop()


# x1 + taille_cellule = verif droite
# x1 - taille _cellule + verif gauche
# y1 + taille_cellule = verif bas
# y1 - taille_cellule = verif haut