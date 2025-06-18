import sqlite3
import os
from scripts.utils.config import DATA_PATH

DB_PATH = os.path.join(DATA_PATH, "corpus_gaming.db")

def fetch_frequencies():
    """
    Récupère toutes les entrées de la table 'frequencies'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM frequencies")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_patterns():
    """
    Récupère toutes les entrées de la table 'patterns'.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patterns")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_frequency_entry(entry_id):
    """
    Supprime une entrée de la table 'frequencies' par ID.
    :param entry_id: ID de l'entrée à supprimer.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM frequencies WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def delete_pattern_entry(entry_id):
    """
    Supprime une entrée de la table 'patterns' par ID.
    :param entry_id: ID de l'entrée à supprimer.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patterns WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

def update_frequency_entry(entry_id, new_data):
    """
    Met à jour une entrée de la table 'frequencies'.
    :param entry_id: ID de l'entrée à mettre à jour.
    :param new_data: Nouveaux données (dictionnaire contenant 'date', 'liste_mots_trouves', 'top_5_mots').
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE frequencies 
        SET date=?, liste_mots_trouves=?, top_5_mots=?
        WHERE id=?
    """, (new_data['date'], new_data['liste_mots_trouves'], new_data['top_5_mots'], entry_id))
    conn.commit()
    conn.close()

def update_pattern_entry(entry_id, new_data):
    """
    Met à jour une entrée de la table 'patterns'.
    :param entry_id: ID de l'entrée à mettre à jour.
    :param new_data: Nouveaux données (dictionnaire contenant 'date_enregistrement', 'pattern_recherche', 'resultat_pattern').
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patterns 
        SET date_enregistrement=?, pattern_recherche=?, resultat_pattern=?
        WHERE id=?
    """, (new_data['date_enregistrement'], new_data['pattern_recherche'], new_data['resultat_pattern'], entry_id))
    conn.commit()
    conn.close()