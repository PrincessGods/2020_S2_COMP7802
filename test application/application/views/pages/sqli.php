<div id="main" class="container d-flex flex-column mt-4">
     <?php 
        $attr = array('class'=>'px-2 col-12', 'id'=>"postForm", 'method'=>"POST");
        echo form_open("includes/sqli_inc/", $attr); 
    ?>
        <fieldset>
            <div class="form-group">
                <label for="pid" class="col-form-label">PID:</label>
                <input type="text" id ="postPid" name = "pid" class="form-control" />
            </div>
            <div class="form-group">
                <label for="owner" class="col-form-label">Owner:</label>
                <input type="text" id ="postTitle" name = "owner" class="form-control" />
            </div>

            <div class="form-group">
                <label for="message-text" class="col-form-label">Contents:</label>
                <textarea rows="4" name="message-text" id ="message-text" class="form-control"></textarea>
            </div>
        </fieldset>

        <div class="form-label-group d-flex mt-2">
            <button class="btn btn-primary col-2 ml-auto mb-2 text-light" type="submit" name="submit">Post</button>
        </div>
    </form>
</div>

<div id="main" class="container d-flex flex-column mt-4">
    <form action="http://localhost/CodeIgniter/includes/sqli_inc_get/" method="GET" class="px-2 col-12" id="sqliForm" accept-charset="utf-8">
        <fieldset>
            <div class="form-group">
                <label for="pid" class="col-form-label">PID:</label>
                <input type="text" id ="postPid" name = "pid" class="form-control" />
            </div>
            <div class="form-group">
                <label for="owner" class="col-form-label">Owner:</label>
                <input type="text" id ="postTitle" name = "owner" class="form-control" />
            </div>

            <div class="form-group">
                <label for="message-text" class="col-form-label">Contents:</label>
                <textarea rows="4" name="message-text" id ="message-text" class="form-control"></textarea>
            </div>
        </fieldset>

        <div class="form-label-group d-flex mt-2">
            <button class="btn btn-primary col-2 ml-auto mb-2 text-light" type="submit" name="submit">Post</button>
        </div>
    </form>
</div>

<div class="container d-flex flex-column mt-4" id="injRes">
    <?php 
        // $dbServername = "127.0.0.1";
        // $dbUsername = "root";
        // $dbPassword = "Your Password";
        // $dbName = "test";
        // $conn = $mysqli;
        
        // if (!$conn) {
        //     echo "Failed to connect to MySQL: " . mysqli_connect_error();
        //     header("Location: ../index.php?login=dn_access_error");
        // }

        // if (isset($_POST['owner']) || isset($_POST['pid'])){
        //     $owner = $_POST['owner'];
        //     $pid = $_POST['pid'];
        
        //     $sql = "SELECT * FROM posttest WHERE postID = '$pid'";                            
        //     $result = mysqli_query($conn, $sql);
        //     echo "Error updating record: \n" . $conn->error . "<br>";
        //     if ($result->num_rows > 0) {
        //         // output data of each row
        //         while($row = $result->fetch_assoc()) {
        //           echo "id: " . $row["postID"]. " - add: " . $row["address"]. " - text: " . $row["contents"]. "<br>";
        //         }
        //     } 
        // }
        // mysqli_close($conn);
    ?>
</div>