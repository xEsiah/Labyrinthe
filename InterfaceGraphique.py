from tkinter import *
import random


def ajuster_taille(fenetre, lignes, colonnes):
    largeur_ecran = fenetre.winfo_width()
    hauteur_ecran = fenetre.winfo_height()

    taille_cellule_x = largeur_ecran // colonnes
    taille_cellule_y = hauteur_ecran // lignes
    return min(taille_cellule_x, taille_cellule_y)


import random

def generer_labyrinthe(lignes, colonnes):
    labyrinthe = [['#' for _ in range(colonnes)] for _ in range(lignes)]

    def dfs(x, y):
        """Exploration en profondeur pour créer un labyrinthe"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # Mélanger les directions de manière aléatoire

        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 < nx < lignes - 1 and 0 < ny < colonnes - 1 and labyrinthe[nx][ny] == '#':
                labyrinthe[nx][ny] = '.'
                labyrinthe[x + dx][y + dy] = '.'
                dfs(nx, ny)

    # Définir l'entrée et la sortie fixes
    entree = (1, 0)  # Entrée en haut à gauche
    sortie = (lignes - 2, colonnes - 2)  # Sortie en bas à droite

    # Définir l'entrée et la sortie comme chemins
    labyrinthe[entree[1]][entree[1]] = '.'
    labyrinthe[sortie[0]][sortie[1]] = '.'

    # Générer le labyrinthe à partir de l'entrée
    dfs(entree[0], entree[1])

    return labyrinthe



def dessiner_labyrinthe(canvas, labyrinthe, lignes, colonnes, taille_cellule):
    """Dessine le labyrinthe sur le canvas"""
    for i in range(lignes):
        for j in range(colonnes):
            x1, y1 = j * taille_cellule, i * taille_cellule
            x2, y2 = (j + 1) * taille_cellule, (i + 1) * taille_cellule
            color = 'white' if labyrinthe[i][j] == '.' else 'black'
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='gray')


def dessiner_labyrinthe_complet(fenetre, canvas, lignes, colonnes):
    """Met à jour la fenêtre en redessinant la grille et le labyrinthe"""
    taille_cellule = ajuster_taille(fenetre, lignes, colonnes)
    labyrinthe = generer_labyrinthe(lignes, colonnes)
    canvas.delete("all")  # Supprimer tous les objets existants
    dessiner_labyrinthe(canvas, labyrinthe, lignes, colonnes, taille_cellule)


def InterfaceLabyrinthe(lignes, colonnes):
    """Interface principale pour afficher le labyrinthe"""
    fenetre = Tk()
    fenetre.title("Labyrinthe")
    fenetre.state("zoomed")
    fenetre.attributes("-fullscreen", True)

    # Créer le canvas
    canvas = Canvas(
        fenetre,
        width=fenetre.winfo_screenwidth(),
        height=fenetre.winfo_screenheight(),
        bg="white"
    )
    canvas.pack(fill=BOTH, expand=True)

    # Dessiner le labyrinthe initial
    dessiner_labyrinthe_complet(fenetre, canvas, lignes, colonnes)

    # Mettre à jour l'affichage lorsque la taille de la fenêtre change
    fenetre.bind("<Configure>", lambda event: dessiner_labyrinthe_complet(fenetre, canvas, lignes, colonnes))

    # Lancer l'application
    fenetre.mainloop()


# Exemple d'appel avec un labyrinthe de 30 lignes et 60 colonnes

