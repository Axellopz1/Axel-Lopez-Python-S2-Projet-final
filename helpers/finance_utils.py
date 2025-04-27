# Import de la librairie pour récupérer les prix du marché
import yfinance as yf

# Import de la classe Actif (modèle d'un actif financier)
from models.actif import Actif

# Import de la classe Portefeuille (modèle d'un portefeuille)
from models.portefeuille import Portefeuille

# Import de la librairie random pour faire des sélections aléatoires
import random

# Début du mapping manuel type d'actif - secteur - géographie
mapping_info = {
    "AAPL": ("Actions", "Technologie", "USA"),
    "MSFT": ("Actions", "Technologie", "USA"),
    "GOOGL": ("Actions", "Technologie", "USA"),
    "TSLA": ("Actions", "Automobile", "USA"),
    "AIR.PA": ("Actions", "Aéronautique", "Europe"),
    "AMZN": ("Actions", "E-commerce", "USA"),
    "BABA": ("Actions", "E-commerce", "Asie"),
    "BMW.DE": ("Actions", "Automobile", "Europe"),
    "ASML.AS": ("Actions", "Technologie", "Europe"),
    "EWJ": ("ETF", "Marché Japon", "Asie"),
    "EEM": ("ETF", "Marché Émergents", "Émergents"),
    "VOO": ("ETF", "Mixte", "USA"),
    "SPY": ("ETF", "Mixte", "USA"),
    "VNQ": ("Immobilier", "Immobilier", "USA"),
    "GLD": ("Commodités", "Or", "Global"),
    "SLV": ("Commodités", "Argent", "Global"),
    "BND": ("Obligations", "Diversifié", "USA"),
    "AGG": ("Obligations", "Diversifié", "USA"),
}
# Fin du dictionnaire mapping_info

# Début du dictionnaire pour regrouper les tickers par type
tickers_par_type = {
    "Actions": ["AAPL", "MSFT", "GOOGL", "TSLA", "AIR.PA", "AMZN", "BABA", "BMW.DE", "ASML.AS"],
    "ETF": ["VOO", "SPY", "EWJ", "EEM"],
    "Immobilier": ["VNQ"],
    "Commodités": ["GLD", "SLV"],
    "Obligations": ["BND", "AGG"],
}
# Fin du dictionnaire tickers_par_type

# Définir la fonction quotas_geo qui retourne la répartition géographique cible selon l'objectif
def quotas_geo(objectif):
    if objectif == "Préparer la retraite" or objectif == "Créer un patrimoine":
        return {"USA": 0.60, "Europe": 0.25, "Asie": 0.15}
    elif objectif == "Acheter une maison" or objectif == "Constituer une épargne":
        return {"USA": 0.50, "Europe": 0.30, "Asie": 0.20}
    elif objectif == "Financer les études des enfants":
        return {"USA": 0.60, "Europe": 0.30, "Asie": 0.10}
    else:
        return {"USA": 0.70, "Europe": 0.20, "Asie": 0.10}
# Fin de la fonction quotas_geo

# Définir la fonction allocation_dynamiques qui retourne l'allocation cible selon le profil
def allocation_dynamiques(objectif, horizon, tolerance):
    # Allocation de base selon l'objectif et l'horizon
    if objectif in ["Préparer la retraite", "Créer un patrimoine"]:
        if horizon > 15:
            base = {"Actions": 0.60, "ETF": 0.20, "Obligations": 0.10, "Immobilier": 0.05, "Commodités": 0.05}
        else:
            base = {"Actions": 0.40, "ETF": 0.30, "Obligations": 0.20, "Immobilier": 0.10}
    elif objectif in ["Acheter une maison", "Constituer une épargne"]:
        if horizon <= 5:
            base = {"Obligations": 0.50, "ETF": 0.30, "Immobilier": 0.20}
        else:
            base = {"Actions": 0.30, "Obligations": 0.40, "ETF": 0.30}
    elif objectif == "Financer les études des enfants":
        base = {"Actions": 0.40, "Obligations": 0.40, "ETF": 0.20}
    else:
        base = {"Actions": 0.50, "Obligations": 0.30, "ETF": 0.20}

    # Ajustement selon la tolérance au risque
    if tolerance == "Faible":
        base["Obligations"] = base.get("Obligations", 0) + 0.20
        base["Actions"] = max(0, base.get("Actions", 0) - 0.10)
    elif tolerance == "Élevée":
        base["Actions"] = base.get("Actions", 0) + 0.20
        base["Obligations"] = max(0, base.get("Obligations", 0) - 0.10)

    # Normalisation pour que la somme des poids soit 1
    total = sum(base.values())
    base = {k: v / total for k, v in base.items()}

    return base
# Fin de la fonction allocation_dynamiques

# Définir la fonction construire_portefeuille qui construit un portefeuille personnalisé
def construire_portefeuille(preferences, montant_investi):
    allocation = allocation_dynamiques(preferences.objectif, preferences.horizon, preferences.tolerance)
    geo_target = quotas_geo(preferences.objectif)

    # Déterminer les types d'actifs valides choisis par l'utilisateur
    types_valides = [t for t in preferences.types_actifs if t in tickers_par_type.keys()]
    if not types_valides:
        types_valides = ["Actions", "ETF", "Obligations"]

    # Créer un portefeuille vide
    portefeuille = Portefeuille()

    valeur_investie = 0  # Initialiser la valeur totale investie

    # Boucle sur les types d'actifs selon l'allocation
    for type_actif, poids in allocation.items():
        if type_actif not in types_valides:
            continue  # Si l'utilisateur ne veut pas ce type d'actif, passer

        tickers = tickers_par_type.get(type_actif, [])
        if not tickers:
            continue  # Pas de tickers pour ce type

        nb_actifs = max(1, int(len(tickers) * poids))  # Nombre d'actifs à sélectionner
        tickers_selectionnes = []  # Liste pour stocker les tickers sélectionnés

        # Répartir les actifs par zone géographique
        for geo, pourcentage in geo_target.items():
            candidats = [ticker for ticker in tickers if mapping_info.get(ticker, ("","",geo))[2] == geo]
            nb_geo = max(1, int(nb_actifs * pourcentage))
            tickers_selectionnes += random.sample(candidats, min(len(candidats), nb_geo))

        # Enlever les doublons si besoin
        tickers_selectionnes = list(set(tickers_selectionnes))

        # Pour chaque actif sélectionné
        for ticker in tickers_selectionnes:
            try:
                # Récupérer les données de prix avec yfinance
                data = yf.Ticker(ticker)
                prix = data.history(period="1d")["Close"].iloc[-1]

                # Déterminer la quantité achetable
                montant_alloue = montant_investi * poids / len(tickers_selectionnes)
                quantite = max(1, int(montant_alloue / prix))

                # Extraire les informations sur l'actif
                type_asset, secteur, zone_geo = mapping_info.get(ticker, ("Inconnu", "Inconnu", "Inconnu"))

                # Créer un nouvel objet Actif
                actif = Actif(ticker, prix, quantite, type_asset, secteur, zone_geo)

                # Ajouter cet actif au portefeuille
                portefeuille.ajouter_actif(actif)

                valeur_investie += prix * quantite  # Mettre à jour le montant investi

            except Exception as e:
                # Si erreur (ex: prix indisponible), afficher l'erreur
                print(f"Erreur de récupération pour {ticker}: {e}")

    # Retourner le portefeuille complet
    return portefeuille
# Fin de la fonction construire_portefeuille
