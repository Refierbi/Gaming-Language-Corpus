import os
import json
import tkinter as tk
from collections import Counter
import pandas as pd
from scripts.utils.config import DATA_PATH
from scripts.utils.helpers import save_data
from Analyse_linguistique.save_to_database import create_database, store_frequencies_in_db, store_pattern_in_db

def analyze_frequencies(csv_file, resultat_analyse=None):
    """
    Analyse les fréquences des mots liés aux jeux ou mods dans un fichier CSV contenant une colonne 'text'.

    :param csv_file: Chemin vers le fichier CSV.
    :param resultat_analyse: Widget Tkinter (optionnel) pour afficher les résultats.
    """
    try:
        # Vérifier l'existence du fichier
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Le fichier {csv_file} n'existe pas.")
        
        # Charger les données
        df = pd.read_csv(csv_file)
        
        # Vérifier si la colonne 'text' existe
        if 'text' not in df.columns:
            raise KeyError("La colonne 'text' est manquante dans le fichier CSV.")
        
        # Concaténer tous les textes en un seul bloc
        all_text = ' '.join(df['text'].dropna().astype(str).tolist())
        
        # Diviser le texte en mots et compter leur fréquence
        words = all_text.split()
        word_freq = Counter(words)
        
        # Définir une liste de mots clés liés aux jeux ou mods
        game_related_keywords = {
            "jeu", "jeux", "mod", "mods", "joueur", "joueurs", "niveau", "carte", "personnage",
            "équipe", "mission", "quête", "arme", "armes", "skins", "classe", "classes",
            "serveur", "serveurs", "update", "patch", "dlc", "game", "games", "modding",
            "gamer", "gaming", "level", "map", "character", "team", "mission", "quest",
            "weapon", "weapons", "skin", "skins", "class", "classes", "server", "servers",
            "download", "online", "offline", "multiplayer", "singleplayer", "fps", "rpg",
            "mmo", "moba", "strategy", "puzzle", "adventure", "platformer", "shooter",
            "survival", "horror", "sandbox", "openworld", "story", "lore", "npc", "ai",
            "crafting", "loot", "drops", "xp", "experience", "points", "score", "leaderboard",
            "achievements", "trophies", "unlockables", "expansion", "season", "pass",
            "battlepass", "cosmetics", "customization", "perks", "abilities", "skills",
            "stats", "statistics", "inventory", "shop", "marketplace", "trading", "currency",
            "gold", "coins", "gems", "resources", "buildings", "structures", "base", "camp",
            "city", "town", "village", "kingdom", "empire", "faction", "alliance", "guild",
            "clan", "pvp", "pve", "raiding", "dungeon", "boss", "miniboss", "combat",
            "melee", "ranged", "magic", "spells", "potions", "healing", "damage", "health",
            "mana", "energy", "stamina", "cooldown", "timer", "turn", "round", "phase",
            "wave", "spawn", "respawn", "death", "revive", "save", "load", "checkpoint",
            "progression", "leveling", "upgrading", "enhancement", "equipment", "gear",
            "armor", "shield", "helmet", "boots", "gloves", "cape", "amulet", "ring",
            "accessory", "vehicle", "mount", "pet", "companion", "ally", "enemy", "mob",
            "monster", "creature", "beast", "dragon", "zombie", "skeleton", "undead",
            "alien", "robot", "cyborg", "spaceship", "starship", "planet", "galaxy",
            "universe", "space", "exploration", "discovery", "science", "technology",
            "magic", "fantasy", "sci-fi", "scifi", "stealth", "espionnage", "puzzle",
            "énigme", "défi", "challenge", "objectif", "goal", "objectifs", "goals",
            "victory", "défaite", "win", "lose", "rank", "ranking", "tier", "league",
            "competition", "tournament", "event", "seasonal", "holiday", "festive",
            "limitedtime", "exclusive", "rare", "epic", "legendary", "mythic", "unique"
        }
        
        # Filtrer les mots en fonction des mots-clés liés aux jeux ou mods
        filtered_word_freq = {word: freq for word, freq in word_freq.items() if word.lower() in game_related_keywords}
        
        # Préparer les résultats
        output = "Fréquences des mots-clés liés aux jeux ou mods :\n"
        if filtered_word_freq:
            for word, freq in filtered_word_freq.items():
                output += f"{word}: {freq}\n"
            liste_mots_trouves = json.dumps(filtered_word_freq)
            
            filtered_word_freq_counter = Counter(filtered_word_freq)

            # Extraire les 10 mots les plus fréquents
            top_10_mots = ", ".join([f"{word}:{freq}" for word, freq in filtered_word_freq_counter.most_common(10)])
            store_frequencies_in_db(liste_mots_trouves, top_10_mots)
        
        else:
            output += "Aucun mot clé lié aux jeux ou mods trouvé.\n"
            liste_mots_trouves = json.dumps({})
            top_10_mots = "Aucun mot trouvé."
        
        # Afficher les résultats
        if resultat_analyse:
            resultat_analyse.delete(1.0, tk.END)  # Effacer le contenu précédent
            resultat_analyse.insert(tk.END, output)
            resultat_analyse.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
        else:
            print(output)
        
        # Enregistrer les résultats dans une base de données
        # save_data(output, f"{DATA_PATH}corpus_gaming_frequencies_filtered.txt")
       

    except Exception as e:
        error_message = f"Erreur lors de l'analyse des fréquences : {str(e)}"
        if resultat_analyse:
            resultat_analyse.insert(tk.END, error_message + "\n")
        else:
            print(error_message)

import re

def extract_patterns(csv_file, pattern, resultat_analyse=None):
    """
    Extrait les lignes contenant un motif spécifique dans un fichier CSV, avec 10 mots maximum autour du motif.

    :param csv_file: Chemin vers le fichier CSV.
    :param pattern: Motif à rechercher dans la colonne 'text'.
    :param resultat_analyse: Widget Tkinter (optionnel) pour afficher les résultats.
    """
    try:
        # Charger les données
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"Le fichier {csv_file} n'existe pas.")
        
        df = pd.read_csv(csv_file)
        
        # Vérifier si la colonne 'text' existe
        if 'text' not in df.columns:
            raise KeyError("La colonne 'text' est manquante dans le fichier CSV.")
        
        # Convertir tous les éléments de la colonne 'text' en chaînes de caractères
        df['text'] = df['text'].astype(str)
        
        # Rechercher les lignes contenant le motif
        matches = df[df['text'].str.contains(pattern, na=False, case=False, regex=True)]
        
        # Préparer les résultats
        output = f"Expressions contenant le pattern '{pattern}' (avec 6 mots maximum autour) :\n"
        extracted_results = []

        if not matches.empty:
            for match in matches['text']:
                # Utiliser une expression régulière pour extraire 10 mots avant et après le motif
                regex_pattern = r"(?:\b\w+\b\s*){0,6}\b" + re.escape(pattern) + r"\b(?:\s*\b\w+\b){0,6}"
                results = re.findall(regex_pattern, match, re.IGNORECASE)
                
                # Ajouter les résultats au texte de sortie
                for result in results:
                    # Supprimer les retours à la ligne et les espaces multiples
                    cleaned_result = re.sub(r'\s+', ' ', result.strip())
                    extracted_results.append(cleaned_result)
                    output += f"{cleaned_result}\n"
        else:
            output += "Aucune correspondance trouvée.\n"
        
        # Afficher les résultats
        if resultat_analyse:
            resultat_analyse.delete(1.0, tk.END)  # Effacer le contenu précédent
            resultat_analyse.insert(tk.END, output)
            resultat_analyse.insert(tk.END, "-" * 80 + "\n")  # Séparateur visuel
        else:
            print(output)
        
        # Stocker les résultats dans la base de données
        store_pattern_in_db(pattern, "\n".join(extracted_results))

    except Exception as e:
        error_message = f"Erreur lors de l'extraction des motifs : {str(e)}"
        if resultat_analyse:
            resultat_analyse.insert(tk.END, error_message + "\n")
        else:
            print(error_message)