<?php

if (isset($_POST['submit'])){
	include_once 'dbh_inc.php';

    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
	$email = mysqli_real_escape_string($conn, $_POST['email']);
    $phone = mysqli_real_escape_string($conn, $_POST['phone']);
	$address = mysqli_real_escape_string($conn, $_POST['address']);
	$country = mysqli_real_escape_string($conn, $_POST['country']);
    $gender = $_POST['gender'];

	//Error handlers
	//Check for empty fields
	if (empty($username) || empty($password) || empty($email) || empty($phone) 
        || empty($gender) || empty($address) || empty($country)) {
		header("Location: ../signup.php?signup=empty");
		exit();

	} else {
		if (!preg_match("/^[a-zA-Z0-9]*$/", $username)) {
    		header("Location: ../signup.php?signup=invalidusername");
    		exit();

    	}else{
    		if(!filter_var($email, FILTER_VALIDATE_EMAIL)){
            	header("Location: ../signup.php?signup=$email+invailemail");
            	exit();

    		}else{
    			$sql = "SELECT * FROM usertest WHERE Username = '$username'";
    			$result = mysqli_query($conn, $sql);
    			$resultCheck = mysqli_num_rows($result);

    			if($resultCheck > 0){
    				header("Location:../signup.php?signup=usertaken");
    				exit();

				}else{
					$sql = "SELECT * FROM usertest WHERE Email = '$email'";
					$result = mysqli_query($conn, $sql);
					$resultCheck = mysqli_num_rows($result);

					if($resultCheck > 0){
						header("Location:../signup.php?signup=emailtaken");
						exit();
					}else{
						$hashedPwd = password_hash($password, PASSWORD_DEFAULT);

						if(!preg_match("/^[0-9]*$/", $phone)){
							header("Location: ../signup.php?signup=$phone+invailphone");
							exit();

						}else{
							$sql = "INSERT INTO usertest (Username, Password, Email, Phone, Address, Gender, Country) VALUES 
								('$username', '$hashedPwd','$email', '$phone', '$address', '$gender', '$country');";
						}

						mysqli_query($conn, $sql);
						//echo "Error updating record: " . $conn->error;
						header("Location:../pages/login.php?signup=success");
						exit();
					}
				}	
    		}
    	}
	}

}else {
	header("Location: ../signup.php?signup=conn_error");
	exit();
}