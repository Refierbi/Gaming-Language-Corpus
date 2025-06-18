import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import tkinter as tk
from scripts.utils.helpers import save_data
from scripts.utils.config import RAW_DATA_PATH

def scrape_articles(url, resultat_articles=None):
    """
    Scrape les articles d'une URL donnée et affiche les résultats dans une zone de texte Tkinter.

    :param url: L'URL de la page à scraper.
    :param resultat_articles: Zone de texte Tkinter pour afficher les résultats (optionnel).
    """
    # Configuration de Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Exécuter en mode headless (sans interface graphique)
    chrome_options.add_argument("--disable-gpu")  # Désactiver GPU pour éviter les avertissements
    chrome_options.add_argument("--no-sandbox")  # Désactiver le sandbox pour éviter les erreurs

    # Chemin vers chromedriver (utilisez une chaîne brute)
    service = Service(r'chromedriver/chromedriver.exe')  # Remplacez par le chemin de votre chromedriver

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Charger la page
        driver.get(url)
        time.sleep(5)  # Attendre que la page se charge (ajuster le temps si nécessaire)

        # Récupérer le contenu de la page après chargement dynamique
        page_source = driver.page_source

        # Utiliser BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Trouver les éléments souhaités (exemple : critiques ou articles)
        articles = [article.get_text(strip=True) for article in soup.find_all('div', class_=re.compile(r'review|article|content'))]

        # Afficher les articles trouvés
        if resultat_articles:
            resultat_articles.insert(tk.END, f"Nombre d'articles trouvés : {len(articles)}\n")
            resultat_articles.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel

            for index, article in enumerate(articles, start=1):
                # Tronquer l'article à 200 caractères pour une meilleure lisibilité
                truncated_article = (article[:200] + '...') if len(article) > 200 else article

                # Afficher l'article avec un numéro et une séparation visuelle
                resultat_articles.insert(tk.END, f"Article #{index}:\n{truncated_article}\n")
                resultat_articles.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
        else:
            print(f"Nombre d'articles trouvés : {len(articles)}")
            print("-" * 80)  # Séparateur visuel

            for index, article in enumerate(articles, start=1):
                # Tronquer l'article à 200 caractères pour une meilleure lisibilité
                truncated_article = (article[:200] + '...') if len(article) > 200 else article

                # Afficher l'article avec un numéro et une séparation visuelle
                print(f"Article #{index}:\n{truncated_article}\n")
                print("-" * 80)  # Séparateur visuel

        # Sauvegarder les données
        save_data(articles, f"{RAW_DATA_PATH}articles/articles.json")

    except Exception as e:
        if resultat_articles:
            resultat_articles.insert(tk.END, f"Erreur lors du scraping : {e}\n")
        else:
            print(f"Erreur lors du scraping : {e}")

    finally:
        # Fermer le navigateur
        driver.quit()
        if resultat_articles:
            resultat_articles.insert(tk.END, "Scraping terminé.\n")
            resultat_articles.see(tk.END)  # Faire défiler vers le bas
        else:
            print("Scraping terminé.")