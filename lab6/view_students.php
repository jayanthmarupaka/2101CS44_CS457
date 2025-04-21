<?php
session_start();
require 'db_config.php';


$result = $conn->query("SELECT * FROM stud_info");

echo "<h2>Student Information</h2>";
while ($row = $result->fetch_assoc()) {
    echo "{$row['roll']}. {$row['name']} ({$row['age']}) - {$row['branch']} - {$row['hometown']}<br>";
}

echo '<a href="dashboard.php"><button>Back</button></a>';
?>
