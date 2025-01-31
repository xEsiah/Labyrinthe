import tkinter as tk
import random

# Paramètres du labyrinthe
taille_cellule = 30
largeur = 30  # Nombre de colonnes
hauteur = 30  # Nombre de lignes

def voisins(x, y):
    """Retourne les voisins valides pour le creusement."""
    directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
    random.shuffle(directions)
    return [(x+dx, y+dy, x+dx//2, y+dy//2) for dx, dy in directions if 0 <= x+dx < largeur and 0 <= y+dy < hauteur and labyrinthe[y+dy][x+dx] == 1]

def generer_labyrinthe(x, y):
    """Génère un labyrinthe parfait en creusant des chemins."""
    labyrinthe[y][x] = 0
    pile = [(x, y)]
    while pile:
        cx, cy = pile[-1]
        voisins_valides = voisins(cx, cy)
        if voisins_valides:
            nx, ny, mx, my = voisins_valides[0]
            labyrinthe[my][mx] = 0
            labyrinthe[ny][nx] = 0
            pile.append((nx, ny))
        else:
            pile.pop()

# Génération d'une grille pleine de murs
labyrinthe = [[1 for _ in range(largeur)] for _ in range(hauteur)]

# Initialisation au centre
depart_x, depart_y = largeur // 2, hauteur // 2
generer_labyrinthe(depart_x, depart_y)

# Définition de l'entrée et de la sortie
entree = (depart_x, 0)
sortie = (depart_x, hauteur - 1)
labyrinthe[entree[1]][entree[0]] = 0
labyrinthe[sortie[1]][sortie[0]] = 0

# Interface graphique
fenetre = tk.Tk()
fenetre.attributes("-fullscreen", True)
fenetre.title("Labyrinthe")
canvas = tk.Canvas(fenetre, width=largeur * taille_cellule, height=hauteur * taille_cellule, bg="black")
canvas.pack()

for y in range(hauteur):
    for x in range(largeur):
        couleur = "ivory4" if labyrinthe[y][x] == 0 else "grey2"
        canvas.create_rectangle(x*taille_cellule, y*taille_cellule, (x+1)*taille_cellule, (y+1)*taille_cellule, fill=couleur, outline="darkgrey")

# Dessin de l'entrée et de la sortie
canvas.create_rectangle(entree[0]*taille_cellule, entree[1]*taille_cellule, (entree[0]+1)*taille_cellule, (entree[1]+1)*taille_cellule, fill="green")
canvas.create_rectangle(sortie[0]*taille_cellule, sortie[1]*taille_cellule, (sortie[0]+1)*taille_cellule, (sortie[1]+1)*taille_cellule, fill="red")

fenetre.mainloop()
