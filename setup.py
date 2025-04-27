# --- Imports nécessaires ---
from setuptools import setup, find_packages  # Outils pour préparer un paquet Python installable

# --- Configuration du projet ---
setup(
    name='portefeuille_investissement',  # Nom du projet (paquet)
    version='1.0',  # Version actuelle du projet

    packages=find_packages(),  # Trouve automatiquement tous les sous-dossiers Python contenant des __init__.py

    install_requires=[  # Liste des bibliothèques nécessaires à l'exécution du projet
        'pandas',  # Manipulation de tableaux de données
        'numpy',  # Calculs mathématiques et simulations
        'matplotlib',  # Graphiques de base
        'seaborn',  # Graphiques avancés
        'yfinance',  # Téléchargement de données financières
        'streamlit',  # Application web rapide en Python
        'openpyxl',  # Manipulation de fichiers Excel (.xlsx)
    ],
)
