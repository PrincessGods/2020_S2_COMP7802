<div class="container mt-4">
    <?php
        for($i = 0; $i < sizeof($posts); $i++){
            $count = $i + 1; 
            echo "<h3>Post" .$count. ":</h3>";
            echo "<small>Posted on: " .$posts[$i]['date']. "</small>
                    <br>
                    <p>" .word_limiter($posts[$i]['contents'], 50). "</p>";
            echo "<a class='btn btn-secondary' href='".site_url('/posts/'.$posts[$i]['postID'])."'>Read More</a> <br>";
            /*
            foreach($posts[$i] as $p){
                echo $p . "<br>";
            }
            */
            echo "<br>";
        }
        
    ?>
</div>