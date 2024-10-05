# README : Recherche et Affichage d'Accords de Guitare à Partir de Positions de Doigts

## Introduction

Ce projet Flask permet aux utilisateurs de saisir les positions des doigts sur une guitare pour identifier et afficher les accords correspondants. Le script récupère les informations depuis le site jguitar.com, génère les images des accords correspondants et les affiche. Le projet inclut également une fonctionnalité de "chenillard" (spinner) pendant la recherche des résultats, offrant ainsi une meilleure expérience utilisateur.

## Prérequis

- **Python** 3.x
- **Flask** pour le serveur web
- **Requests** pour faire des requêtes HTTP
- **BeautifulSoup** pour le scraping web
- Un accès à internet pour récupérer les informations depuis le site jguitar.com

## 1. Outils Utilisés

### 1.1 Flask

**Flask** est un micro-framework en Python utilisé pour gérer les requêtes et servir les pages web. Il gère le formulaire utilisateur et affiche les résultats des recherches d'accords en fonction des positions des doigts sur la guitare.

### 1.2 Requests et BeautifulSoup

**Requests** permet de faire des requêtes HTTP pour obtenir le contenu des pages web, tandis que **BeautifulSoup** est utilisé pour scraper les informations pertinentes des pages jguitar.com. Ces outils récupèrent les noms des accords et les images correspondant aux positions des doigts saisies.

### 1.3 CSS et JavaScript

**CSS** est utilisé pour le style du formulaire et des résultats, tandis que **JavaScript** gère la modale (avec chenillard) qui apparaît pendant que les informations sont recherchées.

## 2. Fonctionnement du Projet

### 2.1 Formulaire de Positions des Doigts

L'utilisateur entre les positions des doigts pour chaque corde de la guitare (Corde 6 à 1) via un formulaire web. Chaque position correspond à une frette (un nombre entier) ou une corde non jouée ('x').

### 2.2 Scraping des Accords

Lorsque le formulaire est soumis, le script Flask envoie une requête au site jguitar.com pour récupérer les accords correspondant aux positions de doigts spécifiées. Le scraping est réalisé via **BeautifulSoup** pour extraire les accords et leurs images.

### 2.3 Affichage des Résultats

Le projet distingue les résultats en deux catégories :
- **Accords exacts** : les accords qui correspondent exactement aux positions de doigts fournies.
- **Autres positions** : des accords similaires mais avec des positions de doigts différentes.

Les résultats sont affichés directement dans le navigateur avec leurs images associées.

## 3. Structure des Fichiers

### 3.1 `app.py`

Ce fichier est le cœur du projet. Il contient le code Flask pour gérer les requêtes, traiter le formulaire utilisateur et scraper les informations depuis jguitar.com. Il inclut également la gestion de l'affichage des résultats et du chenillard pendant la recherche.

### 3.2 `templates/index.html`

Le fichier HTML qui affiche le formulaire pour les positions des doigts et les résultats après la recherche. Il inclut également un script JavaScript pour afficher la modale de chargement pendant la recherche.

### 3.3 `static/css/style.css`

Ce fichier contient les styles CSS pour le formulaire, les résultats, et la modale. Le style assure que le site est à la fois esthétique et facile à utiliser.

## 4. Explication du Code

### 4.1 Flask et Formulaire

Lorsque l'utilisateur soumet le formulaire, Flask reçoit les données et les traite via la fonction `get_chord_images_for_finger_positions()`. Les positions des doigts sont passées sous forme de paramètres à la fonction qui se charge de scraper jguitar.com.

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        string_positions = [
            request.form['string0'], request.form['string1'], 
            request.form['string2'], request.form['string3'], 
            request.form['string4'], request.form['string5']
        ]
        exact_matches, other_positions = get_chord_images_for_finger_positions(string_positions)
        return render_template('index.html', exact_matches=exact_matches, other_positions=other_positions)
    return render_template('index.html')
```

### 4.2 Scraping avec BeautifulSoup

La fonction `get_chord_images_for_finger_positions()` fait une requête à jguitar.com, puis utilise **BeautifulSoup** pour extraire les résultats pertinents (nom de l'accord et image). 

### 4.3 Modale avec Chenillard

Le JavaScript et le CSS sont utilisés pour afficher une modale avec un spinner pendant que les informations sont scrappées, améliorant l'expérience utilisateur.

```html
<div class="modal" id="loaderModal">
    <div class="modal-content">
        <h2>Recherche en cours...</h2>
        <div class="loader"></div>
    </div>
</div>
```

```css
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
}
```

## 5. Lancer le Projet

### 5.1 Installer les dépendances

Assurez-vous que **Flask**, **Requests** et **BeautifulSoup** sont installés sur votre machine.

```bash
pip install flask requests beautifulsoup4
```

### 5.2 Lancer le serveur

```bash
python app.py
```

Le serveur sera accessible à l'adresse [http://127.0.0.1:5000](http://127.0.0.1:5000). Vous pourrez saisir les positions des doigts et voir les résultats en temps réel.

## 6. Conclusion

Ce projet offre une solution simple et intuitive pour rechercher des accords de guitare en fonction des positions des doigts, avec un affichage clair des résultats exacts et similaires. Il pourrait être étendu pour inclure d'autres fonctionnalités comme la recherche par nom d'accord, l'ajout de filtres, ou encore la gestion d'autres instruments.
