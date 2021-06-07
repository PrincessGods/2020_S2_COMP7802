<?php


session_start();
$url = $_SESSION['url'];
//session_unset();
//session_destroy();
unset($_SESSION['u_id']);
unset($_SESSION['u_email']);
unset($_SESSION['u_name']);
unset($_SESSION['u_phone']);
unset($_SESSION['u_address']);
unset($_SESSION['u_gender']);
unset($_SESSION['u_country']);
header("Location: " .base_url(). "index");
exit();