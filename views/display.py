# --- Import nécessaire ---
import streamlit as st  # Import de Streamlit pour créer l'affichage web de l'application

# --- Fonction pour afficher les informations du portefeuille ---
def afficher_infos_portefeuille(portefeuille):
    st.subheader("Composition du Portefeuille")  # Titre secondaire pour la section composition
    df = portefeuille.composition()  # Récupère la composition du portefeuille sous forme de DataFrame

    # Affiche la table formatée : prix unitaire et valeur totale arrondis à 2 décimales
    st.dataframe(df.style.format({"Prix Unitaire": "{:.2f}", "Valeur Totale": "{:.2f}"}))

    # Titre secondaire pour afficher la valeur totale
    st.subheader("Valeur Totale du Portefeuille")
    valeur = portefeuille.valeur_totale()  # Calcule la valeur totale du portefeuille

    # Affiche une métrique simple : Valeur Totale du portefeuille en dollars avec séparateur de milliers
    st.metric(label="Valeur Totale", value=f"{valeur:,.2f} $")
