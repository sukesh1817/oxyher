<?php

function get_sess_id()
{
    // Include the domain configuration json file.
    $jsonFile = '/var/www/api.oxyher.com/config/url/domain.json';
    $jsonData = file_get_contents($jsonFile);
    $url_data = json_decode($jsonData, true);
    $url = $url_data['SESSION_URL'];

    // Check if the session cookie exists.
    if (isset($_COOKIE['session'])) {
        $session_value = $_COOKIE['session'];
        $cookie = "session=$session_value;";

        // Initialize cURL session.
        $ch = curl_init($url);

        // Set cURL options.
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            "Cookie: $cookie",
            "User-Agent: PHP-CURL"
        ]);

        // Execute cURL request.
        $response = curl_exec($ch);

        // Check for cURL errors.
        if (curl_errno($ch)) {
            echo "cURL Error: " . curl_error($ch);
        } else {
            // Decode the JSON response.
            $session_data = json_decode($response, true);
            return $session_data['auth_id'];

        }
        // Close cURL session.
        curl_close($ch);
        return "SESSION_ERROR";
    } else {
        return "SESSION_NOT_FOUND";
    }
}


