# ChordFinder 🎸 v2.1

## Description

**ChordFinder** est une application web intuitive qui permet d'identifier des accords de guitare en utilisant une interface moderne d'expansion intelligente. L'application récupère des diagrammes d'accords depuis jguitar.com et propose une expérience utilisateur optimisée avec navigation séquentielle corde par corde.

## Fonctionnalités

- ✨ **Interface d'expansion intelligente** : Frettes courantes (X, 0-12) par défaut + expansion vers 13-26
- 🎯 **Navigation séquentielle optimisée** : Passage automatique entre cordes avec modification directe
- 🎲 **Exemples aléatoires intégrés** : 5 accords populaires (Do, Sol, Em, La, Ré majeurs/mineurs)
- 🔗 **Partage d'accords avancé** : URL partageable avec restauration automatique
- 💾 **Persistance session** : État d'expansion et accords mémorisés automatiquement
- 📱 **Mobile-first responsive** : Interface tactile optimisée avec swipe et tap
- 🎨 **Design glassmorphism** : Interface moderne avec animations fluides
- ⚡ **Performance optimisée** : Scraping intelligent avec cache et retry logic
- ⌨️ **Raccourcis clavier étendus** : ←→ navigation, Espace expand, Échap clear

## Installation

### Démarrage rapide (Développement)

1. **Clonage du projet**
   ```bash
   git clone https://github.com/Florent-ARENE/Virtualbox.git
   cd Virtualbox/ChordFinder
   ```

2. **Environnement virtuel**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Installation des dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancement développement**
   ```bash
   python app.py
   ```
   Accessible sur `http://localhost:5000/`

### Déploiement Production (Apache + WSGI)

Consultez le guide détaillé [install.md](install.md) pour la configuration complète Apache/SSL.

## Comment utiliser ChordFinder

### 📝 Comment utiliser :

* **Sélectionnez une position** pour la corde courante (passage automatique à la suivante)
* **Cliquez sur une case** dans "Accord actuel" pour modifier cette corde directement
* **Touches clavier** : ← et → pour naviguer rapidement

### ⚡ Fonctionnalités avancées :

* **Interface d'expansion** : Bouton "+" pour révéler frettes 13-26 (mémorisé en session)
* **Raccourcis étendus** : Espace pour expand, Échap pour effacer tout
* **Accord aléatoire** : Bouton 🎲 pour charger des exemples populaires  
* **Persistance intelligente** : Vos sélections survivent à la navigation
* **Partage instantané** : URL générée automatiquement pour partager vos accords

### Exemples d'Accords Populaires

#### **🎲 Fonction "Accord aléatoire"**
Cliquez sur le bouton **🎲 Accord aléatoire** dans l'interface pour charger automatiquement un des 5 accords suivants :

#### **Accords intégrés** (testez ces liens !)
- [**C Major (Do)**](https://fiflo.fr/ChordFinder/?chord=x,3,2,0,1,0) : `x,3,2,0,1,0`
- [**G Major (Sol)**](https://fiflo.fr/ChordFinder/?chord=3,2,0,0,3,3) : `3,2,0,0,3,3`
- [**Em Minor (Mi m)**](https://fiflo.fr/ChordFinder/?chord=0,2,2,0,0,0) : `0,2,2,0,0,0`
- [**A Major (La)**](https://fiflo.fr/ChordFinder/?chord=x,0,2,2,2,0) : `x,0,2,2,2,0`
- [**D Major (Ré)**](https://fiflo.fr/ChordFinder/?chord=x,x,0,2,3,2) : `x,x,0,2,3,2`

#### **Accords intermédiaires**
- [**F Major (Barré)**](https://fiflo.fr/ChordFinder/?chord=1,3,3,2,1,1) : `1,3,3,2,1,1`
- [**B7**](https://fiflo.fr/ChordFinder/?chord=x,2,1,2,0,2) : `x,2,1,2,0,2`
- [**Dm7**](https://fiflo.fr/ChordFinder/?chord=x,x,0,2,1,1) : `x,x,0,2,1,1`

#### **Accords avancés (frettes hautes)**
- [**E Major (12ème case)**](https://fiflo.fr/ChordFinder/?chord=12,14,14,13,12,12) : `12,14,14,13,12,12`

### Tutoriel Pas-à-Pas

#### **Première utilisation :**

1. **Démarrage** : Interface sur corde 6 (Mi grave)
2. **Exemple C Major** :
   - Corde 6 → Cliquez **X** (rouge) → ✅ Passage auto corde 5
   - Corde 5 → Cliquez **3** (vert) → ✅ Passage auto corde 4
   - Corde 4 → Cliquez **2** (vert) → ✅ Passage auto corde 3
   - Corde 3 → Cliquez **0** (orange) → ✅ Passage auto corde 2
   - Corde 2 → Cliquez **1** (vert) → ✅ Passage auto corde 1
   - Corde 1 → Cliquez **0** (orange) → ✅ Bouton "Trouver l'accord" actif

3. **Validation** : "🎵 Accord actuel" affiche `X-3-2-0-1-0`
4. **Recherche** : Clic "🔍 Trouver l'accord" → Résultats avec diagrammes

#### **Modification d'un accord existant :**

1. **Clic direct** sur une case "Accord actuel" (ex: corde 4 contenant "2")
2. **Interface bascule** sur cette corde avec sélection actuelle mise en évidence
3. **Nouvelle sélection** → Mise à jour immédiate de l'accord
4. **Navigation libre** avec flèches ou clic suivant

### Interface d'expansion des frettes

#### **Vue compacte (par défaut)**
```
| X | 0 | 1 | 2 | 3 | 4 | 5 |
| 6 | 7 | 8 | 9 | 10| 11| 12|
|     [+ Afficher frettes hautes]     |  ← Bouton d'expansion
```

#### **Vue étendue (après clic +)**
```
| X | 0 | 1 | 2 | 3 | 4 | 5 |
| 6 | 7 | 8 | 9 | 10| 11| 12|
| 13| 14| 15| 16| 17| 18| 19|
| 20| 21| 22| 23| 24| 25| 26|
|     [- Masquer frettes hautes]      |  ← Bouton de repli
```

**Persistance intelligente :**
- Votre préférence d'affichage est **mémorisée durant toute la session**
- **Navigation clavier** : Barre `Espace` pour toggle expansion
- **Animation fluide** : Transitions CSS pour expand/collapse

## Technologies utilisées

### Stack Frontend
- **HTML5/CSS3** : Interface glassmorphism avec système d'expansion intelligent
- **CSS modulaire** : style.css (design) + behavioral.css (interactions)
- **JavaScript ES6+** : Logic séquentielle, persistance sessionStorage, navigation tactile
- **Design System** : Variables CSS, animations fluides, responsive grid adaptatif

### Stack Backend
- **Python 3.8+** / **Flask 3.0.3** : Framework web léger et performant
- **BeautifulSoup4** : Scraping HTML intelligent avec retry logic
- **Requests** : Client HTTP robuste avec gestion d'erreurs

### Infrastructure Production
- **Apache 2.4+** / **mod_wsgi** : Serveur web avec configuration SSL
- **Let's Encrypt** : Certificats SSL automatisés
- **Ubuntu Server** : Système avec monitoring et logs centralisés

### Architecture Avancée
- **Scraping intelligent** : Navigation multi-pages avec détection de pagination
- **Cache stratégique** : Optimisation des requêtes répétées
- **Monitoring** : Logs détaillés pour diagnostic et performance
- **Sécurité** : Headers HSTS, CSP, validation rigoureuse des entrées

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées pour améliorer ce projet :

**Issues ouvertes :**
- 🔍 Recherche par nom d'accord (reverse lookup)
- 🎵 Base de données d'accords locale (cache permanent)
- 📱 App mobile native (React Native / Flutter)
- 🔧 API REST pour intégration externe
- 🎨 Thèmes personnalisables (mode sombre/clair)

**Comment contribuer :**
1. Fork du repository
2. Branche dédiée : `git checkout -b feature/nom-fonctionnalite`
3. Commits descriptifs en français
4. Pull request avec description détaillée

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus d'informations.

---

## Support

### 🆘 Problèmes fréquents

**L'interface ne répond pas :**
- Vérifiez que JavaScript est activé
- Testez sur un autre navigateur (Chrome/Firefox recommandés)
- Consultez la console développeur (F12)

**Accords introuvables :**
- Vérifiez que toutes les cordes sont renseignées
- Testez avec un accord connu (ex: Em = 0,2,2,0,0,0)
- Les accords très rares peuvent ne pas être dans jguitar.com

**Lien de partage incorrect :**
- L'URL doit contenir `?chord=x,x,x,x,x,x` avec 6 valeurs
- Evitez les caractères spéciaux dans l'URL

### 📞 Contact et feedback

- **Issues GitHub** : Rapports de bugs et suggestions
- **Email** : support@fiflo.fr (pour questions techniques)
- **Demo live** : https://fiflo.fr/ChordFinder/

---

*ChordFinder v2.1 - Interface d'expansion intelligente - Créé avec ❤️ pour la communauté des guitaristes*