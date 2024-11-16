<?php

$allowed_origins = [
    "https://test.oxyher.com",
    "https://oxyher.com"
];

// Get the Origin header from the incoming request
if (isset($_SERVER['HTTP_ORIGIN'])) {
    $origin = $_SERVER['HTTP_ORIGIN'];

    // Check if the origin is in the allowed origins array
    if (in_array($origin, $allowed_origins)) {
        // Set the Access-Control-Allow-Origin header to the matching origin
        header("Access-Control-Allow-Origin: $origin");
        header("Access-Control-Allow-Methods: GET, POST, OPTIONS");
        header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");
        header("Access-Control-Allow-Credentials: true");
        header("Content-Type: application/json");

    }
}
require_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';
require_once $_SERVER['DOCUMENT_ROOT'] . "/config/functions/get_session.php";
require_once $_SERVER['DOCUMENT_ROOT'] . "/config/functions/get_product_details.php";

if (!isset($_COOKIE['session'])) {
    echo json_encode(["Status" => "Unauthorized"]);
    exit(-1);
}

$jsonData = file_get_contents('php://input');
$cart = json_decode($jsonData, true);

$cart['rem_id'] = isset($cart['rem_id']) ? filter_var($cart['rem_id'], FILTER_SANITIZE_STRING) : null;
$cart['p_id'] = isset($cart['p_id']) ? filter_var($cart['p_id'], FILTER_SANITIZE_STRING) : null;
$cart['q'] = isset($cart['q']) ? filter_var($cart['q'], FILTER_VALIDATE_INT) : null;

$client = new MongoDB\Client("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.1");  // MongoDB connection
$db = $client->selectDatabase('user');
$collection = $db->selectCollection('cart');


if (isset($cart['rem_id'])) {
    ini_set('display_errors', 1);

    // Set the error reporting level to report all errors
    error_reporting(E_ALL);
    $auth_id = get_sess_id();
    $filter = [
        '_id' => $auth_id,
        "products." . $cart['rem_id'] => ['$exists' => true],
        "prices." . $cart['rem_id'] => ['$exists' => true],

    ];

    // Perform the update operation to remove the specific product
    $result = $collection->updateOne(
        $filter,
        ['$unset' => ["products." . $cart['rem_id'] => "", "prices." . $cart['rem_id'] => ""]] // Remove the specific product
    );





    // Check if the deletion was successful
    if ($result->getModifiedCount() === 1) {
        echo json_encode(["status" => "dataDeletedSuccess"]);
    } else {
        echo json_encode(["status" => "dataDeletedFailed"]);
    }
} else if (isset($cart['p_id']) && isset($cart['q'])) {
    // ini_set('display_errors', 1);
    // ini_set('display_startup_errors', 1);
    // error_reporting(E_ALL);
    $auth_id = get_sess_id();
    $filter = [
        '_id' => $auth_id,
        "products." . $cart['p_id'] => ['$exists' => true],
        "prices." . $cart['p_id'] => ['$exists' => true]
    ];
    $result = $collection->findOne($filter);


    if ($result) {
        if ($cart['q'] > 0) {
            $product_data = json_decode(get_individual_product($pid = $cart['p_id']), true);
            $product_price = $product_data['price'];
            $filter = [
                '_id' => $auth_id
            ];
            $update = [
                '$set' => [
                    "products.{$cart['p_id']}" => $cart['q'],
                    "prices.{$cart['p_id']}" => $product_price * $cart['q']
                ],
            ];
            $result = $collection->updateOne($filter, $update, ['upsert' => true]);
            if ($result->getModifiedCount() > 0) {
                echo json_encode(["status" => "dataUpdatedSuccess"]);
            } else {
                echo json_encode(["status" => "dataUpdatedFailed"]);
            }
        } else {
            echo json_encode(["status" => "nullResult"]);
        }
    } else {
        echo json_encode(["status" => "dataUpdatedFailed"]);
    }



} else {
    echo json_encode(["status" => "someThingWentWrong"]);
}


