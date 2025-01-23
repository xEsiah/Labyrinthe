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
    for sol1 in range(2,lignes-3):
        for sol2 in range(20,colonnes-2):
            canvas.create_rectangle(
                sol2 * taille_cellules, sol1 * taille_cellules,
                (sol2 + 1) * taille_cellules, (sol1 + 1) * taille_cellules,
                fill="darkgray", outline="gray"
            )
            
    for murshaut1 in range(2,3):
        for murshaut2 in range(20,colonnes-2):
            canvas.create_rectangle(
                murshaut2 * taille_cellules, murshaut1 * taille_cellules,
                (murshaut2 + 1) * taille_cellules, (murshaut1 + 1) * taille_cellules,
                fill="black", outline="gray"
            )
    for mursbas1 in range(46,47):
        for mursbas2 in range(20,colonnes-2):
            canvas.create_rectangle(
                mursbas2 * taille_cellules, mursbas1 * taille_cellules,
                (mursbas2 + 1) * taille_cellules, (mursbas1 + 1) * taille_cellules,
                fill="black", outline="gray"
            )

    for mursdroite1 in range(3,47):
        for mursdroite2 in range(20,78):
            if mursdroite2 == 20 or mursdroite2 == 77:
                canvas.create_rectangle(
                    mursdroite2 * taille_cellules, mursdroite1 * taille_cellules,
                    (mursdroite2 + 1) * taille_cellules, (mursdroite1 + 1) * taille_cellules,
                    fill="black", outline="gray"
                )
            if (mursdroite1 == 11 and mursdroite2 == 20) or (mursdroite1 == 29 and mursdroite2 == 77) or (mursdroite1 == 11 and mursdroite2 == 21) or (mursdroite1 == 29 and mursdroite2 == 76) : # conidition pour les portes
                canvas.create_rectangle(
                    mursdroite2 * taille_cellules, mursdroite1 * taille_cellules,
                    (mursdroite2 + 1) * taille_cellules, (mursdroite1 + 1) * taille_cellules,
                    fill="red", outline="gray"
                )
    
    fenetre.mainloop()