from tkinter import *
from PIL import ImageTk, Image
import random


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
    image_importee1 =  Image.open("ressources/Sortie.png")
    image_porte = ImageTk.PhotoImage(image_importee1)
    
    image_importee2 = Image.open("ressources/Rejouer.png")
    image_rejouer = ImageTk.PhotoImage(image_importee2)
    
    bouton_quitter = Button(
        fond_fenetre, 
        image= image_porte, 
        command= lambda: quitter(fenetre_jeu),
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
    dictionnaire_pieges = ["SALVE DE FLECHE","TRAPPE","PIÈGE À OURS","ACIDE SULFURIQUE"]
    dictionnaire_coffres = ["POTION(S) DE SOIN", "PLAQUE(S) D'ARMURE"]
    lc_mystere = {} # Liste des informations complètes des cases mystères
    lc_sols = [] # Liste cases sol
    lc_chemin = [] # Liste cases chemin principal
    case_mystere = [dictionnaire_coffres, dictionnaire_pieges] # Réunion de tous les types d'événements
    inventaire_du_personnage = { 
        "PV": 5,
        "POTION(S) DE SOIN" : 0,
        "PLAQUE(S) D'ARMURE" : 0,
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
                        lc_mystere[x,y] = nombre_d_objets,mystere[itn]   # DIFFICULTE
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


    '''--------- PERSONNAGE ---------'''


    ''' Design du personnage et position de départ '''
    personnage = dimension_labyrinthe.create_rectangle(
        entree_x + 5, 5 + taille_cellule,  
        entree_x + taille_cellule - 5, taille_cellule - 5 + taille_cellule,
        # Réduction et centrage du personnage par rapport à tailles_cellules
        fill="purple", outline="black"
    )

    ''' Affichage des status du personnage '''
    # Importation des icones
    image_importee3 =  Image.open("ressources/Coeur.png") 
    image_coeur = ImageTk.PhotoImage(image_importee3)
    image_importee4 =  Image.open("ressources/Potion.png")
    image_potion = ImageTk.PhotoImage(image_importee4)
    image_importee5 =  Image.open("ressources/Armure.png")
    image_armure = ImageTk.PhotoImage(image_importee5)
    
    affichage_nombre_pv = Label( # Affichage de la stat PV
    fond_fenetre, 
    text=inventaire_du_personnage["PV"], 
    font=("Kristen ITC", 60, "bold"),
    bg="grey12", 
    fg="goldenrod"
    )
    affichage_nombre_pv.place(relx=0.1, rely=0.3)
    
    affichage_nombre_potion = Label( # Affichage de la stat Potion de soin
    fond_fenetre, 
    text=inventaire_du_personnage["POTION(S) DE SOIN"], 
    font=("Kristen ITC", 60, "bold"),
    bg="grey12", 
    fg="goldenrod"
    )
    affichage_nombre_potion.place(relx=0.1, rely=0.5) 
    
    affichage_nombre_armure = Label( # Affichage de la stat Armure
    fond_fenetre, 
    text=inventaire_du_personnage["PLAQUE(S) D'ARMURE"], 
    font=("Kristen ITC", 60, "bold"),
    bg="grey12", 
    fg="goldenrod"
    )
    affichage_nombre_armure.place(relx=0.1, rely=0.7) 
    
    
    affichage_nombre_pv_icon = Label(fond_fenetre, image=image_coeur, bg="grey12") # Affichage de l'icone pour PV
    affichage_nombre_pv_icon.place(relx=0.02, rely=0.3)

    affichage_nombre_potion_icon = Label(fond_fenetre, image=image_potion, bg="grey12") # Affichage de l'icone pour Potions
    affichage_nombre_potion_icon.place(relx=0.02, rely=0.5)
    
    affichage_nombre_armure_icon = Label(fond_fenetre, image=image_armure, bg="grey12") # Affichage de l'icone pour Armure
    affichage_nombre_armure_icon.place(relx=0.02, rely=0.7)
    
    def mettre_a_jour_stats(): 
        affichage_nombre_pv.config(text=inventaire_du_personnage["PV"])
        affichage_nombre_potion.config(text=inventaire_du_personnage["POTION(S) DE SOIN"])
        affichage_nombre_armure.config(text=inventaire_du_personnage["PLAQUE(S) D'ARMURE"])

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


    ''' Interactions avec les murs, les cases mystères et la sortie et affichage des événements '''   
    def interactions_murs(coordonnées,x,y):    
        if coordonnées in lc_murs: # Gestion des collisions (changement de couleur si un mur est rencontré et retour à la case d'avant)
            dimension_labyrinthe.itemconfig(personnage, fill="firebrick")
            dimension_labyrinthe.move(personnage, -x, -y)

    def interactions_cases_mystère(coordonnées, mystere, fenetre, inventaire):
        coord_tuple = tuple(coordonnées)
        if coord_tuple in mystere:
            nombre, objet = mystere[coord_tuple]
            afficher_surprise_et_evenements(fenetre,nombre,objet)       
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

    def afficher_surprise_et_evenements(fenetre, nombre_d_objets, mystere_element): 
        affichage_surprise = Toplevel(fenetre)
        affichage_surprise.configure(bg="grey25")
        affichage_surprise.geometry("420x100+10+20") # Positionne les alertes en haut à gauche
        texte_surprise = Label(affichage_surprise, text="OH ! \nCETTE CASE DISSIMULE...", font=("Kristen ITC", 16, "bold"), bg="grey25", fg="goldenrod")
        texte_surprise.pack(expand=True)
        affichage_surprise.after(1200, affichage_surprise.destroy) # Fermeture automatique après le temps choisi
    
        def afficher_événement(fenetre, remplacement):
            evenement = Toplevel(fenetre)
            evenement.configure(bg="grey25")
            evenement.geometry("420x100+10+160")
            evenement_texte = Label(evenement, text= f"{remplacement} {mystere_element}", font=("Kristen ITC", 16, "bold"), bg="grey25", fg="goldenrod")
            evenement_texte.pack(expand=True)
            evenement.after(2500, evenement.destroy)
        if mystere_element not in dictionnaire_coffres:
            if mystere_element != "PIÈGE À OURS" and mystere_element != "ACIDE SULFURIQUE": # Affichage différent pour les objets et pour certains piège
                afficher_événement(fenetre, "UN(E)")    
        else: # Affichage pour les autres pièges
            afficher_événement(fenetre, nombre_d_objets)
            print("OK")

                  
    '''  Gestion des conséquences des événements sur les statuts du joueur '''   
    def evenement_cause_par_case_mystere(nombre,objet,inventaire, fenetre):
        if objet == "SALVE DE FLECHE": # Enleve 1 point de vie (ou d'armure si armure > 0)
            if inventaire["PLAQUE(S) D'ARMURE"] >= nombre:
                inventaire["PLAQUE(S) D'ARMURE"] -= nombre
            else:
                inventaire["PV"] -= nombre
                
        if objet == "TRAPPE": # Renvoie le personnage à l'entrée (EASTER EGG: faible chance de l'envoyer à la sortie)
            easter_egg = random.randint(0, 100)
            if easter_egg != 99:
                dimension_labyrinthe.coords(
                    personnage,
                    entree_x + 5, 35,  
                    entree_x + taille_cellule - 5, taille_cellule + 25
                )
                inventaire["PV"] -= 1
            else:
                dimension_labyrinthe.coords(
                    personnage,
                    sortie_x + 5, sortie_y + 5,  
                    sortie_x + taille_cellule - 5, sortie_y + 25
                )
            
        if objet == "PIÈGE À OURS": # Immoblise pendant quelques secondes 
            immobilisation(fenetre)
            if inventaire["PLAQUE(S) D'ARMURE"] >= nombre:
                inventaire["PLAQUE(S) D'ARMURE"] -= nombre
            else:
                inventaire["PV"] -= nombre
                if inventaire["PV"] <= 0:
                    rejouer(fenetre)
                    
        if objet == "ACIDE SULFURIQUE": # Supprime toute l'armure
            destruction_armure(fenetre)
            if inventaire["PLAQUE(S) D'ARMURE"] != 0:
                inventaire["PLAQUE(S) D'ARMURE"] = 0 

        if objet == "PLAQUE(S) D'ARMURE" and inventaire["PLAQUE(S) D'ARMURE"] < 4: # Octroie de l'armure (maximum à 4)
            inventaire["PLAQUE(S) D'ARMURE"] += nombre

        if objet == "POTION(S) DE SOIN" and inventaire["POTION(S) DE SOIN"] < 4: # Octroie des potions (maximum à 4)
            inventaire["POTION(S) DE SOIN"] += nombre

        if inventaire["PV"] <= 0: # Condition de GAME OVER  
            fin_de_partie_defaite(fenetre)  
   
        mettre_a_jour_stats()    


    def immobilisation(fenetre): # Fonction pour afficher le statut d'immobilisation lorsque le joueur rencontre piège à ours 
        immobilisation = Toplevel(fenetre) # Crée la fenêtre d'événement "immobilisation"
        immobilisation.configure(bg="grey25")
        immobilisation.geometry("420x100+10+160")  # Position du message
        texte_événement_immobilisation = Label(
            immobilisation, 
            text="UN PIÈGE À OURS\nQUI VOUS A IMMOBILISÉ", # Message
            font=("Kristen ITC", 16, "bold"), 
            bg="grey25", 
            fg="goldenrod"
        )
        texte_événement_immobilisation.pack(expand=True)
        immobilisation.focus_set() # Change la fenetre prise en compte, en quelque sorte elle devient la fenetre principale tant que non détruite
        immobilisation.after(3000, immobilisation.destroy)  # Réactive les événements après 3 secondes

 
    def destruction_armure(fenetre): # Fonction pour afficher le statut de destruction d'armure lorsque le joueur rencontre de l'acide
        destruction_armure = Toplevel(fenetre) # Crée la fenêtre d'événement "destruction_armure"
        destruction_armure.configure(bg="grey25")
        destruction_armure.geometry("420x100+10+160")  # Position du message
        texte_événement_destruction_armure = Label(
            destruction_armure, 
            text="DE L'ACIDE SULFURIQUE\nVOTRE ARMURE DISPARAIT", # Message
            font=("Kristen ITC", 16, "bold"), 
            bg="grey25", 
            fg="goldenrod"
        )
        texte_événement_destruction_armure.pack(expand=True)
        destruction_armure.after(2500, destruction_armure.destroy)


    def soignement(inventaire, fenetre): # Fonction pour utiliser les potions de soin
        def creation_fenetre_soin(changement_texte): 
            soin = Toplevel(fenetre) # Crée la fenêtre d'événement "soin"
            soin.configure(bg="grey25")
            soin.geometry("420x100+10+160")  # Positionne du message
            texte_événement_soin = Label(
                soin, 
                text = changement_texte, # Message
                font=("Kristen ITC", 14, "bold"), 
                bg="grey25", 
                fg="goldenrod"
            )
            texte_événement_soin.pack(expand=True)
            soin.focus_set()
            soin.after(500, soin.destroy)

        if inventaire["PV"] < 5 and inventaire["POTION(S) DE SOIN"] >= 1: # Soin en dessous d'un certain seuil de vie si nombre de potion suffisant
            inventaire["PV"] += 1
            inventaire["POTION(S) DE SOIN"] -= 1
            creation_fenetre_soin("VOUS VENEZ DE VOUS SOIGNER")
        elif inventaire["PV"] >= 5:
            creation_fenetre_soin("IMPOSSIBLE\n\n PV MAXIMUM ATTEINTS")
        else:
            creation_fenetre_soin("IMPOSSIBLE\n\n NOMBRE DE POTION INSUFFISANT")
            
        mettre_a_jour_stats()     
        

    def fin_de_partie_defaite(fenetre): # Fonction pour perdre la partie
        def fermer_et_rejouer(fenetre):
            for fenetre_ouverte in fenetre.winfo_children():
                if isinstance(fenetre_ouverte, Toplevel):
                    fenetre_ouverte.destroy()
                rejouer(fenetre)
        partie_perdue = Toplevel(fenetre)
        partie_perdue.configure(bg="grey25")
        partie_perdue.attributes("-fullscreen", True)
        partie_perdue = Label(partie_perdue, text="QUEL DOMMAGE...\n\nLE LABYRINTHE\n\n A EU RAISON DE VOUS...\n", font=("Kristen ITC", 32, "bold"), bg="grey25", fg="goldenrod")
        partie_perdue.pack(expand=True)
        partie_perdue.after(5000, fermer_et_rejouer)
    
    
    '''--------- APPELS DES FONCTIONS DE COMMANDES DU JOUEUR ---------'''

    fenetre_jeu.bind("<Up>", deplacement_personnage)
    fenetre_jeu.bind("<Down>", deplacement_personnage)
    fenetre_jeu.bind("<Left>", deplacement_personnage)
    fenetre_jeu.bind("<Right>", deplacement_personnage)  
    fenetre_jeu.bind("<h>", lambda event: soignement(inventaire_du_personnage, fenetre_jeu))
    fenetre_jeu.bind("<Escape>", lambda event: quitter(fenetre_jeu))
    fenetre_jeu.bind("<r>", lambda event: rejouer(fenetre_jeu))
    fenetre_jeu.bind("<v>", lambda event: interactions_sortie([sortie_x,870],sortie_x,fenetre_jeu))
    fenetre_jeu.bind("<d>", lambda event: fin_de_partie_defaite(fenetre_jeu))
    fenetre_jeu.mainloop()

def rejouer(fenetre):
    fenetre.destroy() 
    Labyrinthe()
    
def quitter(fenetre):
    fenetre.destroy() 
    
Labyrinthe()