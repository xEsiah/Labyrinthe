from tkinter import *
from PIL import ImageTk, Image
import random
import time


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

    ouvertures_entree = [360,480]  # Pour pouvoir définir l'entrée et la sortie
    ouvertures_sortie = [120,780]
    entree_x = random.choice(ouvertures_entree)
    sortie_x = random.choice(ouvertures_sortie)
    entree_y = 30
    sortie_y = 840


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
    image_importee2 =  Image.open("ressources/Sortie.png")
    image_porte = ImageTk.PhotoImage(image_importee2)
    
    image_importee3 = Image.open("ressources/Rejouer.png")
    image_rejouer = ImageTk.PhotoImage(image_importee3)
    
    bouton_quitter = Button(
        fond_fenetre, 
        image= image_porte, 
        command=fenetre_jeu.destroy,
        font=("Kristen ITC", 16, "bold"),
        bg="grey75", 
        relief="raised",
        borderwidth=5,
        padx=1,
        pady=1
    )
    bouton_quitter.place(relx=0.97, rely=0.06, anchor=CENTER)

    
    bouton_rejouer = Button(
        fond_fenetre, 
        image= image_rejouer,
        command= lambda: rejouer(fenetre_jeu),
        font=("Kristen ITC", 16, "bold"),
        bg="grey75", 
        relief="raised",
        borderwidth=5,
        padx=1,
        pady=1
    )
    bouton_rejouer.place(relx=0.91, rely=0.06, anchor=CENTER)
    
    
    
    """--------- DICTIONNAIRES ET LISTES ---------"""


    ''' Initialisation des listes d'objets et de celles des cases '''
    dictionnaire_pieges = ["SALVE DE FLECHE","TRAPPE","PIÈGE À OURS","FLÈCHE EMPOISONNÈE"]
    dictionnaire_coffres = ["POTION(S) DE SOIN", "PLAQUE(S) D'ARMURE"]
    lc_mystere = {} # Liste des informations complètes des cases mystères
    lc_sols = [] # Liste cases sol
    lc_chemin = [] # Liste cases chemin principal
    case_mystere = [dictionnaire_coffres, dictionnaire_pieges]


    ''' Gestion de l'inventaire et de sa fenètre  '''
    inventaire_du_personnage = {
        "PV": 5,
        "PLAQUE(S) D'ARMURE" : 0,
        "POTION(S) DE SOIN" : 0,
    }


    ''' Liste générant les murs extérieurs et mettant en mémoire leur position '''
    lc_murs = [[0, y] for y in range(0, 901, taille_cellule)] + [[x, 0] for x in range(0, 901, taille_cellule)] + [[870, y] for y in range(0, 901, taille_cellule)] + [[x, 870] for x in range(0, 871, taille_cellule)] # Liste cases mur
    

    '''--------- GENERATION DE LA STRUCTURE INTERNE DU LABYRINTHE ---------'''


    ''' Fonction de création des 3 types de cases du labyrinthe '''
    def création_des_trois_types_de_terrain(terrain_à_générer,x,y): # Fonction pour dessiner les cases murs et les cases sols
        if terrain_à_générer == 0: # murs 
            dimension_labyrinthe.create_rectangle(
                x, y,
                x + taille_cellule, y + taille_cellule,
                fill="grey2", outline="darkgrey", 
            ) 
        elif terrain_à_générer == 1: # sols
            dimension_labyrinthe.create_rectangle(
                x, y,
                x + taille_cellule, y + taille_cellule,
                fill="gold3", outline="darkgrey", 
            ) 
        else: # objets/pièges
            dimension_labyrinthe.create_rectangle(
                x, y,
                x + taille_cellule, y + taille_cellule,
                fill="gold4", outline="darkgrey", 
            ) 


    ''' Fonction de generation des cases du terrain et de la gestion des listes associées (fait appel à la fonction de création des cases) '''  
    def generation_terrain(nombre_aléatoire,x,y): # Fonction pour déterminer les probabilité de générer une case mur ou une case sol
        if nombre_aléatoire <= 10: # Murs
            création_des_trois_types_de_terrain(0,x,y)
            if [x,y] not in lc_murs:
                lc_murs.append([x,y]) 
                
        elif nombre_aléatoire >= 11 and nombre_aléatoire <= 18: # Sols
            création_des_trois_types_de_terrain(1,x,y) 
            lc_sols.append([x,y]) 
            if [x,y] in lc_murs:
                lc_murs.remove([x,y])
            if (x,y) in lc_mystere:
                del lc_mystere[x,y]
                
        else: # Objets/Pièges
            création_des_trois_types_de_terrain(2,x,y)
            mystere = random.choice(case_mystere) # Choix au hasard d'un des 2 types de case mystère
            if mystere == dictionnaire_coffres:
                nombre_d_objets = random.randint(0,2)
                random.shuffle(mystere) # Mélange des indices des items dans la liste
                for itn in range (len(mystere)):
                    if itn == 0: # Choix au hasard d'un item dans la liste choisie 
                        lc_mystere[x,y] = nombre_d_objets,mystere[itn]
            else:
                random.shuffle(mystere) # Mélange des indices des items dans la liste
                for itn in range (len(mystere)):
                    if itn == 0: # Choix au hasard d'un item dans la liste choisie 
                        lc_mystere[x,y] = 1,mystere[itn]              
            if [x,y] in lc_murs:
                lc_murs.remove([x,y])
                
        return lc_murs,lc_sols, lc_mystere


    ''' Génération d'un parcours à travers l'abscisse du labyrinthe  '''    
    chemin_x, chemin_y = entree_x, entree_y
    while chemin_y < sortie_y or chemin_x != sortie_x:
        lc_chemin.append([chemin_x, chemin_y])
        generation_terrain(random.randint(15,22), chemin_x, chemin_y)
        voisins = []
        if chemin_y < sortie_y:
            voisins.append((chemin_x, chemin_y + taille_cellule))
        if chemin_x < sortie_x:
            voisins.append((chemin_x + taille_cellule, chemin_y))
        elif chemin_x > sortie_x:
            voisins.append((chemin_x - taille_cellule, chemin_y))
        if voisins:
            chemin_x, chemin_y = random.choice(voisins)

    ''' Remplissage de la grille du labyrinthe avec des cases murs/ mystères/ sols '''
    for positionX in range(taille_cellule, largeur_ecran-taille_cellule, taille_cellule):  
        for positionY in range(taille_cellule, hauteur_ecran-taille_cellule, taille_cellule): 
            if [positionX,positionY] not in lc_chemin:
                generation_terrain(random.randint(0,22), positionX, positionY) # Première génération du terrain (murs)
    print(lc_mystere)
    print(len(lc_mystere))
    
    ''' Gestion de l'entré et de la sortie '''       
    dimension_labyrinthe.create_rectangle( # Dessin de l'entrée sur 2 cases
        entree_x, 0,
        entree_x + taille_cellule, taille_cellule*2,
        fill="gold3", outline="darkgrey",      
    )
    dimension_labyrinthe.create_rectangle( # Dessin de la sortie sur 2 cases
        sortie_x, hauteur_ecran,
        sortie_x + taille_cellule, hauteur_ecran-taille_cellule*2,
        fill="gold3", outline="darkgrey",      
    )


    ''' Suppresion des murs et des cases mystères qui peuvent être générés "dans" l'entrée et la sortie ''' 

    if (entree_x, 30) in lc_mystere:
        del lc_mystere[(entree_x, 30)]  # Vide la case entrée+1 de la liste des cases mystères      
        
    if [sortie_x, 840] in lc_murs:        
        lc_murs.remove([sortie_x, 840])  # Vide la case sortie-1 de la liste des murs    
            
    if (sortie_x, 840) in lc_mystere:
        del lc_mystere[(sortie_x, 840)]  # Vide la case sortie-1 de la liste des cases mystères
        
    if [sortie_x, 870] in lc_murs:
        lc_murs.remove([sortie_x, 870])  # Vide la case sortie de la liste des murs


    '''--------- INSERTION DU PERSONNAGE ---------'''


    ''' Design du personnage et position de départ '''
    personnage = dimension_labyrinthe.create_rectangle(
        entree_x + 5, 5 + taille_cellule,  
        entree_x + taille_cellule - 5, taille_cellule - 5 + taille_cellule,
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
        interactions_cases_mystère(nouvelles_coord,lc_mystere,fenetre_jeu, inventaire_du_personnage)
        interactions_sortie(nouvelles_coord,sortie_x,fenetre_jeu)


    ''' Interactions avec les murs, les cases mystères et la sortie '''   
    def interactions_murs(coordonnées,x,y):   
        
        if coordonnées in lc_murs: # Gestion des collisions (changement de couleur si un mur est rencontré et retour à la case d'avant)
            dimension_labyrinthe.itemconfig(personnage, fill="firebrick")
            dimension_labyrinthe.move(personnage, -x, -y)


    def interactions_cases_mystère(coordonnées, mystere, fenetre, inventaire):
        coord_tuple = tuple(coordonnées)
        if coord_tuple in mystere:
            
            nombre, objet = mystere[coord_tuple]
            
            afficher_evenements(fenetre,nombre,objet)       
            evenement_cause_par_case_mystere(nombre, objet, inventaire, fenetre)
            
            x = coord_tuple[0]
            y = coord_tuple[1]
            del lc_mystere[x,y]
            
            nouveau_sol = dimension_labyrinthe.create_rectangle(
                x, y,
                x + taille_cellule, y + taille_cellule,
                fill="gold3", outline="darkgrey", 
            ) 
            dimension_labyrinthe.tag_lower(nouveau_sol, personnage)

    def interactions_sortie(coordonnées,fin,fenetre):
        if coordonnées == [fin,870]: # Gestion de la case de sortie et de l'écran de victoire
            fin_du_niveau = Toplevel(fenetre)
            fin_du_niveau.configure(bg="grey25")

            fin_du_niveau.attributes("-fullscreen", True)
            alerteLabel = Label(fin_du_niveau, text="FELICITATIONS !\n\n\nVOUS ÊTES PARVENUS À SURMONTER\n\n\n LE LABYRINTHE!\n", font=("Kristen ITC", 32, "bold"), bg="grey25", fg="goldenrod")
            alerteLabel.pack(expand=True)
            fin_du_niveau.after(10000, fin_du_niveau.destroy) # Fermeture automatique après le temps choisi


    '''--------- APPELS DES FONCTIONS DE COMMANDES DU JOUEUR ---------'''


    fenetre_jeu.bind("<Up>", deplacement_personnage)
    fenetre_jeu.bind("<Down>", deplacement_personnage)
    fenetre_jeu.bind("<Left>", deplacement_personnage)
    fenetre_jeu.bind("<Right>", deplacement_personnage)  
    # Insérer
    fenetre_jeu.mainloop()
    return 

def evenement_cause_par_case_mystere(nombre,objet,inventaire, fenetre):
   
    if objet == "SALVE DE FLECHE":
        if inventaire["PLAQUE(S) D'ARMURE"] >= nombre:
            inventaire["PLAQUE(S) D'ARMURE"] -= nombre
        else:
            inventaire["PV"] -= nombre
        
        
    # if objet == "TRAPPE":
        
        
    if objet == "PIÈGE À OURS":
        immobilisation(fenetre)
        if inventaire["PLAQUE(S) D'ARMURE"] >= nombre:
            inventaire["PLAQUE(S) D'ARMURE"] -= nombre
        else:
            inventaire["PV"] -= nombre
        
    if objet == "FLÈCHE EMPOISONNÈE":
        if inventaire["PLAQUE(S) D'ARMURE"] >= 3:
            inventaire["PLAQUE(S) D'ARMURE"] -= 3
        if inventaire["PLAQUE(S) D'ARMURE"] == 2:
            inventaire["PLAQUE(S) D'ARMURE"] -= 2  
            inventaire["PV"] -= 1
        if inventaire["PLAQUE(S) D'ARMURE"] == 1:
            inventaire["PLAQUE(S) D'ARMURE"] -= 1
            inventaire["PV"] -= 2
        else:
            inventaire["PV"] -= 3
 
    if objet == "PLAQUE(S) D'ARMURE":
        inventaire["PLAQUE(S) D'ARMURE"] += nombre
  
    if objet == "POTION(S) DE SOIN" and inventaire["POTION(S) DE SOIN"] < 5:
        inventaire["POTION(S) DE SOIN"] += nombre
    while inventaire["PV"] < 5 and inventaire["POTION(S) DE SOIN"] >= 1:
        inventaire["PV"] += 1
        inventaire["POTION(S) DE SOIN"] -= 1
                
                
    if inventaire["PV"] <= 0:
        partie_perdue = Toplevel(fenetre)
        partie_perdue.configure(bg="grey25")
        partie_perdue.attributes("-fullscreen", True)
        alerteLabel = Label(partie_perdue, text="QUEL DOMMAGE...\n\nLE LABYRINTHE\n\n A EU RAISON DE VOUS...\n", font=("Kristen ITC", 32, "bold"), bg="grey25", fg="goldenrod")
        alerteLabel.pack(expand=True)
        partie_perdue.after(10000, partie_perdue.destroy) # Fermeture automatique après le temps choisi
        rejouer(fenetre)
    print(inventaire)    
    
    return

def afficher_evenements(fenetre, nombre_d_objets, mystere_element):
    affichage_evenement = Toplevel(fenetre)
    affichage_evenement.configure(bg="grey25")
    affichage_evenement.geometry("420x100+10+20") # Positionne les alertes en haut à gauche
    alerteLabel = Label(affichage_evenement, text="OH ! \nCETTE CASE DISSIMULE...", font=("Kristen ITC", 16, "bold"), bg="grey25", fg="goldenrod")
    alerteLabel.pack(expand=True)
    affichage_evenement.after(1200, affichage_evenement.destroy) # Fermeture automatique après le temps choisi
    if mystere_element != "PIÈGE À OURS":
        evenement = Toplevel(fenetre)
        evenement.configure(bg="grey25")
        evenement.geometry("420x100+10+20")
        bn_label = Label(evenement, text=f"{nombre_d_objets} {mystere_element}", font=("Kristen ITC", 16, "bold"), bg="grey25", fg="goldenrod")
        bn_label.pack(expand=True)
        evenement.after(2500, evenement.destroy)
    

def immobilisation(fenetre):  
    immobilisation = Toplevel(fenetre) # Crée la fenêtre d'événement "immobilisation"
    immobilisation.configure(bg="grey25")
    immobilisation.geometry("420x100+10+160")  # Positionne l'alerte en haut à gauche
    texte_événement_immobilisation = Label(
        immobilisation, 
        text="UN PIÈGE À OURS\nQUI VOUS A IMMOBILISÉ", 
        font=("Kristen ITC", 16, "bold"), 
        bg="grey25", 
        fg="goldenrod"
    )
    texte_événement_immobilisation.pack(expand=True)
    immobilisation.focus_set() # Change la fenetre prise en compte, en quelque sorte elle devient la fenetre principale tant que non détruite
    immobilisation.after(3000, immobilisation.destroy)  # Réactive les événements après 3 secondes

def rejouer(fenetre):
    fenetre.destroy() 
    Labyrinthe()
   
Labyrinthe()