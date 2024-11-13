<?php /* export_scans.php */
$csvFile = 'scans.csv';

// Ouvrir le fichier CSV et lire les données
if (file_exists($csvFile)) {
    // Définir les en-têtes pour le téléchargement du CSV
    header('Content-Type: text/csv; charset=ISO-8859-1');
    header('Content-Disposition: attachment; filename="scans.csv"');

    // Lire le fichier et convertir en ISO-8859-1 à la volée
    $output = fopen('php://output', 'w');
    
    // Ouvrir le fichier CSV en lecture
    $file = fopen($csvFile, 'r');
    
    while (($data = fgetcsv($file, 1000, ";")) !== false) {
        // Convertir chaque ligne en ISO-8859-1 pour assurer la compatibilité avec Excel
        $data = array_map(function($field) {
            return iconv('UTF-8', 'ISO-8859-1//TRANSLIT', $field);
        }, $data);
        
        fputcsv($output, $data, ";"); // Écrire chaque ligne dans le fichier de sortie
    }
    fclose($file);
    fclose($output);
}
exit;
