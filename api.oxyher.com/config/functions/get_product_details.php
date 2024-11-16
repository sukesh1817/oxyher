<?php 
include_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';

function get_individual_product($p_id) {
        try {
            $client = new MongoDB\Client("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.1"); // Change the URI if needed
            // Get a list of all databases
            $databases = $client->listDatabaseNames();

            // Loop through the databases
            foreach ($databases as $db_name) {
                // Skip system databases
                if (in_array($db_name, ['config', 'admin', 'local', 'user'])) {
                    continue;
                }

                // Access the database
                $database = $client->$db_name;
                $collections = $database->listCollectionNames(); // Get all collections in the database

                // Loop through the collections
                foreach ($collections as $collection_name) {
                    $collection = $database->$collection_name;

                    // Search for the product in the current collection by `product_id`
                    $product = $collection->findOne(['product_id' => $p_id]);

                    // If the product is found, return it
                    if ($product) {
                        return json_encode($product); // Convert MongoDB document to JSON
                    }
                }
            }

            // If the product is not found in any collection
            $error = ["CODE" => 404, "ERROR" => "PRODUCT_NOT_FOUND"];
            return json_encode($error);
            
        } catch (Exception $e) {
            // Log the error message (optional: add proper logging)
            $error = ["CODE" => 500, "ERROR" => "UNABLE_TO_GET_PRODUCT", "DETAIL" => $e->getMessage()];
            return json_encode($error);
        }
    }