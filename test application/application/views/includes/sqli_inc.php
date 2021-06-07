<?php

session_start();

if (isset($_POST['owner']) || isset($_POST['pid'])){
	include_once 'dbh_inc.php';
    $owner = $_POST['owner'];
    $pid = $_POST['pid'];

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
    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
          echo "id: " . $row["postID"]. " - add: " . $row["address"]. " - text: " . $row["contents"]. "<br>";
        }
    } 

} else{
    header("Location: ../login.php?login=haven't_login");
	exit();
}