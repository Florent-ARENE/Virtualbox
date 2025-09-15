## app.py

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

app = Flask(__name__)

# Fonction pour scraper toutes les paires "Nom + Type"
def scrape_chord_name_and_type(string_positions):
    base_url = "https://jguitar.com/chordname"
    params = {f"string{i}": string_positions[i] for i in range(6)}
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    # Trouver toutes les lignes du tableau des résultats
    result_rows = soup.find('table', class_='results').find_all('tr')

    # Extraire toutes les paires "Nom + Type"
    chords = []
    for row in result_rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            chord_root = cells[0].text.strip()
            chord_type = cells[1].text.strip()
            chords.append((chord_root, chord_type))

    return chords

# Fonction pour chercher les images d'un accord spécifique sur une page spécifique
def search_images_for_chord_on_page(chord_name, encoded_positions, page):
    base_url = "https://jguitar.com/chordsearch"
    params = {'chordsearch': chord_name, 'page': page}
    response = requests.get(base_url, params=params)

    # Afficher le numéro de la page pour le debug
    print(f"Recherche sur la page {page} pour l'accord {chord_name}")

    soup = BeautifulSoup(response.content, "html.parser")

    # Chercher toutes les images potentielles sur cette page
    image_elements = soup.find_all('img', src=True)
    images = []

    # Regex mis à jour pour capturer des nombres de plusieurs chiffres
    regex_pattern = re.compile(r"[0-9x]+%2C[0-9x]+%2C[0-9x]+%2C[0-9x]+%2C[0-9x]+%2C[0-9x]+\.png$")

    for img in image_elements:
        if "chordshape" in img['src']:
            full_img_url = f"https://jguitar.com{img['src']}"
            # Vérification avec regex si l'image suit le schéma correct
            if regex_pattern.search(img['src']):
                # Filtrer les images correspondant aux positions exactes des doigts
                if img['src'].endswith(encoded_positions + ".png"):
                    print(f"Image exacte trouvée : {full_img_url}")  # Debug exact match
                    images.append({'match': True, 'url': full_img_url})
                else:
                    print(f"Autre position trouvée : {full_img_url}")  # Debug other position
                    images.append({'match': False, 'url': full_img_url})

    # Si aucune image n'est trouvée, l'indiquer
    if not images:
        print(f"Aucune image trouvée sur la page {page} pour l'accord {chord_name}")

    return images

# Fonction principale pour obtenir toutes les images correspondant aux positions des doigts
def get_chord_images_for_finger_positions(string_positions):
    # Scraper toutes les paires "Nom + Type"
    chords = scrape_chord_name_and_type(string_positions)

    # Encodage des positions pour la fin de l'URL
    encoded_positions = urllib.parse.quote(",".join(string_positions))

    # Chercher les images pour chaque accord trouvé sur un nombre limité de pages
    exact_matches = []
    other_positions = []

    # Boucle à travers chaque accord pour les pages (jusqu'à ce qu'on ne trouve plus d'images pertinentes)
    for chord_root, chord_type in chords:
        page_num = 1
        max_pages_without_results = 0  # Variable pour stopper la recherche après plusieurs pages vides
        while max_pages_without_results < 2:  # On autorise 2 pages vides avant de stopper
            images = search_images_for_chord_on_page(chord_root, encoded_positions, page_num)
            if not images:
                max_pages_without_results += 1
                print(f"Aucune image trouvée pour {chord_root} sur la page {page_num}.")
            else:
                max_pages_without_results = 0  # Réinitialiser le compteur s'il y a des résultats
                # Diviser les images entre exactes et autres
                for img in images:
                    if img['match']:
                        exact_matches.append({'chord_name': chord_root, 'chord_type': chord_type, 'image_url': img['url']})
                    else:
                        other_positions.append({'chord_name': chord_root, 'chord_type': chord_type, 'image_url': img['url']})

            page_num += 1  # Passer à la page suivante

    return exact_matches, other_positions

@app.route('/', methods=['GET', 'POST'])
def index():
    exact_matches = []
    other_positions = []
    error_message = None

    if request.method == 'POST':
        try:
            # Récupérer et valider les positions des doigts depuis le formulaire
            string_positions = []
            for i in range(6):
                value = request.form[f'string{i}'].lower()
                if not re.match(r'^[x0-9]{1,2}$', value) or (value.isdigit() and int(value) > 26):
                    raise ValueError(f"Valeur incorrecte pour la corde {i + 1}")
                string_positions.append(value)
        except (KeyError, ValueError) as e:
            return render_template('index.html', error_message=str(e))

        # Obtenir toutes les images correspondant aux positions des doigts
        exact_matches, other_positions = get_chord_images_for_finger_positions(string_positions)

        # Si aucun accord n'a été trouvé
        if not exact_matches and not other_positions:
            error_message = "Aucun accord trouvé pour les positions de doigts fournies."

    return render_template('index.html', exact_matches=exact_matches, other_positions=other_positions, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
