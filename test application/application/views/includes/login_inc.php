<?php

session_start();

if (isset($_POST['submit'])){
	include_once 'dbh_inc.php';

	$username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);

    if (empty($username) || empty($password)) {
    	header("Location: " .base_url(). "login?login=empty");
    	exit();

    }else{
		$mysqli_stmt = $conn->prepare("SElECT * FROM usertest WHERE Username=? OR Email=?");
		$mysqli_stmt->bind_param("ss", $Username, $Email);
		$Username = "$username";
		$Email = "$username";

		$mysqli_stmt->execute();
		$mysqli_stmt->bind_result($ID, $Username, $Email, $Password, $Icon, $Gender, $Address, $Country, $Phone);
		$result = array();
		while($mysqli_stmt->fetch()){
			array_push($result, $ID, $Username, $Email, $Password, $Icon, $Gender, $Address, $Country, $Phone);
		}

    	if(sizeof($result) < 1){
			header("Location: " .base_url(). "login?login=invalid_id");
    		exit();
    	} else {
			//De-hashing the password
			$hashedPwdCheck = password_verify($password, $result[3]);

			if($hashedPwdCheck == false){
				header("Location: " .base_url(). "index?login=invalid_password");
				exit();

			} elseif ($hashedPwdCheck == true){
				//Log in the user here
				$_SESSION['u_id'] = $result[0];
				$_SESSION['u_email'] = $result[2];
				$_SESSION['u_name'] = $result[1];
				$_SESSION['u_phone'] = $result[8];
				$_SESSION['u_address'] = $result[6];
				$_SESSION['u_gender'] = $result[5];
				$_SESSION['u_country'] = $result[7];
				// echo $_SESSION['u_id'];
				header("Location: " .base_url(). "index");
				exit();
			}
    	}
    }
} else{
    header("Location: " .base_url(). "login?db=conn_error");
	exit();
}