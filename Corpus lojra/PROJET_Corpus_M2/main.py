
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from collections import Counter
import pandas as pd
import os
import json
from scripts.scraper_articles import scrape_articles
from scripts.scraper_game_script import scrape_game_scripts
from scripts.scraper_reddit import scrape_reddit
from scripts.scraper_twitch import scrape_twitch
from scripts.scraper_twitter import scrape_twitter
from scripts.scraper_youtube import scrape_youtube

from Analyse_linguistique.Analyse_Traitement_donnee import analyze_frequencies, extract_patterns
from Analyse_linguistique.save_to_database import create_database, store_frequencies_in_db, store_pattern_in_db
from Analyse_linguistique.Clean_donnee import clean_data, load_json_files, store_data_to_csv

from Analyse_linguistique.database_corpus_linguistique import fetch_frequencies, fetch_patterns, delete_frequency_entry, delete_pattern_entry, update_frequency_entry, update_pattern_entry

################### Initialisation de la base de données ###################
create_database()

################### Fonction pour lancer le scraping des articles ###################

def lancer_scrape_articles():
    url = url_articles.get()  # Récupérer l'URL saisie par l'utilisateur
    if url:
        resultat_articles.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_articles.insert(tk.END, "Scraping des articles en cours...\n")
        scrape_articles(url, resultat_articles)
    else:
        resultat_articles.insert(tk.END, "Veuillez saisir une URL valide.\n")

# Fonction pour lancer le scraping des scripts de jeux
def lancer_scrape_game_scripts():
    url = url_game_scripts.get()  # Récupérer l'URL saisie par l'utilisateur
    if url:
        resultat_game_scripts.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_game_scripts.insert(tk.END, "Scraping des scripts de jeux en cours...\n")
        scrape_game_scripts(url, resultat_game_scripts)
    else:
        resultat_game_scripts.insert(tk.END, "Veuillez saisir une URL valide.\n")

# Fonction pour lancer le scraping de Reddit
def lancer_scrape_reddit():
    subreddit = subreddit_entry.get()  # Récupérer le subreddit saisi par l'utilisateur
    if subreddit:
        resultat_reddit.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_reddit.insert(tk.END, f"Scraping du subreddit '{subreddit}' en cours...\n")
        scrape_reddit(subreddit, resultat_reddit)
    else:
        resultat_reddit.insert(tk.END, "Veuillez saisir un subreddit valide.\n")

# Fonction pour lancer le scraping de Twitch
def lancer_scrape_twitch():
    game_id = twitch_game_id.get()  # Récupérer l'ID du jeu saisi par l'utilisateur
    if game_id:
        resultat_twitch.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_twitch.insert(tk.END, f"Scraping de Twitch pour le jeu ID '{game_id}' en cours...\n")
        scrape_twitch(game_id, resultat_twitch)
    else:
        resultat_twitch.insert(tk.END, "Veuillez saisir un ID de jeu valide.\n")

# Fonction pour lancer le scraping de Twitter
def lancer_scrape_twitter():
    query = twitter_query.get()  # Récupérer la requête saisie par l'utilisateur
    if query:
        resultat_twitter.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_twitter.insert(tk.END, f"Scraping de Twitter pour la requête '{query}' en cours...\n")
        scrape_twitter(query, resultat_twitter)
    else:
        resultat_twitter.insert(tk.END, "Veuillez saisir une requête valide.\n")

# Fonction pour lancer le scraping de YouTube
def lancer_scrape_youtube():
    video_url = youtube_url.get()  # Récupérer l'URL de la vidéo saisie par l'utilisateur
    language = language_var.get()  # Récupérer la langue sélectionnée par l'utilisateur

    if video_url:
        resultat_youtube.delete(1.0, tk.END)  # Effacer le contenu précédent
        resultat_youtube.insert(tk.END, f"Scraping de YouTube pour la vidéo '{video_url}' en cours...\n")
        resultat_youtube.insert(tk.END, f"Langue des sous-titres : {language}\n")
        resultat_youtube.update()  # Mettre à jour l'interface pour afficher le message

        # Lancer le scraping avec la langue spécifiée
        scrape_youtube(video_url, resultat_youtube, language=language)
    else:
        resultat_youtube.insert(tk.END, "Veuillez saisir une URL de vidéo valide.\n")
        
##################################### Fonction pour Analyse et traitement des données ##################################

#Fonction pour nettoyer et sauvegarder les données en CSV

def clean_and_save_to_csv():
    # Ouvrir le dossier donnees/raw pour sélectionner les fichiers JSON
    input_files = filedialog.askopenfilenames(
        initialdir=os.path.join("donnees", "raw"),  # Dossier initial pour la sélection
        title="Sélectionnez les fichiers JSON à nettoyer",
        filetypes=[("Fichiers JSON", "*.json")]
    )
    
    if input_files:
        # Ouvrir le dossier donnees/processed pour sauvegarder le fichier CSV
        output_file = filedialog.asksaveasfilename(
            initialdir=os.path.join("donnees", "processed"),  # Dossier initial pour la sauvegarde
            title="Sauvegarder le fichier CSV nettoyé",
            defaultextension=".csv",
            filetypes=[("Fichiers CSV", "*.csv")]
        )
        
        if output_file:
            resultat_analyse.delete(1.0, tk.END)
            resultat_analyse.insert(tk.END, "Nettoyage et sauvegarde des données en cours...\n")
            
            # Nettoyer les données et les sauvegarder dans un fichier temporaire
            clean_data(input_files, 'temp_cleaned.json', resultat_analyse)
            
            # Sauvegarder les données nettoyées dans le fichier CSV
            store_data_to_csv('temp_cleaned.json', output_file, resultat_analyse)
            
            resultat_analyse.insert(tk.END, "Données nettoyées et sauvegardées avec succès.\n")
        else:
            messagebox.showwarning("Avertissement", "Veuillez spécifier un fichier de sortie.")
    else:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un fichier JSON.")

# Fonction pour analyser les fréquences des mots-clés
def analyser_frequences():
    fichier_csv = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
    if fichier_csv:
        resultat_analyse.delete(1.0, tk.END)
        resultat_analyse.insert(tk.END, "Analyse des fréquences en cours...\n")
        analyze_frequencies(fichier_csv, resultat_analyse)
    afficher_frequences()  # Afficher les données au démarrage

# Fonction pour extraire des patterns spécifiques
def extraire_patterns():
    fichier_csv = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
    pattern = pattern_entry.get()
    if fichier_csv and pattern:
        resultat_analyse.delete(1.0, tk.END)
        resultat_analyse.insert(tk.END, f"Extraction des patterns pour '{pattern}' en cours...\n")
        extract_patterns(fichier_csv, pattern, resultat_analyse)
    afficher_patterns()  # Afficher les données au démarrage
            

##################################### Interface Graphique ##################################

# Création de la fenêtre principale
root = tk.Tk()
root.title("Scraping de Données Gaming pour traitement linguistique NLP by Refierbi Ibro")
window_width = 980
window_height = 600

# Définir l'icône de la fenêtre (fichier ICO)
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Répertoire du script actuel
    logo_path = os.path.join(script_dir, "logo.ico")  # Chemin vers le fichier ICO

    if os.path.exists(logo_path):
        root.iconbitmap(logo_path)  # Définir l'icône de la fenêtre
    else:
        print(f"Le fichier {logo_path} n'existe pas. L'icône par défaut sera utilisée.")
except Exception as e:
    print(f"Erreur lors du chargement de l'icône : {e}")

root.geometry(f"{window_width}x{window_height}")

# Centrer la fenêtre au milieu de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = int((screen_width / 2) - (window_width / 2))
y_position = int((screen_height / 2) - (window_height / 2))
root.geometry(f"+{x_position}+{y_position}")

# Création d'un Notebook (onglets)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Onglet pour les articles
frame_articles = ttk.Frame(notebook)
notebook.add(frame_articles, text="  Articles  " )

# Champ de saisie pour l'URL des articles
url_articles_label = tk.Label(frame_articles, text="URL de la page à scraper :")
url_articles_label.pack(pady=5)
url_articles = tk.Entry(frame_articles, width=100)
url_articles.insert(0, "https://www.gameblog.fr/")
url_articles.pack(pady=10)

# Bouton pour lancer le scraping des articles
btn_articles = tk.Button(frame_articles, text="Lancer le Scraping", width=30, command=lancer_scrape_articles, bg="#673AB7", fg="white")
btn_articles.pack(pady=10)

# Zone de texte pour afficher les résultats des articles
resultat_articles = scrolledtext.ScrolledText(frame_articles, wrap=tk.WORD, width=100, height=20)
resultat_articles.pack(pady=10)

# Onglet pour les scripts de jeux
frame_game_scripts = ttk.Frame(notebook)
notebook.add(frame_game_scripts, text="  Scripts de Jeux  ")

# Champ de saisie pour l'URL des scripts de jeux
url_game_scripts_label = tk.Label(frame_game_scripts, text="URL de la page à scraper :")
url_game_scripts_label.pack(pady=5)
url_game_scripts = tk.Entry(frame_game_scripts, width=100)
url_game_scripts.insert(0, "https://assetstore.unity.com/")
url_game_scripts.pack(pady=10)

# Bouton pour lancer le scraping des scripts de jeux
btn_game_scripts = tk.Button(frame_game_scripts, text="Lancer le Scraping", width=30, command=lancer_scrape_game_scripts, bg="#2196F3", fg="white")
btn_game_scripts.pack(pady=10)

# Zone de texte pour afficher les résultats des scripts de jeux
resultat_game_scripts = scrolledtext.ScrolledText(frame_game_scripts, wrap=tk.WORD, width=100, height=20)
resultat_game_scripts.pack(pady=10)

# Onglet pour Reddit
frame_reddit = ttk.Frame(notebook)
notebook.add(frame_reddit, text="  Reddit  ")

# Champ de saisie pour le subreddit
subreddit_label = tk.Label(frame_reddit, text="Nom du subreddit :")
subreddit_label.pack(pady=5)
subreddit_entry = tk.Entry(frame_reddit, width=100)
subreddit_entry.insert(0, "leagueoflegends")
subreddit_entry.pack(pady=10)

# Bouton pour lancer le scraping de Reddit
btn_reddit = tk.Button(frame_reddit, text="Lancer le Scraping", width=30, command=lancer_scrape_reddit, bg="#FF9800", fg="white")
btn_reddit.pack(pady=10)

# Zone de texte pour afficher les résultats de Reddit
resultat_reddit = scrolledtext.ScrolledText(frame_reddit, wrap=tk.WORD, width=100, height=20)
resultat_reddit.pack(pady=10)

# Onglet pour Twitch
frame_twitch = ttk.Frame(notebook)
notebook.add(frame_twitch, text="  Twitch  ")

# Champ de saisie pour l'ID du jeu sur Twitch
twitch_game_id_label = tk.Label(frame_twitch, text="ID du jeu sur Twitch :")
twitch_game_id_label.pack(pady=5)
twitch_game_id = tk.Entry(frame_twitch, width=100)
twitch_game_id.insert(0, "21779")
twitch_game_id.pack(pady=10)

# Bouton pour lancer le scraping de Twitch
btn_twitch = tk.Button(frame_twitch, text="Lancer le Scraping", width=30, command=lancer_scrape_twitch, bg="#9C27B0", fg="white")
btn_twitch.pack(pady=10)

# Zone de texte pour afficher les résultats de Twitch
resultat_twitch = scrolledtext.ScrolledText(frame_twitch, wrap=tk.WORD, width=100, height=20)
resultat_twitch.pack(pady=10)

# Onglet pour Twitter
frame_twitter = ttk.Frame(notebook)
notebook.add(frame_twitter, text="  Twitter  ")

# Champ de saisie pour la requête Twitter
twitter_query_label = tk.Label(frame_twitter, text="Requête Twitter :")
twitter_query_label.pack(pady=5)
twitter_query = tk.Entry(frame_twitter, width=100)
twitter_query.insert(0, "#leagueoflegends")
twitter_query.pack(pady=10)

# Bouton pour lancer le scraping de Twitter
btn_twitter = tk.Button(frame_twitter, text="Lancer le Scraping", width=30, command=lancer_scrape_twitter, bg="#00BCD4", fg="white")
btn_twitter.pack(pady=10)

# Zone de texte pour afficher les résultats de Twitter
resultat_twitter = scrolledtext.ScrolledText(frame_twitter, wrap=tk.WORD, width=100, height=20)
resultat_twitter.pack(pady=10)

# Onglet pour YouTube
frame_youtube = ttk.Frame(notebook)
notebook.add(frame_youtube, text="  YouTube  ")

# Champ de saisie pour l'URL de la vidéo YouTube
youtube_url_label = tk.Label(frame_youtube, text="Coller l'URL de la vidéo YouTube :")
youtube_url_label.pack(pady=5)
youtube_url = tk.Entry(frame_youtube, width=100)
youtube_url.insert(0, "https://www.youtube.com/watch?v=n_dZEx4amw4&ab_channel=C'estcadeau!C'estgratuit!") 
youtube_url.pack(pady=10)

# Menu déroulant pour choisir la langue des sous-titres
language_label = tk.Label(frame_youtube, text="Langue des sous-titres :")
language_label.pack(pady=5)

# Utiliser la variable globale language_var
language_var = tk.StringVar(value='fr')  # Langue par défaut : français
language_menu = ttk.Combobox(frame_youtube, textvariable=language_var, values=['fr', 'en', 'es', 'de'])
language_menu.pack(pady=5)

# Bouton pour lancer le scraping de YouTube
btn_youtube = tk.Button(frame_youtube, text="Lancer le Scraping", width=30, command=lancer_scrape_youtube, bg="#F44336", fg="white")
btn_youtube.pack(pady=10)

# Zone de texte pour afficher les résultats de YouTube
resultat_youtube = scrolledtext.ScrolledText(frame_youtube, wrap=tk.WORD, width=100, height=20)
resultat_youtube.pack(pady=10)


##################################### Onglet pour le traitement et l'analyse des données ##################################

frame_analyse = ttk.Frame(notebook)
notebook.add(frame_analyse, text="  Traitement et Analyse - Corpus linguistique  ")

# Bouton pour nettoyer et sauvegarder les données en CSV
btn_clean_save = tk.Button(frame_analyse, text="Clean et Sauvegarder en CSV", width=30, command=clean_and_save_to_csv, bg="#607D8B", fg="white")
btn_clean_save.pack(pady=10)

# Bouton pour analyser les fréquences des mots-clés
btn_frequences = tk.Button(frame_analyse, text="Analyser les Fréquences", width=30, command=analyser_frequences, bg="#4CAF50", fg="white")
btn_frequences.pack(pady=10)

# Champ de saisie pour le pattern à extraire
pattern_label = tk.Label(frame_analyse, text="Pattern à extraire :")
pattern_label.pack(pady=5)
pattern_entry = tk.Entry(frame_analyse, width=100)
pattern_entry.pack(pady=10)

# Bouton pour extraire des patterns spécifiques
btn_patterns = tk.Button(frame_analyse, text="Extraire des Patterns", width=30, command=extraire_patterns, bg="#FF5722", fg="white")
btn_patterns.pack(pady=10)

# Zone de texte pour afficher les résultats de l'analyse
resultat_analyse = scrolledtext.ScrolledText(frame_analyse, wrap=tk.WORD, width=100, height=20)
resultat_analyse.pack(pady=10)

########################################### RESULTAT CORPUS POUR NLP #########################################

# Onglet pour le résultat corpus pour NLP
frame_corpus_nlp = ttk.Frame(notebook)
notebook.add(frame_corpus_nlp, text="  Résultat Corpus pour NLP  ")

# Division du cadre en deux colonnes : Tableaux à gauche, Boutons à droite
frame_left = ttk.Frame(frame_corpus_nlp)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

frame_right = ttk.Frame(frame_corpus_nlp)
frame_right.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Tableau pour afficher les fréquences des mots (Treeview)
table_frequences = ttk.Treeview(frame_left, columns=("ID", "Date", "Mots Trouvés", "Top 5 Mots"), show="headings")
table_frequences.heading("ID", text="ID")
table_frequences.heading("Date", text="Date")
table_frequences.heading("Mots Trouvés", text="Mots Trouvés")
table_frequences.heading("Top 5 Mots", text="Top 5 Mots")
table_frequences.column("ID", width=50)
table_frequences.column("Date", width=150)
table_frequences.column("Mots Trouvés", width=300)
table_frequences.column("Top 5 Mots", width=300)
table_frequences.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

# Tableau pour afficher les patterns extraits (Treeview)
table_patterns = ttk.Treeview(frame_left, columns=("ID", "Date", "Pattern Recherché", "Résultat"), show="headings")
table_patterns.heading("ID", text="ID")
table_patterns.heading("Date", text="Date")
table_patterns.heading("Pattern Recherché", text="Pattern Recherché")
table_patterns.heading("Résultat", text="Résultat")
table_patterns.column("ID", width=50)
table_patterns.column("Date", width=150)
table_patterns.column("Pattern Recherché", width=200)
table_patterns.column("Résultat", width=400)
table_patterns.pack(fill=tk.BOTH, expand=True)

# Fonction pour afficher les fréquences des mots dans le tableau
def afficher_frequences():
    table_frequences.delete(*table_frequences.get_children())  # Effacer les données précédentes
    rows = fetch_frequencies()
    if rows:
        for row in rows:
            table_frequences.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Info", "Aucune donnée disponible dans la table 'frequencies'.")

btn_afficher_frequences = tk.Button(frame_right, text="Afficher Fréquences", command=afficher_frequences, bg="#4CAF50", fg="white", width=20)
btn_afficher_frequences.pack(pady=5)

# Fonction pour afficher les patterns extraits dans le tableau
def afficher_patterns():
    table_patterns.delete(*table_patterns.get_children())  # Effacer les données précédentes
    rows = fetch_patterns()
    if rows:
        for row in rows:
            table_patterns.insert("", tk.END, values=row)
    else:
        messagebox.showinfo("Info", "Aucune donnée disponible dans la table 'patterns'.")

btn_afficher_patterns = tk.Button(frame_right, text="Afficher Patterns", command=afficher_patterns, bg="#FF9800", fg="white", width=20)
btn_afficher_patterns.pack(pady=5)

# Champ pour entrer l'ID de l'entrée à supprimer
id_label = tk.Label(frame_right, text="Entrer ID à supprimer :")
id_label.pack(pady=5)
id_entry = tk.Entry(frame_right, width=30)
id_entry.pack(pady=5)

# Bouton pour supprimer une entrée de la table 'frequencies'
def supprimer_frequences():
    entry_id = id_entry.get()
    if entry_id:
        try:
            delete_frequency_entry(entry_id)
            messagebox.showinfo("Succès", f"Entrée avec ID {entry_id} supprimée de la table 'frequencies'.")
            afficher_frequences()  # Rafraîchir les données
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

btn_supprimer_frequences = tk.Button(frame_right, text="Supprimer Fréquence", command=supprimer_frequences, bg="#F44336", fg="white", width=20)
btn_supprimer_frequences.pack(pady=5)

# Bouton pour supprimer une entrée de la table 'patterns'
def supprimer_patterns():
    entry_id = id_entry.get()
    if entry_id:
        try:
            delete_pattern_entry(entry_id)
            messagebox.showinfo("Succès", f"Entrée avec ID {entry_id} supprimée de la table 'patterns'.")
            afficher_patterns()  # Rafraîchir les données
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

btn_supprimer_patterns = tk.Button(frame_right, text="Supprimer Pattern", command=supprimer_patterns, bg="#F44336", fg="white", width=20)
btn_supprimer_patterns.pack(pady=5)

# Champ pour entrer les nouvelles données
update_label = tk.Label(frame_right, text="Modifier Entrée (JSON):")
update_label.pack(pady=5)
update_entry = tk.Entry(frame_right, width=30)
update_entry.pack(pady=5)

# Bouton pour mettre à jour une entrée de la table 'frequencies'
def modifier_frequences():
    entry_id = id_entry.get()
    new_data_json = update_entry.get()
    try:
        new_data = json.loads(new_data_json)
        if all(key in new_data for key in ['date', 'liste_mots_trouves', 'top_5_mots']):
            update_frequency_entry(entry_id, new_data)
            messagebox.showinfo("Succès", f"Entrée avec ID {entry_id} mise à jour.")
            afficher_frequences()  # Rafraîchir les données
        else:
            messagebox.showwarning("Avertissement", "Données JSON incomplètes. Assurez-vous d'inclure 'date', 'liste_mots_trouves' et 'top_5_mots'.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_modifier_frequences = tk.Button(frame_right, text="Modifier Fréquence", command=modifier_frequences, bg="#2196F3", fg="white", width=20)
btn_modifier_frequences.pack(pady=5)

# Bouton pour mettre à jour une entrée de la table 'patterns'
def modifier_patterns():
    entry_id = id_entry.get()
    new_data_json = update_entry.get()
    try:
        new_data = json.loads(new_data_json)
        if all(key in new_data for key in ['date_enregistrement', 'pattern_recherche', 'resultat_pattern']):
            update_pattern_entry(entry_id, new_data)
            messagebox.showinfo("Succès", f"Entrée avec ID {entry_id} mise à jour.")
            afficher_patterns()  # Rafraîchir les données
        else:
            messagebox.showwarning("Avertissement", "Données JSON incomplètes. Assurez-vous d'inclure 'date_enregistrement', 'pattern_recherche' et 'resultat_pattern'.")
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

btn_modifier_patterns = tk.Button(frame_right, text="Modifier Pattern", command=modifier_patterns, bg="#2196F3", fg="white", width=20)
btn_modifier_patterns.pack(pady=5)

afficher_frequences()  # Afficher les données au démarrage
afficher_patterns()  # Afficher les données au démarrage

# Lancer l'interface
root.mainloop()