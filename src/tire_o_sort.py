import csv
import random
import time
import tkinter as tk
from tkinter import filedialog, messagebox
import argparse
from screeninfo import get_monitors
import math

def lire_csv(fichier):
    participants = []
    with open(fichier, 'r', encoding='utf-8') as f:
        lecteur = csv.reader(f, delimiter=";")
        for ligne in lecteur:
            nom, points = ligne
            participants.extend([nom] * int(points))
    return participants

def tirage_au_sort(participants):
    return random.choice(participants)

def animation_tirage(fenetre, label, participants, duree=10):
    debut = time.time()
    while time.time() - debut < duree:
        gagnant = random.choice(participants)
        label.config(text=f"Tirage en cours...\n{gagnant}")
        fenetre.update()
        
        t = (time.time() - debut) / duree
        pause = 0.05 + (0.5 - 0.05) / (1 + math.exp(-10 * (t - 0.5)))
        time.sleep(pause)

class ApplicationTirageAuSort:
    def __init__(self, master, screen_number, fullscreen, maximize, font_size):
        self.master = master
        self.master.title("Tirage au sort")
        
        self.screen_number = screen_number
        self.fullscreen = fullscreen
        self.maximize = maximize
        self.font_size = font_size
        
        self.configure_window()
        
        self.label = tk.Label(self.master, text="", font=("Arial", self.font_size))
        self.label.pack(expand=True)
        
        self.bouton_selection = tk.Button(self.master, text="Sélectionner le fichier CSV", command=self.selectionner_fichier)
        self.adjust_font_size(self.bouton_selection, 12)
        self.bouton_selection.pack(pady=20)
        
        self.participants = []

        # Gérer la sortie du mode plein écran avec la touche Échap
        self.master.bind('<Escape>', self.toggle_fullscreen)

    def configure_window(self):
        monitors = get_monitors()
        if self.screen_number <= len(monitors):
            screen = monitors[self.screen_number - 1]
            screen_width = screen.width
            screen_height = screen.height
            x = screen.x
            y = screen.y
            
            if self.fullscreen:
                # Mode plein écran personnalisé
                self.master.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
                self.master.overrideredirect(True)
                self.master.attributes('-topmost', True)
            else:
                # Rétablir les bordures de la fenêtre
                self.master.overrideredirect(False)
                self.master.attributes('-topmost', False)
                
                if self.maximize:
                    self.master.state('zoomed')
                    self.master.geometry(f"{screen_width}x{screen_height}+{x}+{y}")
                else:
                    # Centrer la fenêtre sur l'écran choisi
                    window_width = 800
                    window_height = 600
                    x = x + (screen_width - window_width) // 2
                    y = y + (screen_height - window_height) // 2
                    self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        else:
            print(f"L'écran {self.screen_number} n'existe pas. Utilisation de l'écran principal.")
            self.master.geometry("800x600")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.configure_window()
        if not self.fullscreen:
            # Forcer la mise à jour de la fenêtre pour s'assurer que les bordures sont correctement affichées
            self.master.update_idletasks()


    def positionner_fenetre(self, screen_number):
        monitors = get_monitors()
        if screen_number <= len(monitors):
            screen = monitors[screen_number - 1]
            # Calculer les dimensions de l'écran
            screen_width = screen.width
            screen_height = screen.height
            # Positionner la fenêtre au centre de l'écran choisi
            x = screen.x + (screen_width - 800) // 2
            y = screen.y + (screen_height - 600) // 2
            self.master.geometry(f"800x600+{x}+{y}")
        else:
            print(f"L'écran {screen_number} n'existe pas. Utilisation de l'écran principal.")


    def selectionner_fichier(self):
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if fichier:
            self.participants = lire_csv(fichier)
            if self.participants:
                self.bouton_selection.pack_forget()
                self.lancer_tirage()
            else:
                messagebox.showerror("Erreur", "Le fichier CSV est vide ou mal formaté.")

    def lancer_tirage(self):
        self.label.config(text="Préparation du tirage...")
        self.master.update()
        time.sleep(1)
        animation_tirage(self.master, self.label, self.participants)
        self.label.config(text="Tirage en cours...\n ... attention ...")
        self.master.update()
        time.sleep(2)
        self.label.config(text="Tirage en cours...\n ... le gagnant est ...")
        self.master.update()
        time.sleep(2)
        gagnant = tirage_au_sort(self.participants)
        self.label.config(text=f"Le gagnant est :\n{gagnant}", fg="green")

    def adjust_font_size(self, widget, base_size):
        
        # On récupére l'écran 
        monitors = get_monitors()
        if self.screen_number <= len(monitors):
            screen = monitors[self.screen_number - 1]
            screen_height = screen.height
        
        # calcul du ratio par rapport au FullHD
        scale_factor = screen_height / 1080 

        new_size = int(base_size * scale_factor)
        widget.config(font=("Arial", new_size))

def main():
    parser = argparse.ArgumentParser(description="Application de tirage au sort")
    parser.add_argument("--screen", type=int, default=1, help="Numéro de l'écran sur lequel afficher l'application (1 par défaut)")
    parser.add_argument("--fullscreen", action="store_true", help="Exécuter l'application en mode plein écran")
    parser.add_argument("--maximize", action="store_true", help="Maximiser la fenêtre de l'application")
    parser.add_argument("--font-size", type=int, default=36, help="Taille de la police (36 par défaut)")
    args = parser.parse_args()

    root = tk.Tk()
    app = ApplicationTirageAuSort(root, args.screen, args.fullscreen, args.maximize, args.font_size)
    root.mainloop()


if __name__ == "__main__":
    main()