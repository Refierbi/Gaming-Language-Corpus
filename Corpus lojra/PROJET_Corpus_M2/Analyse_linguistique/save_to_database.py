import os
import pandas as pd
from collections import Counter
from datetime import datetime
import sqlite3
from scripts.utils.config import DATA_PATH


def create_database():
    """
    Crée la base de données et les tables si elles n'existent pas.
    """
    db_path = os.path.join(DATA_PATH, "corpus_gaming.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table pour les fréquences des mots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS frequencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            liste_mots_trouves TEXT NOT NULL,
            top_5_mots TEXT NOT NULL
        )
    """)
    

    # Table pour les motifs extraits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_enregistrement TEXT NOT NULL,
            pattern_recherche TEXT NOT NULL,
            resultat_pattern TEXT NOT NULL
        )
    """)

    conn.commit()
    if conn:
        print("La base de données a été créée avec succès.")
    else:
        print("Erreur lors de la création de la base de données.")
    conn.close()
    
def store_frequencies_in_db(liste_mots_trouves, top_5_mots):
    """
    Stocke les fréquences des mots dans la base de données.
    :param liste_mots_trouves: Chaîne JSON contenant tous les mots trouvés.
    :param top_5_mots: Les 5 mots les plus fréquents.
    """
    db_path = os.path.join(DATA_PATH, "corpus_gaming.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insérer les données dans la table frequencies
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO frequencies (date, liste_mots_trouves, top_5_mots)
        VALUES (?, ?, ?)""", (date, liste_mots_trouves, top_5_mots))

    conn.commit()
    conn.close()


def store_pattern_in_db(pattern_recherche, resultat_pattern):
    """
    Stocke les motifs extraits dans la base de données.
    :param pattern_recherche: Le motif recherché.
    :param resultat_pattern: Résultat de la recherche du motif.
    """
    db_path = os.path.join(DATA_PATH, "corpus_gaming.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insérer les données dans la table patterns
    date_enregistrement = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO patterns (date_enregistrement, pattern_recherche, resultat_pattern)
        VALUES (?, ?, ?)
        """, (date_enregistrement, pattern_recherche, resultat_pattern))
    conn.commit()
    conn.close()
