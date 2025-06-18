import os
import json
import tkinter as tk
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from scripts.utils.helpers import save_data
from scripts.utils.config import RAW_DATA_PATH

# Chemin vers le fichier client_secret.json
CLIENT_SECRET_FILE = 'client_secret.json'

# Scopes requis pour accéder aux sous-titres YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def authenticate():
    """
    Authentifie l'utilisateur via OAuth 2.0 et retourne les credentials.
    """
    creds = None
    # Charger les credentials existants s'ils existent
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si les credentials n'existent pas ou sont invalides, demander une nouvelle authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Enregistrer les credentials pour les utilisations futures
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_video_captions(video_id, language='en'):
    """
    Récupère les sous-titres d'une vidéo YouTube via l'API YouTube Data v3.
    :param video_id: ID de la vidéo YouTube.
    :param language: Langue des sous-titres à récupérer (par défaut 'en').
    :return: Texte des sous-titres ou message d'erreur.
    """
    try:
        # Authentification avec OAuth 2.0
        creds = authenticate()
        youtube = build('youtube', 'v3', credentials=creds)

        # Récupérer les sous-titres disponibles
        captions_request = youtube.captions().list(part="snippet", videoId=video_id)
        captions_response = captions_request.execute()

        # Vérifier si des sous-titres existent
        captions = captions_response.get("items", [])
        if not captions:
            return f"Aucun sous-titre disponible pour cette vidéo."

        # Sélectionner la piste correspondant à la langue demandée
        caption_id = None
        for caption in captions:
            if caption["snippet"]["language"] == language:
                caption_id = caption["id"]
                break

        if not caption_id:
            return f"Aucun sous-titre en {language} trouvé."

        # Récupérer les sous-titres (format JSON brut)
        caption_request = youtube.captions().download(id=caption_id)
        caption_response = caption_request.execute()

        return caption_response.decode('utf-8')  # Convertir bytes en string

    except Exception as e:
        if "insufficient permissions" in str(e).lower():
            return "Erreur : Permissions insuffisantes pour accéder aux sous-titres. Vérifiez les autorisations ou contactez le propriétaire de la vidéo."
        return f"Erreur lors de la récupération des sous-titres : {e}"

def get_public_captions(video_id, language='en'):
    """
    Récupère les sous-titres publics d'une vidéo YouTube via youtube-transcript-api.
    :param video_id: ID de la vidéo YouTube.
    :param language: Langue des sous-titres à récupérer (par défaut 'en').
    :return: Texte des sous-titres ou message d'erreur.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        captions_text = " ".join([t['text'] for t in transcript])
        return captions_text
    except Exception as e:
        return f"Erreur lors de la récupération des sous-titres publics : {e}"

def scrape_youtube(video_url, resultat_youtube=None, language='en'):
    """
    Scrape les sous-titres d'une vidéo YouTube et affiche les résultats.
    :param video_url: L'URL de la vidéo YouTube.
    :param resultat_youtube: Zone de texte Tkinter pour afficher les résultats.
    :param language: Langue des sous-titres (par défaut 'en').
    """
    try:
        # Extraire l'ID de la vidéo depuis l'URL
        video_id = video_url.split("v=")[-1].split("&")[0]

        # Essayer de récupérer les sous-titres via l'API YouTube
        subtitles = get_video_captions(video_id, language)
        if "Erreur" in subtitles:
            # Si cela échoue, essayer de récupérer les sous-titres publics
            subtitles = get_public_captions(video_id, language)

        # Affichage des sous-titres dans la zone de texte Tkinter ou en console
        
        if resultat_youtube:
            resultat_youtube.insert(tk.END, f"Sous-titres pour la vidéo ({video_id}):\n")
            resultat_youtube.insert(tk.END, "-" * 80 + "\n")
            
            # Découper les sous-titres en blocs de 2000 caractères
            block_size = 2000
            for i in range(0, len(subtitles), block_size):
                block = subtitles[i:i + block_size]
                resultat_youtube.insert(tk.END, block + "\n")
                resultat_youtube.insert(tk.END, "-" * 40 + "\n")  # Séparateur entre les blocs
            
            resultat_youtube.insert(tk.END, "\n" + "-" * 80 + "\n")
        else:
            print(f"Sous-titres pour la vidéo ({video_id}):\n")
            print("-" * 80)
            
            # Découper les sous-titres en blocs de 2000 caractères
            block_size = 2000
            for i in range(0, len(subtitles), block_size):
                block = subtitles[i:i + block_size]
                print(block)
                print("-" * 40)  # Séparateur entre les blocs
            
            print("\n" + "-" * 80)       

        # Sauvegarder les sous-titres
        save_data(subtitles, f"{RAW_DATA_PATH}youtube/{video_id}_{language}.json")

    except Exception as e:
                error_message = f"Erreur lors du scraping : {e}"
                if resultat_youtube:
                    resultat_youtube.insert(tk.END, error_message + "\n")
                else:
                    print(error_message)

    finally:
                if resultat_youtube:
                    resultat_youtube.insert(tk.END, "Scraping terminé.\n")
                    resultat_youtube.see(tk.END)
                else:
                    print("Scraping terminé.")

# Exemple d'utilisation
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=EJzxOb_guHE"
    scrape_youtube(video_url, language='en')