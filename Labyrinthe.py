from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random

def rejouer(fenetre):
    fenetre.destroy() 
    Labyrinthe()


def Labyrinthe():
    """--------- INITIALISATIONS (fenetres principale, menus et base du labyrinthe) ---------"""

    ''' Création et paramétrage de la fenètre principale '''
    fenetre_jeu = Tk()
    fenetre_jeu.attributes("-fullscreen", True)
    fenetre_jeu.title("Labyrinthe")

    fond_fenetre = Frame(
        fenetre_jeu,
        background="grey12",
        border= 10,
        relief="sunken",
    )
    fond_fenetre.pack(fill=BOTH, expand=True)


    ''' Valeurs/Positions '''
    largeur_ecran = 900
    hauteur_ecran = 900
    taille_cellule = 30

    ouvertures = [120,180,270,360,810] # Pour pouvoir définir l'entrée et la sortie
    entree = random.choice(ouvertures) 
    sortie = random.choice(ouvertures)


    ''' Création et positionnement de la base du labyrinthe '''
    dimension_labyrinthe = Canvas( 
        fenetre_jeu,
        width=largeur_ecran,
        height=hauteur_ecran,
        background="black",
        border= -1,
        relief="sunken",
    )
    dimension_labyrinthe.place(relx=0.5, rely=0.5, anchor=CENTER) # Placement du labyrinthe au centre de la fenètre 


    ''' Création des boutons '''
    # Importation d'images pour illustrer les boutons
    image_importee2 =  Image.open("ressources\Porte.png")
    image_porte = ImageTk.PhotoImage(image_importee2)
    
    image_importee3 = Image.open("ressources\Rejouer.png")
    image_rejouer = ImageTk.PhotoImage(image_importee3)
    
    bouton_quitter = Button(
        fond_fenetre, 
        image= image_porte, 
        command=fenetre_jeu.destroy,
        font=("Kristen ITC", 16, "bold"),
        bg="darkgoldenrod", 
        fg="black",
        relief="raised",
        borderwidth=5,
        padx=1,
        pady=1
    )
    bouton_quitter.place(relx=0.97, rely=0.05, anchor=CENTER)

    
    bouton_rejouer = Button(
        fond_fenetre, 
        image= image_rejouer,
        command= lambda: rejouer(fenetre_jeu),
        font=("Kristen ITC", 16, "bold"),
        bg="darkgoldenrod", 
        fg="black",
        relief="raised",
        borderwidth=5,
        padx=1,
        pady=1
    )
    bouton_rejouer.place(relx=0.91, rely=0.05, anchor=CENTER)
    
    
    """--------- DICTIONNAIRES ET LISTES ---------"""


    ''' Initialisation des listes des objets et des cases '''
    dictionnaire_pieges = ["Pique(s)","Trappe(s)","Piège(s) à ours","Flèche(s) empoisonnée(s)"]
    dictionnaire_coffres = ["Carte(s)", "Potion(s) de soin", "Plaque(s) d armure"]
    lc_mystere = [] # Liste cases mystères
    lc_sols = [] # Liste cases sol
    case_mystere = [dictionnaire_coffres, dictionnaire_pieges]


    ''' Gestion de l'inventaire et de sa fenètre  '''
    inventaire_du_personnage = {
        "Points de vie": 10,
        "Rapidité": 0,
        "Vision": 0,
        "Plaque d'armure" : 0,
        "Potion de soin" : 0,
    }


    ''' Liste générant les murs extérieurs et mettant en mémoire leur position '''
    lc_murs = [[0, y] for y in range(0, 901, taille_cellule)] + [[x, 0] for x in range(0, 901, taille_cellule)] + [[870, y] for y in range(0, 901, taille_cellule)] + [[x, 870] for x in range(0, 871, taille_cellule)] # Liste cases mur
    

    '''--------- GENERATION DE LA STRUCTURE INTERNE DU LABYRINTHE ---------'''


    ''' Fonction de création des 3 types de cases du labyrinthe '''
    def création_des_trois_types_de_terrain(terrain_à_générer): # Fonction pour dessiner les cases murs et les cases sols
        if terrain_à_générer == 0: # sols
            dimension_labyrinthe.create_rectangle(
                positionX, positionY,
                positionX + taille_cellule, positionY + taille_cellule,
                fill="gold3", outline="darkgrey", 
            ) 
        elif terrain_à_générer == 1: # objets/pièges
            dimension_labyrinthe.create_rectangle(
                positionX, positionY,
                positionX + taille_cellule, positionY + taille_cellule,
                fill="gold4", outline="darkgrey", 
            ) 
        else: # murs
            dimension_labyrinthe.create_rectangle(
                positionX, positionY,
                positionX + taille_cellule, positionY + taille_cellule,
                fill="grey2", outline="darkgrey", 
            ) 


    ''' Fonction de generation aléatoire des cases du terrain (fait appel à la fonction de création des cases) '''  
    def generation_terrain(nombre_aléatoire,x,y): # Fonction pour déterminer les probabilité de générer une case mur ou une case sol
        
        
        if nombre_aléatoire > 0 and nombre_aléatoire <= 10: # Objets/Pièges
            création_des_trois_types_de_terrain(1) 
            lc_mystere.append([x,y])
            
        elif nombre_aléatoire > 10 and nombre_aléatoire <= 80: # Sols
            création_des_trois_types_de_terrain(0)
            lc_sols.append([x,y])
            
        else: # Murs
            création_des_trois_types_de_terrain(2)
            lc_murs.append([x,y])
            
        return lc_murs,lc_sols


    ''' Appel de la fonction de génération de terrain sur la grille du labyrinthe (grille située entre les 4 murs donc double parcours) '''
    for positionX in range(taille_cellule, largeur_ecran-taille_cellule, taille_cellule):  
        for positionY in range(taille_cellule, hauteur_ecran-taille_cellule, taille_cellule): 

            nombre = random.randint(0,80)
            generation_terrain(nombre, positionX, positionY) # Première génération du terrain (Très haute probabilité de murs)

            couches = [30, 90, 150, 210, 270, 330, 390, 420, 480, 540, 600, 660, 720, 780, 840]
            if [positionX, positionY] in lc_sols:
                nombre = random.randint(60, 100)
                if positionX in couches or positionY in couches:
                    generation_terrain(nombre, positionX, positionY)

                        
    ''' Gestion de l'entré et de la sortie '''       
    dimension_labyrinthe.create_rectangle( # Dessin de l'entrée sur 2 cases
        entree, 0,
        entree + taille_cellule, taille_cellule*2,
        fill="gold3", outline="darkgrey",      
    ) 
    dimension_labyrinthe.create_rectangle( # Dessin de la sortie sur 2 cases
        sortie, hauteur_ecran,
        sortie + taille_cellule, hauteur_ecran-taille_cellule*2,
        fill="gold3", outline="darkgrey",      
    )


    ''' Suppresion des murs et des cases mystères qui peuvent être générés "dans" l'entrée et la sortie '''
    if [entree, 30] in lc_murs or [sortie, 874] in lc_murs or [sortie, 870] in lc_murs or [entree, 30] in lc_mystere or [sortie, 870] in lc_mystere:
        if [entree, 30] in lc_murs:
            lc_murs.remove([entree, 30])  # Vide la case entrée+1 de la liste des murs
        elif [sortie, 840] in lc_murs:
            lc_murs.remove([sortie, 840])  # Vide la case sortie-1 de la liste des murs
        elif [sortie, 870] in lc_murs:
            lc_murs.remove([sortie, 870])  # Permettre au joueur d'aller sur la case sortie
        elif [entree, 30] in lc_mystere:
            lc_mystere.remove([entree, 30])  # Vide la case entrée+1 de la liste des cases mystères
        elif [sortie, 870] in lc_mystere:
            lc_mystere.remove([sortie, 870])  # Vide la case sortie de la liste des cases mystères


    '''--------- INSERTION ET DEPLACEMENT DU PERSONNAGE ---------'''


    ''' Design du personnage et position de départ '''
    personnage = dimension_labyrinthe.create_rectangle(
        entree + 5, 5 + taille_cellule,  
        entree + taille_cellule - 5, taille_cellule - 5 + taille_cellule,
        # Réduction et centrage du personnage par rapport à tailles_cellules
        fill="purple", outline="black"
    )


    ''' Deplacement du personnage et évenements '''
    def deplacement_personnage(commande):
        dimension_labyrinthe.itemconfig(personnage, fill="purple") # Remettre la couleur de base du personnage (changement de couleur nécessaire pour afficher quand il y a colision avec un mur)
        
        x1, y1, _, _ = dimension_labyrinthe.coords(personnage) # Récupération des coordonnées du personnage (4 nombres à cause du fonctionnement des rectangles et de .coords avec tkinter)
        direction_x, direction_y = 0, 0 # Sauvegarde des 2 seules coordonnées qui nous intéressent
        
        if commande.keysym == "Up": # Flèche du haut = Retrait d'une cellule en Y = Monter)
            direction_y = -taille_cellule
        elif commande.keysym == "Down": # Flèche du bas = Ajout d'une cellule en Y = Descendre)
            direction_y = taille_cellule
        elif commande.keysym == "Left": # Flèche de gauche = Retrait d'une cellule en X (X = 0 de base))
            direction_x = -taille_cellule
        elif commande.keysym == "Right": # Flèche de droite = Ajout d'une cellule en X = Monter)
            direction_x = taille_cellule
        dimension_labyrinthe.move(personnage, direction_x, direction_y)
        
        x1, y1, _, _ = dimension_labyrinthe.coords(personnage) # Récupère les nouvelles coordonnées après le déplacement
        nouvelles_coord = [int(x1) - 5, int(y1) - 5] # Cela facilite la gestion des collisions, des cases objets et de la case de sortie (écran de victoire)
        
        interactions_murs(nouvelles_coord,direction_x,direction_y)
        interactions_cases_mystère(nouvelles_coord,case_mystere)
        interactions_sortie(nouvelles_coord,sortie)
        print(nouvelles_coord)


    ''' Interactions avec les murs, les cases mystères et la sortie '''   
    def interactions_murs(coordonnées,x,y):   
        if coordonnées in lc_murs: # Gestion des collisions (changement de couleur si un mur est rencontré et retour à la case d'avant)
            dimension_labyrinthe.itemconfig(personnage, fill="firebrick")
            dimension_labyrinthe.move(personnage, -x, -y)
            
            
    def interactions_cases_mystère(coordonnées,mystere):
        nombre_d_objets = random.randint(1,len(mystere))
        mystere = random.choice(case_mystere) # Choix au hasard d'un des 2 types de case mystère
        random.shuffle(mystere) # Mélange des indices des items dans la liste
        if coordonnées in lc_mystere:
            for itn in range (len(mystere)):
                if itn == 0: # Choix au hasard d'un item dans la liste choisie
                    messagebox.showwarning("OH !","Cette case dissimule...")
                    if mystere[itn] in dictionnaire_coffres: # Personalisation du message si rencontre d'un bonus
                        messagebox.showwarning("SUPER !",(nombre_d_objets,mystere[itn])) 
                    else: # Personalisation du message si rencontre d'un malus
                        messagebox.showwarning("MINCE !",(nombre_d_objets,mystere[itn]))
                    
                        
    def interactions_sortie(coordonnées,fin):
        if coordonnées == [fin,870]: # Gestion de la case de sortie et de l'écran de victoire
            messagebox.showwarning("FELICITATION", "Vous êtes parvenus au bout du labyrinthe!")


    '''--------- APPELS DES FONCTIONS DE COMMANDES DU JOUEUR ---------'''


    fenetre_jeu.bind("<Up>", deplacement_personnage)
    fenetre_jeu.bind("<Down>", deplacement_personnage)
    fenetre_jeu.bind("<Left>", deplacement_personnage)
    fenetre_jeu.bind("<Right>", deplacement_personnage)  
    # Insérer


        
    fenetre_jeu.mainloop()
    return 

    
Labyrinthe()
    