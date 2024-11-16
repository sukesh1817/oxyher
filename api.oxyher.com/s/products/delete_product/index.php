<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';

header("Access-Control-Allow-Origin: https://test.oxyher.com");
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Access-Control-Allow-Credentials: true");

if (isset($_GET['p_id'])) {

    // load json file, contains domain information
    $jsonFile = '/var/www/api.oxyher.com/config/url/domain.json';
    $jsonData = file_get_contents($jsonFile);
    $url = json_decode($jsonData, true);

    // mongodb configuration
    $client = new MongoDB\Client("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.1"); // Change the URI if needed
    $db = $client->selectDatabase('product_hygeine');
    $collection = $db->selectCollection('intimate_wash');
    $filter = ['product_id' => $_GET['p_id']];
    try {
        // Delete a single document that matches the filter
        $deleteResult = $collection->deleteOne($filter);
    
        // Check if the delete was successful
        if ($deleteResult->getDeletedCount() > 0) {
            echo json_encode(['status' => '1', 'message' => 'Product deleted successfully.']);
        } else {
            echo json_encode(['status' => '0', 'message' => 'No product found with the given ID.']);

        }
    } catch (Exception $e) {
        echo json_encode(['status' => '-1', 'message' => 'Error deleting product: ' ]);
    }


    
}

