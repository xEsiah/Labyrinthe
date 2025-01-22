from tkinter import *

def InterfaceLabyrinthe(lignes, colonnes, taille_cellules):
    # Fenetre principale 
    fenetre = Tk() 
    fenetre.title ("LabyteRINTHE") 
    fenetre.state("zoomed")

    # Création du canvas
    canvas = Canvas(
        fenetre,
        width=colonnes * taille_cellules,
        height=lignes * taille_cellules,
        bg="white"
    )
    canvas.pack()

    # Dessin des cellules
    for background1 in range(lignes):
        for background2 in range(colonnes):
            canvas.grid_anchor
            canvas.create_rectangle(
                background2 * taille_cellules, background1 * taille_cellules,
                (background2 + 1) * taille_cellules, (background1 + 1) * taille_cellules,
                fill="silver", outline="gray"
            )

    # Dessin du labyrinthe
    for lab1 in range(2,lignes-3):
        for lab2 in range(20,colonnes-2):
            canvas.create_rectangle(
                lab2 * taille_cellules, lab1 * taille_cellules,
                (lab2 + 1) * taille_cellules, (lab1 + 1) * taille_cellules,
                fill="darkgray", outline="gray"
            )
    for MursExt1 in range(2,3):
        for MursExt2 in range(20,colonnes-2):
            canvas.create_rectangle(
                MursExt2 * taille_cellules, MursExt1 * taille_cellules,
                (MursExt2 + 1) * taille_cellules, (MursExt1 + 1) * taille_cellules,
                fill="black", outline="gray"
            )

    
    fenetre.mainloop()