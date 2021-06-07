<section class="container mt-4">
    
    <?php     
        foreach($post as $p){
            echo $p . "<br>";
        }
        echo '<br> <img src="' . base_url() . 'static/img/' . $post['image'] . '" alt="error"'; 
        echo "<br> <br> <br>";
    ?>

    <?php echo form_open("posts/delete/" . $post['postID'], array('class' => 'mb-5 d-flex'), ""); ?>
        <a class="btn btn-secondary mr-1" href="<?php echo base_url() ?>posts/edit/<?php echo $post['postID']; ?>">Edit</a>
        <input type="submit" value="Delete" class="btn btn-danger">
    </form>
    
</section>