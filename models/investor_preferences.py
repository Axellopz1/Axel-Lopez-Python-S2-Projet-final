# Définition de la classe InvestorPreferences pour stocker les préférences d'un investisseur
class InvestorPreferences:
    # Constructeur de la classe (initialisation des attributs)
    def __init__(self, objectif, horizon, tolerance, types_actifs=None):
        self.objectif = objectif  # Objectif financier de l'investisseur (ex: retraite, acheter une maison)
        self.horizon = horizon  # Horizon temporel en années (ex: 5 ans, 10 ans, 20 ans)
        self.tolerance = tolerance  # Tolérance au risque (ex: Faible, Moyenne, Élevée)
        self.types_actifs = types_actifs or []  # Liste des types d'actifs préférés (ex: Actions, Obligations). Si None, initialise à liste vide
