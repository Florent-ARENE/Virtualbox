# ChordFinder - Guide de Déploiement Production

Ce document décrit la configuration et la mise en production du projet **ChordFinder**, une application Flask utilisant Apache, mod_wsgi, et HTTPS via Let's Encrypt. Ce guide couvre l'intégration de ChordFinder dans un VirtualHost existant ainsi que les solutions aux problèmes de déploiement courants.

## Table des matières
1. [Prérequis et préparation](#prérequis-et-préparation)
2. [Configuration de l'environnement virtuel](#configuration-de-lenvironnement-virtuel)
3. [Installation des dépendances](#installation-des-dépendances)
4. [Configuration du fichier app.wsgi](#configuration-du-fichier-appwsgi)
5. [Configuration du fichier app.py](#configuration-du-fichier-apppy)
6. [Intégration Apache VirtualHost](#intégration-apache-virtualhost)
7. [Gestion des conflits multi-domaines](#gestion-des-conflits-multi-domaines)
8. [Configuration SSL et Let's Encrypt](#configuration-ssl-et-lets-encrypt)
9. [Dépannage des problèmes courants](#dépannage-des-problèmes-courants)
10. [Tests de validation](#tests-de-validation)

---

## Prérequis et préparation

### Système requis
- Ubuntu/Debian avec Apache 2.4+
- Python 3.8+ 
- mod_wsgi installé et activé
- Accès root/sudo

### Structure de fichiers
```
/var/www/html/ChordFinder/
├── app.py                 # Application Flask (route /)
├── app.wsgi              # Point d'entrée WSGI
├── venv/                 # Environnement virtuel Python
├── static/css/           # Fichiers CSS
├── templates/            # Templates HTML
├── requirements.txt      # Dépendances Python
└── readme.md            # Documentation
```

## Configuration de l'environnement virtuel

1. **Créer et activer l'environnement virtuel :**

```bash
cd /var/www/html/ChordFinder/
python3 -m venv venv
source venv/bin/activate
```

2. **Vérifier la version Python utilisée :**

```bash
python3 --version
ls venv/lib/  # Noter le dossier pythonX.Y pour la config WSGI
```

## Installation des dépendances

**Installer les packages requis :**

```bash
# Avec l'environnement virtuel activé
pip install -r requirements.txt

# Ou installation manuelle
pip install Flask==3.0.3 beautifulsoup4==4.12.3 requests==2.32.3
```

**Vérifier l'installation :**

```bash
python3 -c "from app import app; print('Import OK')"
```

## Configuration du fichier app.wsgi

**Créer `/var/www/html/ChordFinder/app.wsgi` :**

```python
#!/usr/bin/python3
import sys
import site

# Ajouter le chemin du projet
sys.path.insert(0, '/var/www/html/ChordFinder')

# CRITIQUE: Ajouter explicitement les packages de l'environnement virtuel
# Adapter python3.12 selon votre version Python
site.addsitedir('/var/www/html/ChordFinder/venv/lib/python3.12/site-packages')

from app import app as application

if __name__ == "__main__":
    application.run()
```

**⚠️ Points critiques :**
- Utiliser `site.addsitedir()` pour l'environnement virtuel
- Adapter le chemin selon votre version Python (python3.X)
- Le fichier doit s'appeler `app.wsgi` (pas `chordfinder.wsgi`)

## Configuration du fichier app.py

### Différences Dev vs Production

**🏠 Mode Développement (test local) :**
```python
@app.route('/ChordFinder/', methods=['GET', 'POST'])  # Route complète
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Port 5000
```

**🚀 Mode Production (WSGI/Apache) :**
```python
@app.route('/', methods=['GET', 'POST'])  # Route racine
if __name__ == '__main__':
    app.run()  # Géré par mod_wsgi
```

### Configuration templates/index.html

**Chemins des fichiers statiques en production :**

```html
<!-- ✅ Correct pour production WSGI -->
<link rel="stylesheet" href="/ChordFinder/static/css/style.css">

<!-- ❌ Incorrect - ne fonctionne qu'en dev -->
<link rel="stylesheet" href="/static/css/style.css">
```

## Intégration Apache VirtualHost

**Au lieu de créer une configuration séparée, intégrer ChordFinder dans un VirtualHost existant.**

### Configuration SSL recommandée

**Exemple d'intégration dans `/etc/apache2/sites-available/mondomaine.fr-le-ssl.conf` :**

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName mondomaine.fr
    ServerAlias www.mondomaine.fr

    # Site principal
    DocumentRoot /var/www/html/mondomaine.fr

    # Configuration WSGI pour ChordFinder
    WSGIScriptAlias /ChordFinder /var/www/html/ChordFinder/app.wsgi

    <Directory /var/www/html/ChordFinder>
        Require all granted
    </Directory>

    # Servir les fichiers statiques de ChordFinder
    Alias /ChordFinder/static /var/www/html/ChordFinder/static
    <Directory /var/www/html/ChordFinder/static>
        Require all granted
    </Directory>

    # Configuration SSL standard
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/mondomaine.fr/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/mondomaine.fr/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    ErrorLog ${APACHE_LOG_DIR}/mondomaine.fr_error.log
    CustomLog ${APACHE_LOG_DIR}/mondomaine.fr_access.log combined
</VirtualHost>
</IfModule>
```

### Permissions système

```bash
# Ajuster les permissions
sudo chown -R www-data:www-data /var/www/html/ChordFinder/
sudo chmod -R 755 /var/www/html/ChordFinder/
sudo chmod +x /var/www/html/ChordFinder/app.wsgi
```

## Gestion des conflits multi-domaines

### Problème des serveurs par défaut

**Si vous gérez plusieurs domaines, éviter les conflits SSL :**

```bash
# Vérifier l'ordre des VirtualHost
sudo apache2ctl -S

# Si nécessaire, faire du domaine principal le serveur par défaut
sudo mv /etc/apache2/sites-available/mondomaine.fr.conf /etc/apache2/sites-available/000-mondomaine.fr.conf
sudo mv /etc/apache2/sites-available/mondomaine.fr-le-ssl.conf /etc/apache2/sites-available/000-mondomaine.fr-le-ssl.conf

# Réactiver avec les nouveaux noms
sudo a2dissite mondomaine.fr.conf mondomaine.fr-le-ssl.conf
sudo a2ensite 000-mondomaine.fr.conf 000-mondomaine.fr-le-ssl.conf
```

### Logs d'erreurs typiques

**Conflit SSL multi-domaines :**
```
AH02032: Hostname autredomaine.fr (default host as no SNI was provided) 
and hostname mondomaine.fr provided via HTTP have no compatible SSL setup
```

**Solution :** Définir le bon domaine comme serveur par défaut.

## Configuration SSL et Let's Encrypt

### Installation certificat

```bash
# Générer le certificat SSL
sudo certbot --apache -d mondomaine.fr -d www.mondomaine.fr
```

### Test de renouvellement

```bash
# Vérifier que le renouvellement fonctionne après intégration
sudo certbot renew --dry-run
```

**Le renouvellement automatique continue de fonctionner même après renommage des fichiers de configuration Apache.**

## Dépannage des problèmes courants

### Erreur "ModuleNotFoundError: No module named 'flask'"

**Cause :** WSGI n'utilise pas l'environnement virtuel

**Solution :** Vérifier `app.wsgi` avec `site.addsitedir()` :

```python
# ✅ Configuration correcte
site.addsitedir('/var/www/html/ChordFinder/venv/lib/python3.12/site-packages')
```

### Erreur 404 Flask "The requested URL was not found"

**Cause :** Route Flask incorrecte pour WSGI

**Solution :** Route `/` dans `app.py` :

```python
# ✅ Correct pour WSGI
@app.route('/', methods=['GET', 'POST'])

# ❌ Incorrect pour WSGI  
@app.route('/ChordFinder/', methods=['GET', 'POST'])
```

### CSS non chargé

**Cause :** Chemins statiques incorrects

**Solution :** Utiliser le préfixe `/ChordFinder/` dans `index.html` :

```html
<!-- ✅ Correct -->
<link rel="stylesheet" href="/ChordFinder/static/css/style.css">
```

### Erreur 500 "Internal Server Error"

**Diagnostic :**

```bash
# Surveiller les logs en temps réel
sudo tail -f /var/log/apache2/mondomaine.fr_error.log

# Tester l'import Python manuellement
cd /var/www/html/ChordFinder/
source venv/bin/activate
python3 -c "from app import app; print('OK')"
```

### Problèmes de permissions

```bash
# Vérifier et corriger les permissions
sudo chown -R www-data:www-data /var/www/html/ChordFinder/
sudo chmod -R 755 /var/www/html/ChordFinder/
```

## Tests de validation

### Tests étape par étape

1. **Test environnement Python :**
```bash
cd /var/www/html/ChordFinder/
source venv/bin/activate
python3 -c "from app import app; print('Import OK')"
```

2. **Test configuration Apache :**
```bash
sudo apache2ctl configtest
sudo systemctl restart apache2
```

3. **Test fonctionnel :**
```bash
curl -I https://mondomaine.fr/ChordFinder/
# Attendu: HTTP/1.1 200 OK
```

4. **Test interface :**
   - Navigateur : `https://mondomaine.fr/ChordFinder/`
   - Vérifier que le CSS se charge
   - Tester la recherche d'accords

### Validation complète

**Checklist finale :**

- [ ] Environnement virtuel fonctionnel
- [ ] `app.wsgi` avec `site.addsitedir()` correct
- [ ] Route Flask `/` (pas `/ChordFinder/`)
- [ ] Chemins CSS avec préfixe `/ChordFinder/static/`
- [ ] Permissions www-data correctes
- [ ] Configuration Apache intégrée
- [ ] Tests SSL et renouvellement OK
- [ ] Application accessible et fonctionnelle

## Support et maintenance

### Logs utiles

```bash
# Logs applicatifs
sudo tail -f /var/log/apache2/mondomaine.fr_error.log

# Logs système Apache
sudo tail -f /var/log/apache2/error.log
```

### Mise à jour de l'application

```bash
cd /var/www/html/ChordFinder/
source venv/bin/activate
git pull  # Si sous Git
pip install -r requirements.txt  # Mise à jour dépendances
sudo systemctl reload apache2  # Redémarrage Apache
```

Cette approche d'intégration dans un VirtualHost existant est plus robuste que les configurations séparées et évite les conflits multi-domaines.
