<?php
use Dwivedianuj9118\PhonePePaymentGateway\PhonePe;
require_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php';
use \Firebase\JWT\JWT;
use \Firebase\JWT\Key;

session_start();

// Load the public key
$publicKey = file_get_contents('/var/www/oxyher/sec_keys/public_key.pem');

// Retrieve the signature from the URL query parameter
if (isset($_GET['_sign'])) {
    $signature = $_GET['_sign'];

    // Check if the token has already been used
    if (isset($_SESSION['used_signature']) && $_SESSION['used_signature'] === $signature) {
        header("Content-Type: application/json");
        echo json_encode(["Response" => "This token has already been used."]);
        exit;
    }

    try {
        // Decode and verify the JWT using the public key wrapped in a Key object
        $decoded = JWT::decode($signature, new Key($publicKey, 'RS256'));

        // Check the origin in the payload
        if ($decoded->origin === "https://oxyher.com") {
            $config = new PhonePe('M226I0MHQCBFO', '742a5cdb-62f9-4ba3-af92-05fbae758cc8', 1); //merchantId, SaltKey, SaltIndex
            $merchantTransactionId = 'M226I0MHQCBFO' . substr(uniqid(), 1); // Unique Random transaction Id
            $merchantOrderId = 'M226I0MHQCBFO' . mt_rand(1000, 99999); // Order Id
            $amount = $decoded->amt * 100;  // Amount in Paisa or amount * 100
            // $amount = 1 * 100;  // Example amount in Paisa
            $redirectUrl = "https://payments.oxyher.com/v1/pay/status/"; // Redirect URL after Payment success or fail
            $mode = "PRODUCTION"; // Payment Mode: UAT (test) or PRODUCTION (production)
            $callbackUrl = "https://payments.oxyher.com/v1/pay/status/"; // Callback URL after Payment success or fail

            $mobileNumber = $decoded->mob_num; // Mobile No from token
            $data = $config->PaymentCall("$merchantTransactionId", "$merchantOrderId", "$amount", "$redirectUrl", "$callbackUrl", "$mobileNumber", "$mode");

            // Store the signature in the session to mark it as used
            $_SESSION['used_signature'] = $signature;

            // Redirect to PhonePe payment gateway
            header('Location:' . $data['url']);
        } else {
            header("Content-Type: application/json");
            echo json_encode(["Response" => "Invalid origin"]);
        }

    } catch (Exception $e) {
        // Handle any decoding errors
        header("Content-Type: application/json");
        echo json_encode(["Response" => "Signature failed"]);
    }
} else {
    header("Content-Type: application/json");
    echo json_encode(["Request" => "Unauthorized"]);
}




// $config = new PhonePe('M226I0MHQCBFO', '742a5cdb-62f9-4ba3-af92-05fbae758cc8', 1);//merchantId,SaltKey,SaltIndex after onboarding PhonePe Payment gateway you will got this.
// $merchantTransactionId = 'M226I0MHQCBFO' . substr(uniqid(), 1);// Uqique Randoe transcation Id
// $merchantOrderId = 'M226I0MHQCBFO' . mt_rand(1000, 99999);// orderId
// $amount = 100;  // Amount in Paisa or amount*100
// $redirectUrl = "https://payments.oxyher.com/v1/pay/status/";    // Redirect Url after Payment success or fail
// $mode = "PRODUCTION"; // MODE or PAYMENT UAT(test) or PRODUCTION(production)
// $callbackUrl = "https://payments.oxyher.com/v1/pay/status/";//Callback Url after Payment success or fail get response
// $mobileNumber = "9600944093";   //Mobile No
// $data = $config->PaymentCall("$merchantTransactionId", "$merchantOrderId", "$amount", "$redirectUrl", "$callbackUrl", "$mobileNumber", "$mode");// call function to get response form phonepe like url,msg,status
// header('Location:' . $data['url']); 