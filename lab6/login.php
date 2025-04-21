<?php
session_start();
require 'db_config.php';
require_once 'jwt/src/JWT.php';
require_once 'jwt/src/Key.php';

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

$secret_key = "keyissimple";
$issuer = "localhost"; 

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = trim($_POST['username']);
    $password = trim($_POST['password']);

    $stmt = $conn->prepare("SELECT username, password, role FROM users WHERE username=?");
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        $stmt->bind_result($db_username, $hashed_password, $role);
        $stmt->fetch();

        if (password_verify($password, $hashed_password)) {
            $issuedAt = time();
            $exp = $issuedAt + 3600; // token valid for 1 hour

            $payload = [
                "iss" => $issuer,
                "iat" => $issuedAt,
                "exp" => $exp,
                "data" => [
                    "username" => $db_username,
                    "role" => $role
                ]
            ];

            $jwt = JWT::encode($payload, $secret_key, 'HS256');
            setcookie("jwt_token", $jwt, $exp, "/", "", false, true); // HttpOnly cookie

            header("Location: dashboard.php");
            exit();
        } else {
            $error = "Invalid password!";
        }
    } else {
        $error = "User not found!";
    }
    $stmt->close();
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <?php if (isset($error)) echo "<p style='color:red;'>$error</p>"; ?>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br>
        <label>Password:</label>
        <input type="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    <br>
    <a href="register.php"><button>Register</button></a>
</body>
</html>
