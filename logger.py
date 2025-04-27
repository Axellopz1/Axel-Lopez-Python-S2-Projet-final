# --- Import de la librairie pour gérer les logs ---
import logging  # Permet de capturer des événements (infos, erreurs) pendant l'exécution du programme


# --- Fonction pour configurer et retourner un logger personnalisé ---
def setup_logger():
    # Crée ou récupère un logger nommé "portefeuille_logger"
    logger = logging.getLogger("portefeuille_logger")

    # Définit le niveau minimal de logs que l'on souhaite enregistrer (ici : INFO et au-dessus)
    logger.setLevel(logging.INFO)

    # Si le logger n'a pas déjà de gestionnaires (handlers)
    if not logger.handlers:
        # --- Configuration d'un gestionnaire de logs vers la console ---

        # Crée un gestionnaire qui affiche les logs dans la console
        ch = logging.StreamHandler()

        # Définir aussi son niveau minimal d'affichage des logs
        ch.setLevel(logging.INFO)

        # --- Définir le format d'affichage des messages de log ---
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')  # Exemple : 2025-04-27 14:00:00 - INFO - Message

        # Appliquer ce format au gestionnaire de console
        ch.setFormatter(formatter)

        # Ajouter le gestionnaire au logger
        logger.addHandler(ch)

    # Retourner le logger prêt à être utilisé partout dans l'application
    return logger
