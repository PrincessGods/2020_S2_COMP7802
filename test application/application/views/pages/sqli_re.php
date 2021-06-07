<section class="container d-flex flex-column mt-4">    
    <div class="content-section mb-5">
        <?php
            if(isset($_SESSION['row_sqli']))
            $rows = $_SESSION['row_sqli'];
            if(sizeof($rows) < 1){
                echo "<h1>No Post Existed!</h1>";

            } else {
                if(sizeof($rows) > 10) {
                    $displayRows = 10;
                } else{
                    $displayRows = sizeof($rows);
                }

                for($i=0; $i < $displayRows; $i++){
                    $date = $rows[$i]["date"];
                    echo '
                        <div class="d-flex border rounded mt-4 px-3 py-3">
                            <div class="post_left"></div>

                            <div class="post_right">
                                <div class="border-bottom pb-1 mb-3 d-flex">
                                    <a href="#">' . $rows[$i]["Owner"] . '</a>
                                    <p class="mb-0 ml-3">' . $date . '</p>
                                </div>
                                <h3>' . $rows[$i]["title"] . '</h3>
                                <p class="mb-0 post-text">' . $rows[$i]["contents"] . '</p>
                            </div>
                        </div>
                    ';
                }
            }
        ?>
    </div>
</section>