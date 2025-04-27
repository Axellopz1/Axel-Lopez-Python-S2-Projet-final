# Import de pandas pour manipuler des tableaux de données
import pandas as pd

# Import de numpy pour faire des calculs mathématiques et générer des variations aléatoires
import numpy as np

# Définition de la fonction principale qui simule les stress tests
def stress_test_portefeuille(portefeuille):
    # Récupère la composition actuelle du portefeuille sous forme de DataFrame
    df = portefeuille.composition()

    # Calcule la valeur totale initiale du portefeuille
    valeur_initiale = df["Valeur Totale"].sum()

    # Crée un tableau représentant les 12 prochains mois
    mois = np.arange(1, 13)  # De 1 à 12

    # Initialise un dictionnaire pour stocker l'évolution sous chaque scénario de stress
    stress_scenarios = {
        "COVID-19": [],  # Scénario d'une crise type COVID
        "Crise 2008": [],  # Scénario d'une crise financière longue
        "Inflation forte": [],  # Scénario de forte inflation
        "Croissance économique": [],  # Scénario de forte croissance
    }

    # Initialise les valeurs de départ pour chaque scénario à la valeur initiale du portefeuille
    covid, crise2008, inflation, croissance = valeur_initiale, valeur_initiale, valeur_initiale, valeur_initiale

    # Boucle sur chaque mois
    for mois_actuel in mois:
        # --- COVID-19 : Scénario de chute brutale sur 2 mois puis reprise lente ---
        if mois_actuel <= 2:
            covid *= np.random.uniform(0.80, 0.85)  # Perte de -15% à -20%
        else:
            covid *= np.random.uniform(1.005, 1.01)  # Croissance lente entre +0.5% et +1%

        # --- Crise 2008 : Scénario de longue chute sur 6 mois puis stabilisation ---
        if mois_actuel <= 6:
            crise2008 *= np.random.uniform(0.95, 0.98)  # Perte de -2% à -5% par mois
        else:
            crise2008 *= np.random.uniform(0.99, 1.005)  # Stagnation légère ensuite

        # --- Inflation forte : Scénario de baisse lente constante ---
        inflation *= np.random.uniform(0.995, 0.998)  # Perte de -0.2% à -0.5% par mois

        # --- Croissance économique : Forte croissance initiale puis normalisation ---
        if mois_actuel <= 3:
            croissance *= np.random.uniform(1.01, 1.02)  # Gain de +1% à +2% sur 3 mois
        else:
            croissance *= np.random.uniform(1.002, 1.005)  # Croissance plus lente ensuite

        # Stocke les nouvelles valeurs pour ce mois
        stress_scenarios["COVID-19"].append(covid)
        stress_scenarios["Crise 2008"].append(crise2008)
        stress_scenarios["Inflation forte"].append(inflation)
        stress_scenarios["Croissance économique"].append(croissance)

    # Convertit le dictionnaire en DataFrame pour avoir un tableau final
    df_stress = pd.DataFrame(stress_scenarios, index=mois)

    # Nommer l'index "Mois" pour plus de clarté
    df_stress.index.name = "Mois"

    # Retourne le DataFrame des stress tests
    return df_stress
