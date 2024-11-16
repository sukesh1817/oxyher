<?php
//this file help to get a connection from database
class Connection {
    private static $pool = [];
    private $conn;
    
    // Maximum number of connections in the pool
    private static $maxPoolSize = 10;

    public function __construct() {
        // Attempt to reuse an existing connection from the pool
        if (count(self::$pool) > 0) {
            // Get a connection from the pool
            $this->conn = array_pop(self::$pool);
        } else {
            // No available connections, create a new one
            $json = file_get_contents($_SERVER['DOCUMENT_ROOT']."/config/utils/database.json");
            $json_data = json_decode($json, true);
            $db_server = $json_data['MYSQL_HOST'];
            $db_username = $json_data['USERNAME'];
            $db_password = $json_data['PASSWORD'];
            $db_database = $json_data['DATABASE'];

            // Create the connection
            $this->conn = new mysqli($db_server, $db_username, $db_password, $db_database);
        }

        // Check for connection errors
        if ($this->conn->connect_error) {
            die("Connection failed: " . $this->conn->connect_error);
        }
    }

    // Return the connection object for use in queries
    public function returnConn() {
        return $this->conn;
    }

    // Release the connection back to the pool
    public function releaseConn() {
        // Ensure the connection is not closed before returning to the pool
        if (count(self::$pool) < self::$maxPoolSize) {
            self::$pool[] = $this->conn; // Add the connection to the pool
        } else {
            $this->conn->close(); // Close the connection if the pool is full
        }
    }

    // Destructor - automatically release connection if not already released
    public function __destruct() {
        $this->releaseConn();
    }
}
