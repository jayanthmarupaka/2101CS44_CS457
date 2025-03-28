<?php
session_start();
require 'db_config.php';

// Only allow access if user is an editor or admin
if ($_SESSION['role'] == "viewer") {
    die("Access Denied! Viewers cannot edit.");
}

// Handle Editing
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $roll = $_POST['roll'];
    $new_name = $_POST['name'];
    $new_age = $_POST['age'];
    $new_branch = $_POST['branch'];
    $new_hometown = $_POST['hometown'];

    $stmt = $conn->prepare("UPDATE stud_info SET name=?, age=?, branch=?, hometown=? WHERE roll=?");
    $stmt->bind_param("sissi", $new_name, $new_age, $new_branch, $new_hometown, $roll);
    
    if ($stmt->execute()) {
        echo "Updated successfully!";
    } else {
        echo "Error updating record.";
    }
}

// Show Student Edit Form
$result = $conn->query("SELECT * FROM stud_info");
while ($row = $result->fetch_assoc()) {
    echo "<form method='POST'>
        <input type='hidden' name='roll' value='{$row['roll']}'>
        <input type='text' name='name' value='{$row['name']}' required>
        <input type='number' name='age' value='{$row['age']}' required>
        <input type='text' name='branch' value='{$row['branch']}' required>
        <input type='text' name='hometown' value='{$row['hometown']}' required>
        <button type='submit'>Update</button>
    </form><br>";
}

echo '<a href="dashboard.php"><button>Back</button></a>';
?>
