#!/usr/bin/python3
import sys
import site

# Ajouter le chemin du projet
sys.path.insert(0, '/var/www/html/ChordFinder')

# Ajouter explicitement les packages de l'environnement virtuel
site.addsitedir('/var/www/html/ChordFinder/venv/lib/python3.12/site-packages')

from app import app as application

if __name__ == "__main__":
    application.run()
