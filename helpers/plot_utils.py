# --- Imports nécessaires ---
import streamlit as st  # Pour afficher l'interface utilisateur sur Streamlit
import matplotlib.pyplot as plt  # Pour tracer des graphiques
import seaborn as sns  # Pour faire des graphiques améliorés (ex: barplot)
import pandas as pd  # Pour gérer les DataFrames
import numpy as np  # Pour faire des calculs mathématiques et simulations


# --- Afficher la composition détaillée du portefeuille ---
def afficher_repartition(portefeuille):
    df = portefeuille.composition()  # Récupère la composition du portefeuille sous forme de DataFrame
    st.subheader("Composition du portefeuille")  # Titre de section
    st.dataframe(df.style.format({"Prix": "{:.2f}", "Valeur Totale": "{:.2f}"}))  # Affiche la table formatée

    # Calcul de la valeur totale du portefeuille
    valeur_totale = df["Valeur Totale"].sum()
    # Affiche la valeur totale en bas de la table
    st.write(f"**Valeur totale du portefeuille : {valeur_totale:.2f} $**")


# --- Afficher un camembert par type d'actif ---
def afficher_repartition_type(portefeuille):
    df = portefeuille.composition()  # Récupère la composition
    df_type = df.groupby("Type")["Valeur Totale"].sum().reset_index()  # Regroupe les valeurs par Type
    fig, ax = plt.subplots()  # Crée une figure et des axes
    ax.pie(df_type["Valeur Totale"], labels=df_type["Type"], autopct='%1.1f%%')  # Tracer un pie chart
    ax.set_title("Répartition par Type d'Actif")  # Titre du graphique
    st.pyplot(fig)  # Affiche le graphique dans Streamlit


# --- Afficher un barplot par secteur ---
def afficher_repartition_secteur(portefeuille):
    df = portefeuille.composition()  # Récupère la composition
    df_secteur = df.groupby("Secteur")["Valeur Totale"].sum().reset_index()  # Regroupe les valeurs par Secteur
    fig, ax = plt.subplots()  # Crée une figure et des axes
    sns.barplot(x="Secteur", y="Valeur Totale", data=df_secteur, ax=ax)  # Tracer un barplot
    ax.set_title("Répartition Sectorielle")  # Titre du graphique
    plt.xticks(rotation=45)  # Tourner les labels pour qu'ils soient lisibles
    st.pyplot(fig)  # Affiche le graphique


# --- Afficher un camembert par zone géographique ---
def afficher_repartition_geo(portefeuille):
    df = portefeuille.composition()  # Récupère la composition
    df_geo = df.groupby("Zone Géographique")["Valeur Totale"].sum().reset_index()  # Regroupe par Zone
    fig, ax = plt.subplots()  # Crée une figure
    ax.pie(df_geo["Valeur Totale"], labels=df_geo["Zone Géographique"], autopct='%1.1f%%')  # Pie chart
    ax.set_title("Répartition Géographique")  # Titre
    st.pyplot(fig)  # Affiche dans Streamlit


# --- Simuler et afficher la projection sur 24 mois ---
def afficher_projections(portefeuille):
    df = portefeuille.composition()  # Récupère la composition
    valeur_initiale = df["Valeur Totale"].sum()  # Calcule la valeur de départ
    mois = np.arange(1, 25)  # 24 mois

    # Initialiser les projections pour différents scénarios
    projections = {
        "Optimiste": [],
        "Neutre": [],
        "Pessimiste": [],
    }

    # Définir les valeurs initiales pour chaque scénario
    valeur_opt, valeur_neutre, valeur_pessi = valeur_initiale, valeur_initiale, valeur_initiale

    # Simuler l'évolution de chaque scénario mois par mois
    for _ in mois:
        valeur_opt *= np.random.uniform(1.005, 1.015)  # Croissance optimiste
        valeur_neutre *= np.random.uniform(0.998, 1.005)  # Croissance neutre
        valeur_pessi *= np.random.uniform(0.990, 1.002)  # Croissance pessimiste

        # Stocker les résultats
        projections["Optimiste"].append(valeur_opt)
        projections["Neutre"].append(valeur_neutre)
        projections["Pessimiste"].append(valeur_pessi)

    # Convertir les projections en DataFrame
    df_projections = pd.DataFrame(projections, index=mois)
    df_projections.index.name = "Mois"

    # Tracer les courbes de projections
    fig, ax = plt.subplots()
    df_projections.plot(ax=ax)
    ax.set_title("Projection de la Valeur du Portefeuille (24 mois)")
    ax.set_ylabel("Valeur ($)")
    st.pyplot(fig)  # Affiche le graphique

    return df_projections  # Retourner le DataFrame pour l'utiliser ailleurs


# --- Appliquer des scénarios de stress et afficher ---
def afficher_stress_tests(portefeuille):
    from stress_tests.simulator import stress_test_portefeuille  # Import interne

    stress_results = stress_test_portefeuille(portefeuille)  # Lance les simulations de stress tests

    # Tracer l'évolution de la valeur sous chaque scénario de stress
    fig, ax = plt.subplots()
    stress_results.plot(ax=ax)
    ax.set_title("Évolution du Portefeuille sous Scénarios de Stress (12 mois)")
    ax.set_ylabel("Valeur ($)")
    ax.set_xlabel("Mois")
    st.pyplot(fig)  # Affiche le graphique

    # --- Afficher un résumé sous forme de tableau ---
    st.subheader("Résumé des pertes par scénario")
    pertes = {}

    # Calculer les pertes pour chaque scénario
    for col in stress_results.columns:
        valeur_init = stress_results[col].iloc[0]
        valeur_finale = stress_results[col].iloc[-1]
        perte_dollars = valeur_init - valeur_finale
        perte_pourcentage = ((valeur_init - valeur_finale) / valeur_init) * 100
        pertes[col] = {"Perte ($)": perte_dollars, "Perte (%)": perte_pourcentage}

    # Transformer en DataFrame pour affichage
    df_pertes = pd.DataFrame(pertes).T
    st.dataframe(df_pertes.style.format({"Perte ($)": "{:.2f}", "Perte (%)": "{:.2f}"}))  # Formater joliment

    return stress_results  # Retourner les résultats complets


# --- Faire l'analyse quantitative du portefeuille ---
def afficher_analyse_quantitative(projections):
    st.subheader("Analyse Quantitative du Portefeuille")  # Titre
    valeur_initiale = projections.iloc[0]  # Valeurs initiales
    valeur_finale = projections.iloc[-1]  # Valeurs finales

    # Calculs de performance
    rendement_total = ((valeur_finale - valeur_initiale) / valeur_initiale) * 100
    cagr = ((valeur_finale / valeur_initiale) ** (1 / 2) - 1) * 100  # CAGR annualisé sur 2 ans
    volatilite_mensuelle = projections.pct_change().std() * 100  # Volatilité
    max_drawdown = (projections.cummax() - projections).max() / projections.cummax().max() * 100  # Max drawdown

    # Regrouper les résultats
    analyse = pd.DataFrame({
        "Valeur Initiale ($)": valeur_initiale,
        "Valeur Finale ($)": valeur_finale,
        "Rendement Total (%)": rendement_total,
        "CAGR (%)": cagr,
        "Volatilité Mensuelle (%)": volatilite_mensuelle,
        "Maximum Drawdown (%)": max_drawdown
    })

    st.dataframe(analyse.style.format("{:.2f}"))  # Affiche joliment
