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
    echo "<script>alert('Access Denied! Only admins can edit users.'); window.location.href='dashboard.php';</script>";
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

// Handle User Update
if (isset($_POST['update_user'])) {
    $id = $_POST['id'];
    $username = $_POST['username'];
    $role = $_POST['role'];

    $stmt = $conn->prepare("UPDATE users SET username=?, role=? WHERE id=?");
    $stmt->bind_param("ssi", $username, $role, $id);
    $stmt->execute();
    $stmt->close();

    echo "<script>alert('User Updated Successfully!'); window.location.href='edit_users.php';</script>";
}

// Fetch users
$result = $conn->query("SELECT id, username, role FROM users");

echo "<h2>Edit Users</h2>";
echo "<table border='1'><tr><th>ID</th><th>Username</th><th>Role</th><th>Action</th></tr>";
while ($row = $result->fetch_assoc()) {
    echo "<tr>
            <form method='POST'>
                <td>{$row['id']} <input type='hidden' name='id' value='{$row['id']}'></td>
                <td><input type='text' name='username' value='{$row['username']}' required></td>
                <td>
                    <select name='role'>
                        <option value='admin' " . ($row['role'] == 'admin' ? 'selected' : '') . ">Admin</option>
                        <option value='editor' " . ($row['role'] == 'editor' ? 'selected' : '') . ">Editor</option>
                        <option value='viewer' " . ($row['role'] == 'viewer' ? 'selected' : '') . ">Viewer</option>
                    </select>
                </td>
                <td><button type='submit' name='update_user'>Update</button></td>
            </form>
          </tr>";
}
echo "</table>";
echo "<br><a href='dashboard.php'><button>Back to Dashboard</button></a>";

$conn->close();
?>
