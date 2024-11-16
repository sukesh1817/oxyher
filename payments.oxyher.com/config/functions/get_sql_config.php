<?php

function get_sql_config()
{
    // Path to the JSON file
    $filename = $_SERVER['DOCUMENT_ROOT'] . '/config/utils/database.json';
    // Read the JSON file contents
    $jsonData = file_get_contents($filename);

    // Check if the file reading was successful
    if ($jsonData === false) {
        // Unable to get the file contents.
        return ;
    }

    // Decode JSON data into a PHP associative array
    $dataArray = json_decode($jsonData, true);

    // Decode JSON data into a PHP object
    $dataObject = json_decode($jsonData);

    // Check for JSON decoding errors
    if (json_last_error() !== JSON_ERROR_NONE) {
        // Json parse error.
        return ;
    }

    // Output the data
    return $dataArray;
}