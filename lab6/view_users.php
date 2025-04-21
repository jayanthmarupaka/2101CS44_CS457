<?php
session_start();
require 'db_config.php';

// Redirect if not logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

// Check if user is admin
if ($_SESSION['role'] !== 'admin') {
    echo "<script>alert('Access Denied! Only admins can view users.'); window.location.href='dashboard.php';</script>";
    exit();
}

// Verify admin password
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $admin_password = $_POST['admin_password'];
    
    // Fetch admin's password from database
    $stmt = $conn->prepare("SELECT password FROM users WHERE username=? AND role='admin'");
    $stmt->bind_param("s", $_SESSION['username']);
    $stmt->execute();
    $stmt->bind_result($hashed_password);
    $stmt->fetch();
    $stmt->close();

    // Check if password is correct
    if (!password_verify($admin_password, $hashed_password)) {
        echo "<script>alert('Incorrect Admin Password!'); window.location.href='dashboard.php';</script>";
        exit();
    }
} else {
    header("Location: dashboard.php");
    exit();
}

// Fetch all users
$result = $conn->query("SELECT id, username, role FROM users");

echo "<h2>User List</h2>";
echo "<table border='1'><tr><th>ID</th><th>Username</th><th>Role</th></tr>";
while ($row = $result->fetch_assoc()) {
    echo "<tr><td>{$row['id']}</td><td>{$row['username']}</td><td>{$row['role']}</td></tr>";
}
echo "</table>";
echo "<br><a href='dashboard.php'><button>Back to Dashboard</button></a>";

$conn->close();
?>
