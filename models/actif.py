# Définition de la classe Actif pour représenter un actif financier (ex: action, obligation, ETF, etc.)
class Actif:
    # Constructeur de la classe (initialisation des attributs)
    def __init__(self, nom, prix, quantite, type_actif, secteur, zone_geo):
        self.nom = nom  # Nom ou ticker de l'actif (ex: AAPL, MSFT)
        self.prix = prix  # Prix unitaire actuel de l'actif
        self.quantite = quantite  # Quantité détenue de cet actif
        self.type_actif = type_actif  # Type d'actif (ex: Actions, Obligations, ETF)
        self.secteur = secteur  # Secteur économique (ex: Technologie, Automobile)
        self.zone_geo = zone_geo  # Zone géographique (ex: USA, Europe, Asie)

    # Méthode pour calculer la valeur totale d'un actif = prix x quantité
    def valeur_totale(self):
        return self.prix * self.quantite  # Retourne la valeur totale de cet actif
