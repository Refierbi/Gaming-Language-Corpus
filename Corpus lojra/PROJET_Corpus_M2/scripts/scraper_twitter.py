import tweepy
from scripts.utils.helpers import save_data
from scripts.utils.config import TWITTER_CREDENTIALS, RAW_DATA_PATH
import tkinter as tk
from datetime import datetime

def scrape_twitter(query, resultat_twitter=None, limit=100):
    """
    Scrape les tweets correspondant à une requête et affiche les résultats dans une zone de texte Tkinter.

    :param query: La requête de recherche (exemple : "League of Legends").
    :param resultat_twitter: Zone de texte Tkinter pour afficher les résultats (optionnel).
    :param limit: Nombre maximum de tweets à scraper (par défaut : 100).
    """
    try:
        # Authentification à l'API Twitter v2
        client = tweepy.Client(
            bearer_token=TWITTER_CREDENTIALS["bearer_token"]
        )

        # Récupérer les tweets avec API v2
        tweets_data = client.search_recent_tweets(query=query, tweet_fields=["created_at", "public_metrics"],
                                                  max_results=min(limit, 100))  # Limite de 100 par requête

        tweets = []
        if tweets_data.data:
            for tweet in tweets_data.data:
                tweets.append({
                    'text': tweet.text,
                    'author_id': tweet.id,
                    'date': tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    'likes': tweet.public_metrics["like_count"],
                    'retweets': tweet.public_metrics["retweet_count"]
                })

        # Affichage dans Tkinter
        if resultat_twitter:
            resultat_twitter.insert(tk.END, f"Nombre de tweets trouvés : {len(tweets)}\n")
            resultat_twitter.insert(tk.END, "-" * 80 + "\n")

            for index, tweet in enumerate(tweets, start=1):
                resultat_twitter.insert(tk.END, f"Tweet #{index}:\n")
                resultat_twitter.insert(tk.END, f"Auteur ID : {tweet['author_id']}\n")
                resultat_twitter.insert(tk.END, f"Date : {tweet['date']}\n")
                resultat_twitter.insert(tk.END, f"Likes : {tweet['likes']}\n")
                resultat_twitter.insert(tk.END, f"Retweets : {tweet['retweets']}\n")
                resultat_twitter.insert(tk.END, f"Texte : {tweet['text']}\n")
                resultat_twitter.insert(tk.END, "-" * 80 + "\n")
        else:
            print(f"Nombre de tweets trouvés : {len(tweets)}")
            print("-" * 80)

            for index, tweet in enumerate(tweets, start=1):
                print(f"Tweet #{index}:")
                print(f"Auteur ID : {tweet['author_id']}")
                print(f"Date : {tweet['date']}")
                print(f"Likes : {tweet['likes']}")
                print(f"Retweets : {tweet['retweets']}")
                print(f"Texte : {tweet['text']}")
                print("-" * 80)

        # Sauvegarde des tweets
        save_data(tweets, f"{RAW_DATA_PATH}twitter/{query}.json")

    except tweepy.errors.TweepyException as e:
        if resultat_twitter:
            resultat_twitter.insert(tk.END, f"Erreur API Twitter : {e}\n")
        else:
            print(f"Erreur API Twitter : {e}")

    except Exception as e:
        if resultat_twitter:
            resultat_twitter.insert(tk.END, f"Erreur inattendue : {e}\n")
        else:
            print(f"Erreur inattendue : {e}")

    finally:
        if resultat_twitter:
            resultat_twitter.insert(tk.END, "Scraping terminé.\n")
            resultat_twitter.see(tk.END)
        else:
            print("Scraping terminé.")
