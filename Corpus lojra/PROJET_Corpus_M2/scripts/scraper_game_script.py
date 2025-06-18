import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import tkinter as tk
from scripts.utils.helpers import save_data
from scripts.utils.config import RAW_DATA_PATH


def scrape_game_scripts(url, resultat_game_scripts=None):
    """
    Scrape les dialogues d'une page web avec Selenium pour gérer le JavaScript.
    :param url: L'URL de la page à scraper.
    :param resultat_game_scripts: Zone de texte Tkinter pour afficher les résultats (optionnel).
    """
    try:
        # Configuration de Selenium
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Exécuter en mode headless (sans interface graphique)
        chrome_options.add_argument("--disable-gpu")  # Désactiver GPU pour éviter les avertissements
        chrome_options.add_argument("--no-sandbox")  # Désactiver le sandbox pour éviter les erreurs
        chrome_options.add_argument("--disable-dev-shm-usage")  # Réduire les erreurs liées à la mémoire partagée
        chrome_options.add_argument("--log-level=3")  # Désactiver les logs inutiles
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Supprimer les logs Chrome
        
        # Chemin vers chromedriver (utilisez une chaîne brute)
        service = Service(r'chromedriver/chromedriver.exe')  # Remplacez par le chemin de votre chromedriver
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Charger la page
        driver.get(url)
        time.sleep(5)  # Attendre que la page se charge (ajuster le temps si nécessaire)

        # Récupérer le contenu de la page après chargement dynamique
        page_source = driver.page_source

        # Utiliser BeautifulSoup pour parser le HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Trouver les éléments souhaités avec une expression régulière
        dialogues = [line.get_text(strip=True) for line in soup.find_all('div', class_=re.compile(r'dialogue|script|line|text'))]

        # Si aucun dialogue n'est trouvé, essayer d'autres balises ou classes
        if not dialogues:
            dialogues = [line.get_text(strip=True) for line in soup.find_all(['p', 'span'], class_=re.compile(r'dialogue|script|line|text'))]

        # Afficher les dialogues trouvés
        if resultat_game_scripts:
            if dialogues:
                resultat_game_scripts.insert(tk.END, f"Nombre de dialogues trouvés : {len(dialogues)}\n")
                resultat_game_scripts.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
                for index, dialogue in enumerate(dialogues, start=1):
                    # Tronquer le dialogue à 200 caractères pour une meilleure lisibilité
                    truncated_dialogue = (dialogue[:200] + '...') if len(dialogue) > 200 else dialogue
                    # Afficher le dialogue avec un numéro et une séparation visuelle
                    resultat_game_scripts.insert(tk.END, f"Dialogue #{index}:\n{truncated_dialogue}\n")
                    resultat_game_scripts.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
            else:
                resultat_game_scripts.insert(tk.END, "Aucun dialogue trouvé. Vérifiez la structure HTML de la page.\n")
        else:
            if dialogues:
                print(f"Nombre de dialogues trouvés : {len(dialogues)}")
                print("-" * 80)  # Séparateur visuel
                for index, dialogue in enumerate(dialogues, start=1):
                    # Tronquer le dialogue à 200 caractères pour une meilleure lisibilité
                    truncated_dialogue = (dialogue[:200] + '...') if len(dialogue) > 200 else dialogue
                    # Afficher le dialogue avec un numéro et une séparation visuelle
                    print(f"Dialogue #{index}:\n{truncated_dialogue}\n")
                    print("-" * 80)  # Séparateur visuel
            else:
                print("Aucun dialogue trouvé. Vérifiez la structure HTML de la page.")

        # Sauvegarder les données
        if dialogues:
            save_data(dialogues, f"{RAW_DATA_PATH}game_scripts/dialogues.json")

    except Exception as e:
        if resultat_game_scripts:
            resultat_game_scripts.insert(tk.END, f"Erreur lors du scraping : {e}\n")
        else:
            print(f"Erreur lors du scraping : {e}")

    finally:
        # Fermer le navigateur
        driver.quit()
        if resultat_game_scripts:
            resultat_game_scripts.insert(tk.END, "Scraping terminé.\n")
            resultat_game_scripts.see(tk.END)  # Faire défiler vers le bas
        else:
            print("Scraping terminé.")