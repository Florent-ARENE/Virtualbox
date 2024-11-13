# QR Contact Logger

## Introduction

QR Contact Logger est un projet permettant de générer des QR codes pour des contacts et de consigner automatiquement les informations scannées via une interface web. Ce projet est particulièrement utile pour des événements où il est nécessaire d’enregistrer rapidement les informations des participants. Le projet inclut un script Python pour créer des QR codes à partir de noms et prénoms, et une application web en PHP pour enregistrer et visualiser les contacts scannés.

## Fonctionnalités

1. **Génération de QR Codes** : À partir d'un fichier CSV contenant des noms et prénoms, le script Python génère des QR codes avec les informations de contact encodées en base64.
2. **Enregistrement Automatique des Scans** : Lorsqu'un QR code est scanné, l'application web enregistre automatiquement les informations dans un fichier CSV pour les consultations ultérieures.
3. **Téléchargement du Journal des Scans** : L'interface web permet de télécharger le journal des scans au format CSV.
4. **Compatibilité avec Excel** : Le fichier CSV est encodé pour être compatible avec les éditeurs de texte classiques ainsi qu'avec Microsoft Excel, sans problème d'affichage des caractères spéciaux.

## Structure du Projet

```
QR Contact Logger
├── fichier.csv               # Fichier source CSV avec les noms
├── generate_qrcode.py        # Script Python pour générer les QR codes
├── qrcodes                   # Dossier pour stocker les images de QR codes générées
└── www                       # Fichiers web pour le déploiement
    ├── export_scans.php      # Exporte les données scannées en CSV
    ├── index.php             # Page principale pour afficher les scans et enregistrer les entrées
    └── style.css             # Style de l'interface web
```

## Installation et Utilisation

### Étape 1 : Préparer le Fichier Source CSV

Créez ou éditez `fichier.csv` pour inclure les noms de contact au format suivant (séparateur `;`) :

```csv
nom;prenom
Dupont;Jean
Martin;Alice
```

### Étape 2 : Générer les QR Codes

Exécutez le script `generate_qrcode.py` pour générer des QR codes pour chaque contact présent dans `fichier.csv`.

1. **Installer les bibliothèques nécessaires** :
   ```bash
   pip install qrcode[pil]
   ```

2. **Exécuter le script** :
   ```bash
   python generate_qrcode.py
   ```
   
   Les QR codes seront sauvegardés sous forme d'images dans le dossier `qrcodes`.

### Étape 3 : Déployer l'Application Web

Placez le contenu du dossier `www` sur votre serveur web. Le fichier `index.php` affichera la liste des noms scannés et permettra le téléchargement du fichier CSV.

## Utilisation de l'Application

1. **Scanner le QR Code** : Chaque QR code redirige vers l'application web avec les informations de contact encodées en paramètre d'URL.
2. **Enregistrement Automatique** : Les informations du contact sont automatiquement ajoutées à `scans.csv` si elles ne sont pas déjà présentes.
3. **Télécharger le CSV** : Le bouton "Télécharger le fichier CSV" sur la page principale permet d'exporter le journal des scans.

## Détails Techniques

### Fichier `generate_qrcode.py`

Ce script Python lit le fichier `fichier.csv`, encode chaque nom et prénom en JSON puis en base64 pour créer un lien URL compatible avec les QR codes. Les images des QR codes sont générées et enregistrées dans le dossier `qrcodes`.

### Fichier `index.php`

Ce fichier PHP traite les données des QR codes scannés, enregistre les nouvelles entrées dans `scans.csv` et affiche les scans précédents sur une interface simple. Le fichier utilise l’encodage UTF-8 pour garantir la compatibilité des caractères spéciaux.

### Fichier `export_scans.php`

Ce fichier exporte le contenu de `scans.csv` pour permettre le téléchargement du fichier depuis l'interface web.

## Prérequis

- **Python** pour la génération des QR codes
- **PHP** et un serveur web pour héberger l'application web

## Compatibilité

Le projet est conçu pour être compatible avec les éditeurs de texte classiques et Excel, afin de garantir :
- Un affichage correct des caractères spéciaux.
- Une lecture facile dans Excel sans problème de codage.

## Licence

Ce projet est open source et disponible sous la [Licence MIT](LICENSE).
```

Ce fichier `README.md` est conçu pour être clair et fournir les informations nécessaires pour l'installation, l'utilisation, et la compréhension des fichiers et fonctionnalités du projet QR Contact Logger.