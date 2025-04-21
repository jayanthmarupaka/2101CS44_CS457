<?php
session_start();
require 'db_config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $entered_password = $_POST['password'];
    $username = $_SESSION['username'];

    $stmt = $conn->prepare("SELECT password FROM users WHERE username=?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->bind_result($hashed_password);
    $stmt->fetch();
    
    if (password_verify($entered_password, $hashed_password)) {
        echo "success";
    } else {
        echo "fail";
    }
}
?>
