# ChordFinder

## Description

ChordFinder est une application web simple qui permet de rechercher des accords de guitare en fonction des positions des doigts sur les 6 cordes. L'application récupère des images des diagrammes d'accords correspondant depuis le site jguitar.com et les affiche en fonction de la saisie de l'utilisateur.

## Fonctionnalités

- Entrez la position des doigts pour chaque corde (mi grave, la, ré, sol, si, mi aigu).
- L'application affiche les accords correspondant à ces positions de doigts, avec leurs images associées et leurs noms.
- Utilise une logique intelligente pour naviguer entre les pages de résultats sur jguitar.com afin de trouver tous les diagrammes pertinents.
- Design moderne et épuré pour une meilleure expérience utilisateur.
- Interface responsive avec validation en temps réel des saisies.
- Modale de chargement pendant la recherche d'accords.

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation locale

1. Clonez ce dépôt sur votre machine :
   ```bash
   git clone https://github.com/Florent-ARENE/Virtualbox.git
   ```

2. Accédez au dossier du projet :
   ```bash
   cd Virtualbox/ChordFinder
   ```

3. Créez un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

4. Installez les dépendances Python nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Mode Développement

Pour tester l'application localement :

```bash
# Assurez-vous que l'environnement virtuel est activé
source venv/bin/activate

# Lancez l'application Flask
python app.py
```

L'application sera accessible à l'adresse : `http://localhost:5000/`

### Mode Production (WSGI)

Pour un déploiement en production avec Apache et mod_wsgi :

1. **Fichier WSGI requis** : `app.wsgi` doit être présent à la racine du projet
2. **Route racine** : En production, l'application utilise la route `/` (pas `/ChordFinder/`)
3. **Fichiers statiques** : Les ressources CSS/JS utilisent le préfixe `/ChordFinder/static/`

**⚠️ Points de vigilance pour le déploiement :**

- L'environnement virtuel doit être correctement configuré dans le fichier WSGI
- Les permissions des fichiers doivent être appropriées pour l'utilisateur web (www-data)
- Les chemins absolus dans `app.wsgi` doivent correspondre à votre installation

## Interface utilisateur

1. Sur la page d'accueil, entrez les positions des doigts pour chaque corde :
   - `x` pour une corde non jouée
   - `0` pour une corde à vide
   - Un nombre entre 1 et 26 pour la frette jouée sur la corde

2. Cliquez sur le bouton **Trouver l'accord**

3. Les résultats s'affichent en deux catégories :
   - **Positions exactes** : Accords correspondant exactement à votre saisie
   - **Positions similaires** : Accords proches si aucune correspondance exacte

## Exemples de positions d'accords

Voici quelques exemples d'accords populaires et leurs positions de doigts :

- **C-Major** : `x,3,2,0,1,0`
- **G-Major** : `3,2,0,0,3,3`
- **E-Minor** : `0,2,2,0,0,0`
- **A-Minor** : `x,0,2,2,1,0`
- **D-Major** : `x,x,0,2,3,2`

Ces exemples peuvent être entrés dans l'application pour retrouver les accords correspondants.

## Architecture technique

### Fichiers principaux

- `app.py` : Application Flask principale avec logique de scraping
- `app.wsgi` : Point d'entrée WSGI pour déploiement en production
- `templates/index.html` : Interface utilisateur avec validation JavaScript
- `static/css/style.css` : Styles CSS responsives
- `requirements.txt` : Dépendances Python

### Technologies utilisées

- **Python 3.x** pour le backend
- **Flask** pour le framework web
- **BeautifulSoup4** et **requests** pour le scraping des données depuis jguitar.com
- **HTML/CSS/JavaScript** pour l'interface utilisateur responsive
- **mod_wsgi** pour le déploiement en production

### Fonctionnement du scraping

1. **Identification** : Envoi des positions de doigts à jguitar.com/chordname
2. **Récupération** : Extraction des noms d'accords correspondants
3. **Recherche d'images** : Parcours des pages de résultats sur jguitar.com/chordsearch
4. **Filtrage** : Correspondance exacte vs. positions similaires
5. **Affichage** : Présentation des résultats avec images des diagrammes

## Dépannage

### Problèmes courants

**"ModuleNotFoundError: No module named 'flask'"**
- Vérifiez que l'environnement virtuel est activé
- Réinstallez les dépendances : `pip install -r requirements.txt`

**CSS non chargé en production**
- Vérifiez que le chemin CSS dans `index.html` utilise `/ChordFinder/static/`
- Vérifiez les permissions du dossier `static/`

**Aucun résultat trouvé**
- Vérifiez la connectivité vers jguitar.com
- Contrôlez les formats d'entrée (x, 0, ou nombres 1-26)

### Logs et débogage

En mode développement, les messages de debug s'affichent dans la console.
En production, consultez les logs du serveur web pour diagnostiquer les problèmes.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet :

1. Forkez le repository
2. Créez une branche pour votre fonctionnalité
3. Testez vos modifications
4. Soumettez une pull request

### Améliorations possibles

- Cache des résultats pour améliorer les performances
- Support d'autres instruments (ukulélé, mandoline)
- Sauvegarde des accords favoris
- API REST pour intégration dans d'autres applications

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.

## Support

Pour signaler un bug ou demander une fonctionnalité, ouvrez une issue sur le repository GitHub.