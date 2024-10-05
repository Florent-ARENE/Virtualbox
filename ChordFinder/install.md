# ChordFinder - Mise en production

Ce document décrit la configuration et la mise en production du projet **ChordFinder**, une application Flask utilisant Apache, mod_wsgi, et HTTPS via Let's Encrypt. Il inclut les instructions de configuration pour le fichier `app.wsgi`, le fichier `app.py` (pour les environnements de test et de production), ainsi que les configurations Apache pour HTTP et HTTPS.

## Table des matières
1. [Configuration de l'environnement virtuel](#configuration-de-lenvironnement-virtuel)
2. [Installation des dépendances](#installation-des-dépendances)
3. [Installation de mod_wsgi](#installation-de-mod_wsgi)
4. [Configuration du fichier `app.wsgi`](#configuration-du-fichier-appwsgi)
5. [Configuration du fichier `app.py`](#configuration-du-fichier-apppy)
   - [Environnement de test](#environnement-de-test)
   - [Environnement de production](#environnement-de-production)
6. [Configuration d'Apache](#configuration-dapache)
   - [HTTP](#http)
   - [HTTPS](#https)
7. [SSL avec Let's Encrypt](#ssl-avec-lets-encrypt)
8. [Renouvellement automatique du certificat SSL](#renouvellement-automatique-du-certificat-ssl)
9. [Démarrage et vérification](#démarrage-et-vérification)

---

## Configuration de l'environnement virtuel

Avant de commencer l'installation des dépendances, il est nécessaire de configurer l'environnement virtuel pour isoler les packages Python de votre projet.

1. Créez un environnement virtuel dans le répertoire du projet :

Exemple pour le répertoire `/var/www/html/ChordFinder/`

   ```bash
   cd /var/www/html/ChordFinder/
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Maintenant que l'environnement virtuel est activé, nous pouvons installer les dépendances spécifiques au projet.

## Installation des dépendances

Une fois l'environnement virtuel activé, installez les dépendances requises pour **ChordFinder**. Les dépendances incluent Flask, requests, BeautifulSoup4, et d'autres :

```bash
pip install -r requirements.txt
```

Si le fichier `requirements.txt` n'est pas disponible, installez manuellement les dépendances comme suit :

```bash
pip install flask requests beautifulsoup4
```

## Installation de mod_wsgi

Pour permettre à Apache de servir une application Flask via WSGI, installez **mod_wsgi** et activez-le :

```bash
sudo apt install libapache2-mod-wsgi-py3
sudo a2enmod wsgi
sudo systemctl reload apache2
```

Cela assure que **mod_wsgi** est bien installé et configuré pour **ChordFinder**.

## Configuration du fichier `app.wsgi`

Le fichier `app.wsgi` est utilisé pour connecter Apache à votre application Flask via mod_wsgi. Voici la configuration correcte :

```python
## app.wsgi
import sys
import os
import site

# Spécifie le chemin du projet et du virtualenv
sys.path.insert(0, '/var/www/html/ChordFinder')

# Ajoute le chemin des packages de l'environnement virtuel à sys.path
site.addsitedir('/var/www/html/ChordFinder/venv/lib/python3.12/site-packages')

# Importer l'application Flask
from app import app as application
```

Ce fichier doit être placé dans le répertoire `/var/www/html/ChordFinder/`.

## Configuration du fichier `app.py`

Voici deux versions du fichier `app.py`, une pour l'environnement de test et une pour l'environnement de production.

### Environnement de test

Le fichier `app.py` pour l'environnement de test permet d'exécuter l'application localement et de vérifier son fonctionnement sur le réseau local. En utilisant l'option `host='0.0.0.0'`, vous permettez à l'application Flask d'être accessible depuis n'importe quelle adresse IP de votre réseau local.

```python
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

app = Flask(__name__)

@app.route('/ChordFinder/', methods=['GET', 'POST'])
def index():
    # Implémentez ici la logique de votre application
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Vous pouvez exécuter cette version de l'application avec la commande suivante dans votre terminal :

```bash
python3 app.py --host=0.0.0.0
```

Cela rendra votre application accessible sur le réseau local à partir de l'adresse IP de votre machine, par exemple `http://192.168.1.x:5000/`. 

Cette méthode est utile pour tester votre application sur d'autres appareils connectés au même réseau local avant la mise en production.


### Environnement de production

Dans la version de production, Flask est exécuté par Apache et mod_wsgi, il n'est donc pas nécessaire d'utiliser `app.run()`. L'application est servie automatiquement via WSGI :

```python
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

app = Flask(__name__)

@app.route('/ChordFinder/', methods=['GET', 'POST'])
def index():
    # Implémentez ici la logique de votre application
    pass

if __name__ == '__main__':
    app.run()
```

### Remarque importante
Dans l'environnement de production, l'exécution de `app.run()` n'est pas nécessaire. C'est mod_wsgi qui prend automatiquement en charge l'exécution de l'application Flask en tant que service via Apache.

## Configuration d'Apache

### HTTP

Le fichier de configuration pour Apache en HTTP (`/etc/apache2/sites-available/ChordFinder.conf`) :

```apache
<VirtualHost *:80>
    ServerName my_domaine.com
    DocumentRoot /var/www/html/ChordFinder

    WSGIDaemonProcess chordfinder python-path=/var/www/html/ChordFinder/venv/lib/python3.12/site-packages
    WSGIScriptAlias /ChordFinder /var/www/html/ChordFinder/chordfinder.wsgi

    <Directory /var/www/html/ChordFinder>
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Ce fichier redirige tout le trafic HTTP vers HTTPS.

### HTTPS

Le fichier de configuration pour Apache en HTTPS (`/etc/apache2/sites-available/ChordFinder-le-ssl.conf`) avec le support SSL de Let's Encrypt :

```apache
<IfModule mod_ssl.c>
<VirtualHost *:443>
    ServerName my_domaine.com
    ServerAlias www.my_domaine.com
    DocumentRoot /var/www/html/ChordFinder

    WSGIDaemonProcess chordfinder_ssl python-path=/var/www/html/ChordFinder/venv/lib/python3.12/site-packages
    WSGIScriptAlias /ChordFinder /var/www/html/ChordFinder/chordfinder.wsgi

    <Directory /var/www/html/ChordFinder>
        Require all granted
    </Directory>

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/my_domaine.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/my_domaine.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
</IfModule>
```

## SSL avec Let's Encrypt

Pour configurer SSL avec Let's Encrypt, utilisez la commande suivante pour générer vos certificats :

```bash
sudo certbot --apache -d my_domaine.com -d www.my_domaine.com
```

Cela ajoutera les certificats nécessaires pour le HTTPS et configurera automatiquement Apache.

## Renouvellement automatique du certificat SSL

Les certificats Let's Encrypt expirent tous les 90 jours. Pour automatiser leur renouvellement, vous pouvez configurer une tâche cron avec Certbot. Ajoutez la ligne suivante pour vérifier quotidiennement et renouveler automatiquement les certificats si nécessaire :

```bash
0 0 * * * certbot renew --quiet
```

Cette ligne de cron exécute la commande `certbot renew` chaque jour à minuit.

## Démarrage et vérification

1. **Activez les fichiers de configuration** :

   ```bash
   sudo a2ensite ChordFinder.conf
   sudo a2ensite ChordFinder-le-ssl.conf
   sudo systemctl reload apache2
   ```

2. **Vérifiez que le service Apache fonctionne** :

   ```bash
   sudo systemctl status apache2
   ```

3. **Testez l'application en HTTPS** :

   Ouvrez un navigateur et accédez à `https://my_domaine.com/ChordFinder/`.