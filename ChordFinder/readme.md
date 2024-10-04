# ChordFinder

## Description

ChordFinder est une application web simple qui permet de rechercher des accords de guitare en fonction des positions des doigts sur les 6 cordes. L'application récupère des images des diagrammes d'accords correspondant depuis le site jguitar.com et les affiche en fonction de la saisie de l'utilisateur.

## Fonctionnalités

- Entrez la position des doigts pour chaque corde (mi grave, la, ré, sol, si, mi aigu).
- L'application affiche les accords correspondant à ces positions de doigts, avec leurs images associées et leurs noms.
- Utilise une logique intelligente pour naviguer entre les pages de résultats sur jguitar.com afin de trouver tous les diagrammes pertinents.
- Design moderne et épuré pour une meilleure expérience utilisateur.

Tu as raison, cela ne fonctionnera pas avec un chemin qui inclut un sous-dossier comme `.../tree/main/ChordFinder`. La commande `git clone` fonctionne uniquement sur des repositories Git complets.

Si tu veux que les utilisateurs clonent directement ton projet `ChordFinder`, ils doivent cloner tout le repository principal, comme ceci :

```bash
git clone https://github.com/Florent-ARENE/Virtualbox.git
```

Ensuite, ils peuvent accéder au dossier `ChordFinder` :

```bash
cd Virtualbox/ChordFinder
```

## Installation

1. Clonez ce dépôt sur votre machine :
   ```bash
   git clone https://github.com/Florent-ARENE/Virtualbox.git
   ```

2. Accédez au dossier du projet :
   ```bash
   cd Virtualbox/ChordFinder
   ```

3. Installez les dépendances Python nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancez l'application Flask :
   ```bash
   python app.py
   ```

## Utilisation

1. Sur la page d'accueil, entrez les positions des doigts pour chaque corde :
   - `x` pour une corde non jouée.
   - `0` pour une corde à vide.
   - Un nombre pour la frette jouée sur la corde.

2. Cliquez sur le bouton **Trouver l'accord**.

3. Les résultats affichent le nom de l'accord trouvé et l'image correspondante montrant le diagramme de doigté.

## Exemples de positions d'accords

Voici quelques exemples d'accords populaires et leurs positions de doigts :

- **C-Major** : `x,3,2,0,1,0`
- **G-Major** : `3,2,0,0,3,3`
- **E-Minor** : `0,2,2,0,0,0`

Ces exemples peuvent être entrés dans l'application pour retrouver les accords correspondants.

## Technologies utilisées

- **Python** pour le backend.
- **Flask** pour le framework web.
- **BeautifulSoup** et **requests** pour le scraping des données depuis jguitar.com.
- **HTML/CSS** pour l'interface utilisateur.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet, n'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.