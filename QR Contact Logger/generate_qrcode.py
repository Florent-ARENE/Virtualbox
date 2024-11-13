import csv
import qrcode
import os
import base64
import json

# Chemin vers le fichier CSV
csv_file = 'fichier.csv'

# Créer un répertoire pour les QR codes s'il n'existe pas déjà
output_dir = 'qrcodes'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Lire le fichier CSV avec le délimiteur ';' et l'encodage ISO-8859-1
with open(csv_file, mode='r', newline='', encoding='ISO-8859-1') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        # Extraire le nom et prénom
        nom = row['nom'].strip()  # Suppression des espaces en trop
        prenom = row['prenom'].strip()
        
        # Créer un dictionnaire pour le nom et le prénom
        data = {"nom": nom, "prenom": prenom}
        
        # Convertir le dictionnaire en chaîne JSON, puis encoder en Base64
        json_data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        content_base64 = base64.urlsafe_b64encode(json_data).decode('utf-8')
        
        # Créer l'URL avec le paramètre encodé
        qr_content = f'https://virtualbox.net/qrcode/?data={content_base64}'
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)

        # Créer une image du QR code
        img = qr.make_image(fill='black', back_color='white')

        # Sauvegarder l'image avec le nom de la personne
        img_file = os.path.join(output_dir, f'{nom}_{prenom}.png')
        img.save(img_file)

        print(f'QR code généré pour {nom} {prenom} : {img_file}')
