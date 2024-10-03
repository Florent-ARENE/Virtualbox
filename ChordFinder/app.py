from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

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
    soup = BeautifulSoup(response.content, "html.parser")

    # Chercher toutes les images potentielles sur cette page
    image_elements = soup.find_all('img', src=True)
    images = []

    for img in image_elements:
        if "chordshape" in img['src']:
            full_img_url = f"https://jguitar.com{img['src']}"
            # Filtrer uniquement les images dont la fin correspond aux positions des doigts
            if img['src'].endswith(encoded_positions + ".png"):
                images.append(full_img_url)

    return images

# Fonction principale pour obtenir toutes les images correspondant aux positions des doigts
def get_chord_images_for_finger_positions(string_positions):
    # Scraper toutes les paires "Nom + Type"
    chords = scrape_chord_name_and_type(string_positions)

    # Encodage des positions pour la fin de l'URL
    encoded_positions = urllib.parse.quote(",".join(string_positions))

    # Chercher les images pour chaque accord trouvé sur un nombre limité de pages
    all_images = []

    # Boucle à travers chaque accord pour les pages (jusqu'à ce qu'on ne trouve plus d'images pertinentes)
    for chord_root, chord_type in chords:
        max_pages = 3  # Limite des pages à parcourir
        for page in range(1, max_pages + 1):
            images = search_images_for_chord_on_page(chord_root, encoded_positions, page)
            for image in images:
                all_images.append({'chord_name': chord_root, 'chord_type': chord_type, 'image_url': image})

    # Retourner toutes les images filtrées
    return all_images

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Récupérer les positions des doigts depuis le formulaire
            string_positions = [
                request.form['string0'],  # Corde mi grave
                request.form['string1'],  # Corde la
                request.form['string2'],  # Corde ré
                request.form['string3'],  # Corde sol
                request.form['string4'],  # Corde si
                request.form['string5']   # Corde mi aigu
            ]
        except KeyError as e:
            return f"Erreur dans le formulaire, champ manquant : {e}"

        # Obtenir toutes les images correspondant aux positions des doigts
        images = get_chord_images_for_finger_positions(string_positions)

        # Afficher les informations et les images
        return render_template('index.html', images=images)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
