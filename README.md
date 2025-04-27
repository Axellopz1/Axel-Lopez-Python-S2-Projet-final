# Projet Python – Construction et Analyse d'un Portefeuille d'Investissement

## Objectif du projet

Ce projet vise à construire, analyser et simuler un portefeuille d’investissement personnalisé en fonction des préférences de l’utilisateur :
- Objectif financier
- Horizon temporel
- Tolérance au risque
- Types d’actifs favoris

L'application utilise **Streamlit** pour offrir une interface interactive permettant à tout utilisateur de générer son propre portefeuille en quelques clics.

---

## Fonctionnalités principales

- Collecte des préférences d’investissement via une **sidebar intuitive**.
- **Construction automatique** d'un portefeuille à partir d'actifs sélectionnés (Actions, Obligations, ETF, Immobilier, Commodités).
- **Visualisation graphique** de la répartition et des performances estimées du portefeuille.
- **Stress tests** simulant des scénarios économiques défavorables.
- **Exportation** de toutes les analyses dans un fichier Excel et Word (`portefeuille_analyses.xlsx`,`fiche_portefeuille.docx` ).

---

## Technologies utilisées

- **Python 3.12**
- **Streamlit** (interface web)
- **pandas** (gestion de données)
- **numpy** (calculs numériques)
- **yfinance** (récupération de données financières)
- **matplotlib** & **seaborn** (visualisation)
- **openpyxl** (écriture de fichiers Excel)
- **logging** (gestion des logs)

---

## Lancement du projet

1. **Ouvrir un terminal** dans le dossier du projet.
2. **Installer les dépendances** :

    bash pip install -r requirements.txt
3. Pour lancer le code 

   inscrivez la commande dans le terminal 

    `streamlit run app.py`

4. Utiliser l'interface web pour :

- Cliquer sur le lien web qui est géneré 
- Remplir vos préférences d’investissement dans la sidebar.

- Générer votre portefeuille personnalisé.

- Visualiser la composition, les performances et les stress tests.

- Exporter les résultats dans un fichier Excel et Word portefeuille_analyses.xlsx, fiche_portefeuille.docx.

## Évolution du projet initial vers la version finale

1. Avant amélioration :

- Le projet était structuré en quelques fichiers séparés (main.py, model.py, repository.py, view.py, stress_tests.py).

- Les fonctions n’étaient pas regroupées dans un package helpers/.

- L’interface utilisateur se faisait par input() dans le terminal.

- Il n’y avait pas de fichier de configuration (config.py) ni de logger (logger.py).

- Le respect du style PEP8 était partiel, sans formattage automatique.

- Aucun système de version Git/GitHub n'était mis en place.

- Aucune interface web (Streamlit) n'était utilisée.

- Le projet était fonctionnel mais en mode script "console".

2. Après amélioration :

- Création de packages modulaires (helpers/, models/, views/, repository/, stress_tests/), respectant un pattern MVC simplifié.

- Introduction d’un dossier helpers/ pour centraliser les fonctions réutilisables (construction de portefeuille, graphiques).

- Remplacement des input() par une application web Streamlit moderne, avec sidebar intuitive et affichage graphique dynamique.

- Ajout d’un fichier config.py pour centraliser les paramètres globaux du projet.

- Mise en place d’un logger personnalisé (logger.py) pour tracer les actions importantes.

- Respect complet du style PEP8 grâce à l’utilisation du formattage automatique avec black.

- Création de fichiers requirements.txt (liste des dépendances) et setup.py (installation du projet).

- Préparation du projet à un versionnement Git/GitHub, conforme aux bonnes pratiques de gestion de code source.
- Utilisation d'un fichier de configuration pour centraliser les paramètres globaux.

L'export Excel et Word est généré automatiquement sous le nom portefeuille_analyses.xlsx et fiche_portefeuille.docx dans le dossier du projet.

## Structure du code 
```bash
pip install -r requirements.txt
PortefeuilleProjetFinal/
│
├── app.py
├── config.py
├── logger.py
├── requirements.txt
├── setup.py
├── README.md
│
├── helpers/
│   ├── finance_utils.py
│   ├── plot_utils.py
│   ├── excel_utils.py
    ├── word_generator.py
│
├── models/
│   ├── actif.py
│   ├── portefeuille.py
│   ├── investor_preferences.py
│
├── repository/
│   ├── data_fetcher.py
│
├── stress_tests/
│   ├── simulator.py
│
├── views/
│   ├── display.py
│
└── .streamlit/
    └── config.toml

