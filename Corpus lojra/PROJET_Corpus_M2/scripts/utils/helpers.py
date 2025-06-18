import json
import csv
import logging
from pathlib import Path

# Configuration des logs
logging.basicConfig(filename='logs/scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_data(data, file_path):
    """Sauvegarde les données dans un fichier JSON ou CSV."""
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        if file_path.endswith('.json'):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        elif file_path.endswith('.csv'):
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        logging.info(f"Données sauvegardées dans {file_path}")
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des données : {e}")