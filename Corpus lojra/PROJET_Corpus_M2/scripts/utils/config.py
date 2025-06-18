import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Chemins des dossiers
DATA_PATH = "donnees/"
RAW_DATA_PATH = "donnees/raw/"
PROCESSED_DATA_PATH = "donnees/processed/"
LOG_PATH = "logs/scraping.log"

# Configuration des API
REDDIT_CREDENTIALS = {
    'client_id': os.getenv("REDDIT_CLIENT_ID"),
    'client_secret': os.getenv("REDDIT_CLIENT_SECRET"),
    'user_agent': os.getenv("REDDIT_USER_AGENT")
}


TWITTER_CREDENTIALS = {
    'api_key': os.getenv('TWITTER_API_KEY'),
    'api_secret_key': os.getenv('TWITTER_API_SECRET_KEY'),
    'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
    'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
    'bearer_token': os.getenv('TWITTER_BEARER_TOKEN')
}

TWITCH_CREDENTIALS = {
    'client_id': os.getenv('TWICH_CLIENT_ID'),
    'token': os.getenv('TWICH_ACCESS_TOKEN')
}

YOUTUBE_CREDENTIALS = {
    'client_id':os.getenv("CLIENT_ID"),
    'auth_uri': os.getenv("AUTH_URI"),
    'token_uri': os.getenv("TOKEN_URI"),
    'client_secret': os.getenv("CLIENT_SECRET"),
    'youtube_api_key': os.getenv("YOUTUBE_API_KEY")
}
