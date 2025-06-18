import praw
import tkinter as tk
from scripts.utils.helpers import save_data
from scripts.utils.config import REDDIT_CREDENTIALS, RAW_DATA_PATH

def scrape_reddit(subreddit_name, resultat_reddit=None, limit=100):
    """
    Scrape les posts d'un subreddit et affiche les résultats dans une zone de texte Tkinter.

    :param subreddit_name: Nom du subreddit à scraper.
    :param resultat_reddit: Zone de texte Tkinter pour afficher les résultats (optionnel).
    :param limit: Nombre maximum de posts à scraper (par défaut : 100).
    """
    try:
        reddit = praw.Reddit(**REDDIT_CREDENTIALS)
        subreddit = reddit.subreddit(subreddit_name)
        posts = []

        for post in subreddit.hot(limit=limit):
            posts.append({
                'title': post.title,
                'text': post.selftext,
                'author': post.author.name if post.author else None,
                'score': post.score,
                'url': post.url
            })

        # Afficher les résultats dans la zone de texte Tkinter
        if resultat_reddit:
            resultat_reddit.insert(tk.END, f"Nombre de posts trouvés : {len(posts)}\n")
            resultat_reddit.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel

            for index, post in enumerate(posts, start=1):
                resultat_reddit.insert(tk.END, f"Post #{index}:\n")
                resultat_reddit.insert(tk.END, f"Titre : {post['title']}\n")
                resultat_reddit.insert(tk.END, f"Auteur : {post['author']}\n")
                resultat_reddit.insert(tk.END, f"Score : {post['score']}\n")
                resultat_reddit.insert(tk.END, f"URL : {post['url']}\n")
                resultat_reddit.insert(tk.END, f"Contenu : {post['text'][:200]}...\n")  # Tronquer le contenu
                resultat_reddit.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
        else:
            print(f"Nombre de posts trouvés : {len(posts)}")
            for index, post in enumerate(posts, start=1):
                print(f"Post #{index}:")
                print(f"Titre : {post['title']}")
                print(f"Auteur : {post['author']}")
                print(f"Score : {post['score']}")
                print(f"URL : {post['url']}")
                print(f"Contenu : {post['text'][:200]}...")  # Tronquer le contenu
                print("-" * 80)  # Séparateur visuel

        # Sauvegarder les données
        save_data(posts, f"{RAW_DATA_PATH}reddit/{subreddit_name}.json")

    except Exception as e:
        if resultat_reddit:
            resultat_reddit.insert(tk.END, f"Erreur lors du scraping : {e}\n")
        else:
            print(f"Erreur lors du scraping : {e}")

    finally:
        if resultat_reddit:
            resultat_reddit.insert(tk.END, "Scraping terminé.\n")
            resultat_reddit.see(tk.END)  # Faire défiler vers le bas
        else:
            print("Scraping terminé.")