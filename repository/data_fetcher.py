# Import de la librairie yfinance pour récupérer les données financières en direct
import yfinance as yf

# Définition d'une fonction pour récupérer le dernier prix de clôture d'un actif
def get_price(ticker):
    data = yf.Ticker(ticker)  # Crée un objet Ticker pour accéder aux données du ticker passé en argument
    return data.history(period="1d")["Close"].iloc[-1]  # Récupère le prix de clôture du dernier jour disponible
