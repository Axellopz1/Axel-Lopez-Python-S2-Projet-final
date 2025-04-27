# --- Imports des modules nécessaires ---
import streamlit as st  # Pour construire l'interface web
from config import Config  # Pour accéder aux paramètres de configuration
from logger import setup_logger  # Pour configurer le système de logs
from models.investor_preferences import InvestorPreferences  # Modèle des préférences utilisateur
from helpers.finance_utils import construire_portefeuille  # Fonction pour construire le portefeuille
from helpers.plot_utils import (  # Fonctions pour afficher les graphiques et données
    afficher_repartition,
    afficher_repartition_type,
    afficher_repartition_secteur,
    afficher_repartition_geo,
    afficher_projections,
    afficher_stress_tests,
    afficher_analyse_quantitative,
)
from helpers.excel_utils import export_vers_excel  # Fonction pour exporter vers Excel

# Configuration du logger pour suivre ce qui se passe dans l'app
logger = setup_logger()


# --- Fonction principale de l'application ---
def main():
    # Configuration générale de la page Streamlit
    st.set_page_config(page_title="Gestion de Portefeuille Dynamique", layout="wide")
    st.title("Construction et Analyse Dynamique d'un Portefeuille d'Investissement")

    # --- Section sidebar pour les paramètres utilisateurs ---
    with st.sidebar:
        st.header("Paramètres de l'investisseur")  # Titre de la sidebar

        # Choix de l'objectif financier via un menu déroulant
        objectif = st.selectbox(
            "Quel est votre objectif financier ?",
            (
                "Préparer la retraite",
                "Acheter une maison",
                "Constituer une épargne",
                "Financer les études des enfants",
                "Créer un patrimoine",
            )
        )

        # Sélection de l'horizon d'investissement avec un slider
        horizon = st.slider("Horizon temporel (en années)", 1, 30, 10)

        # Sélection de la tolérance au risque
        tolerance = st.selectbox("Tolérance au risque", ("Faible", "Moyenne", "Élevée"))

        # Choix des types d'actifs préférés
        types_actifs = st.multiselect(
            "Types d'actifs préférés",
            ["Actions", "Obligations", "ETF", "Immobilier", "Commodités"],
            default=["Actions", "Obligations", "ETF"]
        )

        # Choix du montant à investir
        montant_investi = st.selectbox(
            "Montant à investir ($)",
            (10000, 25000, 50000, 100000),
            index=1
        )

        # Bouton pour valider la création du portefeuille
        valider = st.button("Construire le portefeuille")

    # --- Quand l'utilisateur clique sur "Construire le portefeuille" ---
    if valider:
        try:
            # Créer un objet InvestorPreferences avec les sélections de l'utilisateur
            preferences = InvestorPreferences(objectif, horizon, tolerance, types_actifs)

            # Afficher les choix faits par l'utilisateur
            st.subheader("Votre profil sélectionné :")
            st.write(f"Objectif : {objectif}")
            st.write(f"Horizon : {horizon} ans")
            st.write(f"Tolérance au risque : {tolerance}")
            st.write(f"Types d'actifs sélectionnés : {', '.join(types_actifs)}")
            st.write(f"Montant à investir : {montant_investi} $")
            st.markdown("---")  # Ligne de séparation

            # Construire le portefeuille avec les paramètres choisis
            portefeuille = construire_portefeuille(preferences, montant_investi)

            # Message de succès
            st.success("Portefeuille construit avec succès !")

            # --- Affichage de la composition du portefeuille ---
            st.header("Composition du Portefeuille")
            afficher_repartition(portefeuille)

            # --- Affichage des répartitions ---
            st.header("Répartition du Portefeuille")
            afficher_repartition_type(portefeuille)
            afficher_repartition_secteur(portefeuille)
            afficher_repartition_geo(portefeuille)

            # --- Affichage des projections de rendement ---
            st.header("Projections de Rendement sur 24 mois")
            projections = afficher_projections(portefeuille)

            # --- Affichage des stress tests ---
            st.header("Stress Tests Dynamiques")
            stress_results = afficher_stress_tests(portefeuille)

            # --- Analyse quantitative du portefeuille ---
            st.header("Analyse Quantitative du Portefeuille")
            afficher_analyse_quantitative(projections)

            # --- Exporter les résultats dans un fichier Excel ---
            export_vers_excel(portefeuille, projections, stress_results)
            st.success(f"Portefeuille exporté dans {Config.FICHIER_EXPORT}")

            # --- Générer également une fiche Word pour le portefeuille ---
            from helpers.word_generator import \
                generer_fiche_portefeuille  # Import local pour éviter problème si pas utilisé

            generer_fiche_portefeuille(portefeuille, projections, stress_results, preferences, montant_investi)
            st.success("Fiche de portefeuille Word générée : fiche_portefeuille.docx")

            # Logguer le succès
            logger.info("Portefeuille construit et exporté avec succès.")

        # --- Gestion des erreurs ---
        except Exception as e:
            st.error(f"Erreur lors de la construction du portefeuille : {e}")
            logger.error(f"Erreur : {e}")


# --- Exécuter la fonction principale si le fichier est lancé directement ---
if __name__ == "__main__":
    main()
