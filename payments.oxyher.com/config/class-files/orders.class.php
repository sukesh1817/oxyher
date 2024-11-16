<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/vendor/autoload.php'; // Load MongoDB library if installed via Composer
require_once $_SERVER['DOCUMENT_ROOT'] . '/config/class-files/connection.class.php'; // Load MongoDB library if installed via Composer
use MongoDB\Client;




class Orders
{
    public function make_new_order($auth_id)
    {
        // Mongodb configurations.
        $client = new Client("mongodb://localhost:27017", [
            'maxPoolSize' => 10, // Maximum number of connections in the pool
            'minPoolSize' => 1,  // Minimum number of connections in the pool
            'connectTimeoutMS' => 10000 // Timeout in milliseconds
        ]);
        $database = $client->user;
        $collection = $database->orders;

        // Mysql stuffs.
        $sql_conn = new Connection();
        $conn = $sql_conn->returnConn();
        $sql = "SELECT * FROM user_details where username='$auth_id'";
        $result = $conn->query($sql);
        $data = $result->fetch_assoc();
        if ($result && $data['username']) {
            // Ensures all the data is properly set.

        }
    }
}
?>