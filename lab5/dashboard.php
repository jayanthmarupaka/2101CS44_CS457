<?php
session_start();
require 'db_config.php';

// Redirect if not logged in
if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit();
}

$username = $_SESSION['username']; // ✅ Get logged-in username
$role = $_SESSION['role'];

// Hide "Editor" and "Viewer" from welcome message
$display_role = ($role == "admin") ? " ($role)" : "";

echo "<h2>Welcome, {$username}{$display_role}</h2>";

// View Students Button
echo '<a href="view_students.php"><button>View Students</button></a>';

// Edit Students Button
echo '<button onclick="confirmEdit()">Edit Students</button>';

// View Users (Admin Only)
echo '<button onclick="adminAuth(\'view_users.php\')">View Users</button>';

// Edit Users (Admin Only)
echo '<button onclick="adminAuth(\'edit_users.php\')">Edit Users</button>';

// Logout Button
echo '<a href="logout.php"><button>Logout</button></a>';
?>

<script>
function confirmEdit() {
    var role = "<?php echo $_SESSION['role']; ?>";
    if (role === "viewer") {
        alert("Access Denied! Viewers cannot edit.");
    } else {
        window.location.href = "edit_students.php";
    }
}

function adminAuth(page) {
    var role = "<?php echo $_SESSION['role']; ?>";
    if (role !== "admin") {
        alert("Access Denied! Only admins can access this.");
        return;
    }

    var password = prompt("Enter Admin Password:");
    if (password) {
        var form = document.createElement("form");
        form.method = "POST";
        form.action = page;

        var input = document.createElement("input");
        input.type = "hidden";
        input.name = "admin_password";
        input.value = password;
        form.appendChild(input);

        document.body.appendChild(form);
        form.submit();
    }
}
</script>
