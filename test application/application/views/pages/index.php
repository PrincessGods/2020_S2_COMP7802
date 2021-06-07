    <div id="main" class="container d-flex mt-4">
        <section id="left" class="w-75">
        <?php echo form_open("", array('class' => 'm-auto w-100', 'id' => 'searchForm'), ""); ?>
                <fieldset class="form-group m-auto">
                    <div class="form-group d-flex">
                        <input class="form-control form-control-lg search_bar" id="search" name="search" placeholder="Search this site" required="" type="text" value="">
                        <input class="btn btn-secondary search_btn" id="submit" name="submit" type="submit" value="Search">
                    </div>
                </fieldset>
            </form>  
            
            <!--
            <div id="post" class="content-section">
                <form class="px-4 py-2 border rounded" id="postForm" method="POST" action="includes/post.inc.php">
                    <legend class="border-bottom mb-2 mt-2"><h4 class="text-dark">New Post</h4></legend>
                    
                    <fieldset class="form-group">
                        <div class="form-group">
                            <label for="type" class="col-form-label">Type:</label>
                            <div class="d-flex mt-1">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="type" id="type1" value="find" checked>
                                    <label class="form-check-label" for="type">
                                        Job Finding
                                    </label>
                                </div>
                                <div class="form-check ml-5">
                                    <input class="form-check-input" type="radio" name="type" id="type2" value="employ">
                                    <label class="form-check-label" for="type">
                                        Employment
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="form-group">
                            <label for="title" class="col-form-label">Title:</label>
                            <input type="text" id ="postTitle" name = "title" class="form-control" />
                        </div>

                        <div class="form-group">
                            <label for="message-text" class="col-form-label">Contents:</label>
                            <textarea rows="3" name="message-text" id ="message-text" class="form-control"></textarea>
                        </div>
                    </fieldset>

                    <div class="form-label-group d-flex mt-2">
                        <button class="btn btn-dark ml-auto mb-2 text-light" type="submit" name="submit">Post</button>
                    </div>
                </form>
            </div>
            -->

            <div class="content-section mb-5">
                <?php
                    $rows = $posts;
                    if(sizeof($rows) < 1){
                        echo "<h1>No Post Existed!</h1>";

                    } else {
                        if(sizeof($rows) > 10) {
                            $displayRows = 10;
                        } else{
                            $displayRows = sizeof($rows);
                        }

                        for($i=0; $i < $displayRows; $i++){
                            $date = new DateTime($rows[$i]["date"]);
                            echo '
                                <div class="d-flex border rounded mt-4 px-3 py-3">
                                    <div class="post_left"></div>

                                    <div class="post_right">
                                        <div class="border-bottom pb-1 mb-3 d-flex">
                                            <a href="#">' . $rows[$i]["Owner"] . '</a>
                                            <p class="mb-0 ml-3">' . date_format($date, 'Y-m-d') . '</p>
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

        <section id="right" class="ml-4 w-25">
            <div class="border rounded px-3 py-2 w-100">
                <legend class="border-bottom mb-3"><h4 class="text-dark">Actions</h4></legend>
        
                <ul class="nav flex-column nav-pills border rounded mb-3" id="side_nav">
                    <li class="nav-item border-bottom m-0">
                        <a class="nav-link rounded-0 active" href="#">All Post</a>
                    </li>
                    <li class="nav-item border-bottom m-0">
                        <a class="nav-link rounded-0" href="#">Jobs Post</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link rounded-0" href="#">Employment Post</a>
                    </li>
                </ul>

                <button class="btn btn-secondary my-2" id="addNew" href="#">Add New Post</button>
            </div>
        </section>
    </div>

    <div class="modal fade" id="postModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content mt-5">
                <div class="modal-body">
                    <?php 
                        $attr = array('class'=>'px-2 col-12', 'id'=>"postForm");
                        echo form_open("includes/post_inc", $attr); 
                    ?>
                        <legend class="border-bottom mb-2 mt-2 d-flex">
                            <h4 class="text-dark">New Post
                                <button type="button" class="close" data-dismiss="modal" aria-label="Close"> 
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </h4>
                        </legend>
                        <fieldset class="form-group">
                            <div class="form-group">
                                <label for="type" class="col-form-label">Type:</label>
                                <div class="d-flex mt-1">
                                    <div class="form-check">
                                        <input class="form-check-input" type="radio" name="type" id="type1" value="find" checked>
                                        <label class="form-check-label" for="type">
                                            Job Finding
                                        </label>
                                    </div>
                                    <div class="form-check ml-5">
                                        <input class="form-check-input" type="radio" name="type" id="type2" value="employ">
                                        <label class="form-check-label" for="type">
                                            Employment
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <label for="pid" class="col-form-label">PID:</label>
                                <input type="text" id ="postPid" name = "pid" class="form-control" />
                            </div>
                            <div class="form-group">
                                <label for="title" class="col-form-label">Title:</label>
                                <input type="text" id ="postTitle" name = "title" class="form-control" />
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
            </div>
        </div>
    </div>