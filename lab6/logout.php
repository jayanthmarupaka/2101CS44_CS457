<?php
session_start();
session_destroy();  // Destroy the session
header("Location: register.php");  // Redirect to register page
exit();
?>
