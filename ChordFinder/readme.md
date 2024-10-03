# Guitar Chord Finder

## Description
Guitar Chord Finder est une application web simple qui permet de rechercher des accords de guitare en fonction des positions des doigts sur les 6 cordes. L'application récupère des images des diagrammes d'accords correspondant depuis le site jguitar.com et les affiche en fonction de la saisie de l'utilisateur.

## Fonctionnalités
- Entrez la position des doigts pour chaque corde (mi grave, la, ré, sol, si, mi aigu).
- L'application affiche les accords correspondant à ces positions de doigts, avec leurs images associées et leurs noms.
- Utilise une logique intelligente pour naviguer entre les pages de résultats sur jguitar.com afin de trouver tous les diagrammes pertinents.
- Design moderne et épuré pour une meilleure expérience utilisateur.

## Installation

1. Clonez ce dépôt sur votre machine :
   ```bash
   git clone https://github.com/ton-utilisateur/guitar-chord-finder.git
   ```
2. Accédez au dossier du projet :
   ```bash
   cd guitar-chord-finder
   ```
3. Installez les dépendances Python nécessaires :
   ```bash
   pip install -r requirements.txt
   ```
4. Lancez l'application Flask :
   ```bash
   python app.py
   ```

5. Ouvrez un navigateur et accédez à `http://127.0.0.1:5000` pour utiliser l'application.

## Utilisation

1. Sur la page d'accueil, entrez les positions des doigts pour chaque corde.
   - `x` pour une corde non jouée.
   - `0` pour une corde à vide.
   - Un nombre pour la frette jouée sur la corde.

2. Cliquez sur le bouton **Trouver l'accord**.

3. Les résultats affichent le nom de l'accord trouvé et l'image correspondante montrant le diagramme de doigté.

## Exemple

Pour une position donnée telle que :  
```
Corde 6 (Mi grave) : x  
Corde 5 (La) : 0  
Corde 4 (Ré) : 2  
Corde 3 (Sol) : 2  
Corde 2 (Si) : 2  
Corde 1 (Mi aigu) : 0  
```

L'application affichera les accords correspondants avec leurs images.

## Technologies utilisées

- **Python** pour le backend.
- **Flask** pour le framework web.
- **BeautifulSoup** et **requests** pour le scraping des données depuis jguitar.com.
- **HTML/CSS** pour l'interface utilisateur.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.