import os
import json
import tkinter as tk
import requests
from scripts.utils.helpers import save_data
from scripts.utils.config import TWITCH_CREDENTIALS, RAW_DATA_PATH


def scrape_twitch(game_id, resultat_twitch=None):
    """
    Scrape les données des streams Twitch pour un jeu donné (via son game_id).
    
    :param game_id: L'ID du jeu sur Twitch.
    :param resultat_twitch: Widget Tkinter (optionnel) pour afficher les résultats.
    """
    try:
        # Vérifier si les credentials sont disponibles
        if not TWITCH_CREDENTIALS.get('client_id') or not TWITCH_CREDENTIALS.get('token'):
            raise ValueError("Les credentials Twitch (client_id ou token) ne sont pas configurés correctement.")

        # Définir les headers pour l'authentification
        headers = {
            'Client-ID': TWITCH_CREDENTIALS['client_id'],
            'Authorization': f"Bearer {TWITCH_CREDENTIALS['token']}"
        }

        # Effectuer la requête à l'API Twitch
        response = requests.get(f'https://api.twitch.tv/helix/streams?game_id={game_id}', headers=headers)

        # Vérifier si la requête a réussi
        if response.status_code != 200:
            error_message = f"Erreur lors de la récupération des données : Code {response.status_code} - {response.text}"
            if resultat_twitch:
                resultat_twitch.insert(tk.END, error_message + "\n")
            else:
                print(error_message)
            return

        # Extraire les données des streams
        data = response.json().get('data', [])
        if not data:
            if resultat_twitch:
                resultat_twitch.insert(tk.END, "Aucun stream trouvé pour ce jeu.\n")
            else:
                print("Aucun stream trouvé pour ce jeu.")
        else:
            # Afficher les données dans le widget Tkinter ou en console
            if resultat_twitch:
                resultat_twitch.insert(tk.END, f"Données récupérées pour {len(data)} streams :\n")
                for stream in data:
                    resultat_twitch.insert(tk.END, f"Titre : {stream.get('title', 'N/A')}\n")
                    resultat_twitch.insert(tk.END, f"Nom du streamer : {stream.get('user_name', 'N/A')}\n")
                    resultat_twitch.insert(tk.END, "-" * 40 + "\n")
            else:
                print(f"Données récupérées pour {len(data)} streams :")
                for stream in data:
                    print(f"Titre : {stream.get('title', 'N/A')}")
                    print(f"Nom du streamer : {stream.get('user_name', 'N/A')}")
                    print("-" * 40)

        # Sauvegarder les données dans un fichier JSON
        save_data(data, f"{RAW_DATA_PATH}twitch/{game_id}.json")

    except Exception as e:
        error_message = f"Une erreur est survenue : {str(e)}"
        if resultat_twitch:
            resultat_twitch.insert(tk.END, error_message + "\n")
        else:
            print(error_message)


if __name__ == "__main__":
    # Exemple d'utilisation sans interface graphique
    scrape_twitch(21779)  # ID de League of Legends