<?php
// Chemin vers le fichier CSV
$csvFile = 'scans.csv';

// Fonction pour ajouter les données dans le CSV avec ISO-8859-1 et séparateur ;
function ajouterScan($nom, $prenom, $csvFile) {
    // Charger tous les scans existants pour vérifier les doublons
    $scans = [];
    if (file_exists($csvFile)) {
        $file = fopen($csvFile, 'r');
        while (($data = fgetcsv($file, 1000, ";")) !== false) {
            $scans[] = $data;
        }
        fclose($file);
    }

    // Vérifier si le couple nom/prénom est déjà présent
    foreach ($scans as $scan) {
        if ($scan[0] === $nom && $scan[1] === $prenom) {
            return; // Si le couple est déjà dans le fichier, on quitte la fonction sans ajouter
        }
    }

    // Ajouter le nom et prénom au fichier CSV avec encodage ISO-8859-1
    $file = fopen($csvFile, 'a');
    fputcsv($file, [$nom, $prenom], ";");
    fclose($file);
}

// Vérifier si le paramètre 'data' est présent dans l'URL
if (isset($_GET['data'])) {
    // Récupérer le paramètre 'data' depuis l'URL
    $data = $_GET['data'];
    
    // Décoder le paramètre en Base64 avec UTF-8
    $decodedData = base64_decode($data);
    if ($decodedData === false) {
        echo "<p style='color: red;'>Erreur de décodage Base64</p>";
        exit();
    }
    
    // Décoder le JSON
    $dataArray = json_decode($decodedData, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        echo "<p style='color: red;'>Erreur de décodage JSON : " . json_last_error_msg() . "</p>";
        exit();
    }
    
    // Récupérer nom et prénom
    $nom = $dataArray['nom'];
    $prenom = $dataArray['prenom'];

    // Ajouter les données dans le fichier CSV (en vérifiant les doublons)
    ajouterScan($nom, $prenom, $csvFile);

    // Rediriger pour éviter la réinsertion en cas d'actualisation
    header("Location: index.php");
    exit();  // Terminer l'exécution pour éviter d'autres traitements
}

// Lire les données déjà scannées
$scans = [];
if (file_exists($csvFile)) {
    $file = fopen($csvFile, 'r');
    while (($data = fgetcsv($file, 1000, ";")) !== false) {  // Utilisation de ';' comme séparateur
        $scans[] = $data;
    }
    fclose($file);
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="ISO-8859-1">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informations Utilisateur</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Informations Utilisateur</h1>
    
    <?php if (isset($nom) && isset($prenom)): ?>
        <p>Nom : <?= htmlspecialchars($nom) ?></p>
        <p>Prénom : <?= htmlspecialchars($prenom) ?></p>
    <?php else: ?>
        <p>Aucune information trouvée.</p>
    <?php endif; ?>
    
    <h2>Scans précédents</h2>
    <?php if (count($scans) > 0): ?>
        <table border="1">
            <tr>
                <th>Nom</th>
                <th>Prénom</th>
            </tr>
            <?php foreach ($scans as $scan): ?>
                <tr>
                    <td><?= htmlspecialchars($scan[0]) ?></td>
                    <td><?= htmlspecialchars($scan[1] ?? '') ?></td>
                </tr>
            <?php endforeach; ?>
        </table>
    <?php else: ?>
        <p>Aucun scan enregistré.</p>
    <?php endif; ?>

    <h2>Exporter en CSV</h2>
    <div class="button-container">
        <a href="export_scans.php" download="scans.csv">Télécharger le fichier CSV</a>
    </div>
</body>
</html>
