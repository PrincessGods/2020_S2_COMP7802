<?php

session_start();

if (isset($_POST['submit']) && isset($_SESSION['u_id'])){
    include_once 'dbh_inc.php';
    echo $_SESSION['u_id'] . "\n";
	
	//$pid = mysqli_real_escape_string($conn, $_POST['pid']);
	$pid = $_POST['pid'];
	$title = mysqli_real_escape_string($conn, $_POST['title']);
	//echo "\n" . $title . "\n";
	//$title = $_POST['title'];
    $content = mysqli_real_escape_string($conn, $_POST['message-text']);
    $type = mysqli_real_escape_string($conn, $_POST['type']);
    $address = $_SESSION['u_address'];
    $uid = $_SESSION['u_id'];
    $owner = $_SESSION['u_name'];

    //echo $pid . $title . $content . $type . "\n";

    if (empty($title) || empty($content)) {
    	header("Location: ../index.php?post=empty");
        exit();
    } else {
        $sql = "INSERT INTO posttest (postID, address, contents, title, type, Owner) VALUES 
                ('$pid', '$address', '$content','$title', '$type', '$owner');";
                                
        mysqli_query($conn, $sql);
		//echo "\n" . $sql . "\n";
		
		echo "Error updating record: \n" . $conn->error;

        $postID = mysqli_insert_id($conn);

        $sql = "INSERT INTO user_post_relationship (U_id, P_id) VALUES 
                ('$uid', '$postID');";
                                
        mysqli_query($conn, $sql);

        echo "\nError updating record: \n" . $conn->error;
        header("Location: ../index.php?post=suceessfully");
        exit();
    }

} else{
    echo $_SESSION['u_id'] . "\n";
    header("Location: ../login.php?login=haven't_login");
	exit();
}