<?php

require_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';
use \Firebase\JWT\JWT;


function make_the_redirection($amount)
{
    // Load the private key
    
    $privateKey = file_get_contents('/var/www/oxyher/sec_keys/private_key.pem');
    // Prepare the payload (add any necessary data)
    $payload = [
        'origin' => 'https://payments.oxyher.com',  // The origin (to match in Flask)
        'exp' => time() + 300,            // Set expiration time (e.g., )
        'amt' => $amount
    ];

    // Encode the JWT with the private key
    $jwt = JWT::encode($payload, $privateKey, 'RS256');

    // Print or pass the JWT in the query string to Flask
    $php_subdomain_url = "https://test.oxyher.com/shop/order/make";
    $redirect_url = $php_subdomain_url . "?_sign=" . $jwt;
    return $redirect_url;
}


