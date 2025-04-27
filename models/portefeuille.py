# Import de la librairie pandas pour manipuler facilement des tableaux (DataFrame)
import pandas as pd

# Définition de la classe Portefeuille pour gérer un ensemble d'actifs financiers
class Portefeuille:
    # Constructeur : initialise le portefeuille vide
    def __init__(self):
        self.actifs = []  # Liste pour stocker les actifs du portefeuille

    # Méthode pour ajouter un actif dans le portefeuille
    def ajouter_actif(self, actif):
        self.actifs.append(actif)  # Ajoute l'actif passé en paramètre à la liste des actifs

    # Méthode pour calculer la valeur totale du portefeuille
    def valeur_totale(self):
        return sum(actif.valeur_totale() for actif in self.actifs)  # Somme de la valeur totale de chaque actif

    # Méthode pour récupérer la composition du portefeuille sous forme d'un DataFrame pandas
    def composition(self):
        data = {
            "Nom": [actif.nom for actif in self.actifs],  # Liste des noms des actifs
            "Type": [actif.type_actif for actif in self.actifs],  # Liste des types d'actifs
            "Secteur": [actif.secteur for actif in self.actifs],  # Liste des secteurs
            "Zone Géographique": [actif.zone_geo for actif in self.actifs],  # Liste des zones géographiques
            "Prix": [actif.prix for actif in self.actifs],  # Liste des prix
            "Quantité": [actif.quantite for actif in self.actifs],  # Liste des quantités
            "Valeur Totale": [actif.valeur_totale() for actif in self.actifs],  # Liste des valeurs totales
        }
        return pd.DataFrame(data)  # Retourne un DataFrame structuré avec toutes ces informations
