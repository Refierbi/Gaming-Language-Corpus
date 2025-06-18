# Gaming Language Corpus

A multilingual corpus of gaming-related language collected from various online platforms such as Reddit, Twitter, YouTube, Twitch, and gaming scripts.

This project contains data, scraping scripts, and linguistic analysis tools designed for studying the influence of English gaming language on other languages like French and German.

---

## Project Overview

- **Languages Covered:** English, French, German,  
- **Data Sources:** Social media (Reddit, Twitter, YouTube, Twitch), game scripts, articles  
- **Purpose:** To create a corpus for linguistic analysis of gaming terminology and language mixing in multilingual contexts via virtual environment 

---

## Folder Structure

- `donnees/`  
  Contains raw and processed datasets including CSV, JSON, and database files.

- `scripts/`  
  Python scripts to scrape data from different sources:
  - `scraper_reddit.py`  
  - `scraper_twitter.py`  
  - `scraper_youtube.py`  
  - `scraper_twitch.py`  
  - `scraper_articles.py`  
  - `scraper_game_script.py`  

- `Analyse_linguistique/`  
  Scripts for linguistic processing and data cleaning.

- `main.py`  
  The main entry script to run different parts of the corpus processing pipeline.

- `requirements.txt`  
  List of Python dependencies.

---

## Installation

Make sure you have Python 3.7+ installed. Then install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

Run `main.py` to execute the main processing workflow:

```bash
python main.py
```

You can explore individual scraper scripts in the `scripts/` folder to collect or update data.

---

## Author

Refierbi Ibro — Master's Student in Automatic Language Treatment (ALTI)  
Contact: [refierbi.ibro@gmail.com]

---

## License

( MIT License).

---

## Acknowledgments

Thanks to open source contributors and platforms that provide APIs for data collection.
