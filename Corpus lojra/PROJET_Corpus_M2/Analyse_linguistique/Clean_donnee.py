import os
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from scripts.utils.config import DATA_PATH
import tkinter as tk


def load_json_files(base_dir):
    """
    Charge tous les fichiers JSON dans un dossier donné.
    :param base_dir: Chemin vers le dossier contenant les fichiers JSON.
    :return: Liste des chemins vers les fichiers JSON.
    """
    json_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def clean_text(text, resultat_analyse=None):
    """
    Nettoie une chaîne de texte en supprimant les balises HTML et en normalisant.
    :param text: Chaîne de texte brute.
    :param resultat_analyse: Widget Tkinter pour afficher les messages (optionnel).
    :return: Chaîne de texte nettoyée.
    """
    if not isinstance(text, str):
        if resultat_analyse:
            resultat_analyse.insert(tk.END, f"Élément non valide détecté : {text}. Ignoré.\n")
        return ""

    # Suppression des balises HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Normalisation des données
    text = text.lower()  # Conversion en minuscules
    text = re.sub(r'[^\w\s]', '', text)  # Suppression des caractères spéciaux

    if resultat_analyse:
        resultat_analyse.insert(tk.END, f"Texte nettoyé : {text[:50]}...\n")
    return text


def clean_data(input_files, output_file, resultat_analyse=None):
    """
    Nettoie les données extraites des fichiers JSON et les sauvegarde dans un fichier JSON.
    :param input_files: Liste des chemins vers les fichiers JSON à nettoyer.
    :param output_file: Chemin vers le fichier JSON de sortie.
    :param resultat_analyse: Widget Tkinter pour afficher les messages (optionnel).
    """
    cleaned_data = []

    for input_file in input_files:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if resultat_analyse:
                resultat_analyse.insert(tk.END, f"Traitement du fichier : {input_file}\n")

            if isinstance(data, list):  # Si les données sont une liste
                for item in data:
                    if isinstance(item, str):  # Si l'élément est une chaîne
                        cleaned_item = clean_text(item, resultat_analyse)
                        if cleaned_item:
                            cleaned_data.append(cleaned_item)
                    elif isinstance(item, dict):  # Si l'élément est un dictionnaire
                        for value in item.values():
                            if isinstance(value, str):
                                cleaned_item = clean_text(value, resultat_analyse)
                                if cleaned_item:
                                    cleaned_data.append(cleaned_item)
            elif isinstance(data, dict):  # Si les données sont un dictionnaire
                for value in data.values():
                    if isinstance(value, str):
                        cleaned_item = clean_text(value, resultat_analyse)
                        if cleaned_item:
                            cleaned_data.append(cleaned_item)
            else:
                if resultat_analyse:
                    resultat_analyse.insert(tk.END, f"Format non pris en charge dans {input_file}. Ignorer ce fichier.\n")

        except Exception as e:
            if resultat_analyse:
                resultat_analyse.insert(tk.END, f"Erreur lors du traitement de {input_file} : {e}\n")
            else:
                print(f"Erreur lors du traitement de {input_file} : {e}")

    # Sauvegarder les données nettoyées dans un fichier JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

    if resultat_analyse:
        resultat_analyse.insert(tk.END, "Données nettoyées et sauvegardées avec succès.\n")


def store_data_to_csv(json_file, csv_file, resultat_analyse=None):
    """
    Convertit un fichier JSON nettoyé en CSV.
    :param json_file: Chemin vers le fichier JSON nettoyé.
    :param csv_file: Chemin vers le fichier CSV de sortie.
    :param resultat_analyse: Widget Tkinter pour afficher les messages (optionnel).
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        df = pd.DataFrame(data, columns=["text"])
        df.to_csv(csv_file, index=False, encoding="utf-8")

        if resultat_analyse:
            resultat_analyse.insert(tk.END, f"Données converties en CSV et sauvegardées dans {csv_file}.\n")
    except Exception as e:
        if resultat_analyse:
            resultat_analyse.insert(tk.END, f"Erreur lors de la conversion en CSV : {e}\n")
        else:
            print(f"Erreur lors de la conversion en CSV : {e}")


def clean_and_save_to_csv(base_dir, output_file, resultat_analyse=None):
    """
    Nettoie les données des fichiers JSON dans un dossier et les sauvegarde dans un fichier CSV.
    :param base_dir: Chemin vers le dossier contenant les fichiers JSON.
    :param output_file: Chemin vers le fichier CSV de sortie.
    :param resultat_analyse: Widget Tkinter pour afficher les messages (optionnel).
    """
    if resultat_analyse:
        resultat_analyse.delete(1.0, tk.END)
        resultat_analyse.insert(tk.END, "Nettoyage et sauvegarde des données en cours...\n")

    # Charger tous les fichiers JSON
    input_files = load_json_files(base_dir)

    if not input_files:
        if resultat_analyse:
            resultat_analyse.insert(tk.END, "Aucun fichier JSON trouvé dans le dossier spécifié.\n")
        return

    # Nettoyer les données et les sauvegarder dans un fichier temporaire
    temp_cleaned_file = 'temp_cleaned.json'
    clean_data(input_files, temp_cleaned_file, resultat_analyse)

    # Convertir les données nettoyées en CSV
    store_data_to_csv(temp_cleaned_file, output_file, resultat_analyse)

    if resultat_analyse:
        resultat_analyse.insert(tk.END, "Processus de nettoyage et de sauvegarde terminé avec succès.\n")