# Projet Cardell Corpus

## Objectif
Ce projet vise à constituer un corpus de données linguistiques dans le domaine du gaming. Il extrait, traite et organise des données textuelles provenant de diverses sources pour une analyse linguistique approfondie.

## Installation de Python et Virtualenv
Avant de commencer, assurez-vous d'avoir Python installé sur votre système.

1. **Vérifier la version de Python** :
    
   python --version
    
   Si Python n'est pas installé, téléchargez-le depuis [python.org](https://www.python.org/downloads/).

2. **Mettre à jour `pip`** :
    
   python -m pip install --upgrade pip
    

3. **Installer Virtualenv** :
    
   pip install virtualenv
    

4. **Créer et activer un environnement virtuel** :
    
   python -m venv env
   env\Scripts\activate  # Sur Windows
   source env/bin/activate  # Sur Mac/Linux
    

## Installation des dépendances
Une fois l'environnement virtuel activé :

1. **Installer les dépendances** :
    
   pip install -r Requirements.txt
    
2. **Vérifier les paquets installés** :
    
   pip list
    
3. **Générer une liste des dépendances utilisées** :
    
   pip freeze > Requirements.txt
    

## Lancer le script principal
Exécuter le script de traitement :
 
python main.py
 

## Explication du processus de scraping
Le projet utilise des scripts de scraping pour extraire des données linguistiques du domaine du gaming. Voici un aperçu du processus :

1. **Collecte des données** :
   - Les scripts de `scripts/` envoient des requêtes HTTP aux sources définies.
   - Utilisation de bibliothèques comme `requests` et `BeautifulSoup` pour récupérer et analyser le contenu HTML.
   
2. **Nettoyage des données** :
   - Suppression des balises HTML et extraction du texte pertinent.
   - Normalisation des données (conversion en minuscules, suppression des caractères spéciaux).

3. **Stockage des données** :
   - Les données sont enregistrées dans plusieurs formats :
     - **CSV (`corpus_final.csv`)** : Données tabulaires prêtes pour analyse.
     - **JSON (`corpus_gaming.json`)** : Format structuré pour le traitement automatisé.
     - **Base de données SQLite (`corpus_gaming.db`)** : Stockage relationnel pour requêtes avancées.

4. **Traitement et analyse** :
   - Analyse des fréquences de mots-clés.
   - Extraction d'expressions et de patterns spécifiques au gaming.
   - Préparation des données pour l'entraînement de modèles NLP.

## Désactiver l'environnement virtuel
 
deactivate
 

