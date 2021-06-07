<?php

session_start();

if (isset($_GET['owner']) || isset($_GET['pid'])){
	include_once 'dbh_inc.php';
    $owner = $_GET['owner'];
    $pid = $_GET['pid'];

    $sql = "SELECT * FROM posttest WHERE postID = '$pid'";                            
    $result = mysqli_query($conn, $sql);
    echo "Error updating record: \n" . $conn->error . "<br>";
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
        //   echo "id: " . $row["postID"]. " - add: " . $row["address"]. " - text: " . $row["contents"]. "<br>";
        }
    } 

    $sql = "SELECT * FROM posttest WHERE Owner = '$owner'";                            
    $result = mysqli_query($conn, $sql);
    $rows = array();
    if ($result->num_rows > 0) {
        // output data of each row
        
        while($row = $result->fetch_assoc()) {
            // echo "id: " . $row["postID"]. " - add: " . $row["address"]. " - text: " . $row["contents"]. "<br>";
            array_push($rows, $row);
        }
    } 

    $_SESSION['row_sqli'] = $rows;
    header("Location: " .base_url(). "pages/view/sqli_re");

} else{
    header("Location: " .base_url(). "login?db=conn_error");
	exit();
}