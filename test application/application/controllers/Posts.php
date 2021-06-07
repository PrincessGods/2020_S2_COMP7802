<?php
    class Posts extends CI_Controller{
        public function index(){
            $data['posts'] = $this -> post_model -> get_posts();

            $this -> load -> view('templates/header');
            $this -> load -> view('posts/index', $data);
            $this -> load -> view('templates/footer');
        }

        public function view($postID = NULL){
            $data['post'] = $this -> post_model -> get_posts($postID);
            if(empty($data['post'])){
                show_404();
            } 

            $this -> load -> view('templates/header');
            $this -> load -> view('posts/views', $data);
            $this -> load -> view('templates/footer');
        }

        public function create(){
            $this -> form_validation -> set_rules('title', 'Title', 'required');
            $this -> form_validation -> set_rules('content', 'Content', 'required');

            if($this -> form_validation -> run() === FALSE){
                $this -> load -> view('templates/header');
                $this -> load -> view('posts/create');
                $this -> load -> view('templates/footer');
            } else {
                $hash_name = bin2hex(random_bytes(16)) . $_FILES['userfile']['name'];

                $config['upload_path'] = './static/img';
                $config['file_name'] = $hash_name;
                $config['allowed_types'] = 'gif|jpg|png';
                $config['max_size'] = '2048';
                $config['max_width'] = '500';
                $config['max_height'] = '500';

                $this -> load -> library('upload', $config);

                if(!$this -> upload -> do_upload()){
                    $errors = array('error' => $this -> upload -> display_errors());
                    $post_image = $data['post']['image'];
                    echo $errors['error'];
                } else {
                    $data = array('upload_data' => $this -> upload ->data());
                    $post_image = $hash_name;

                    foreach($data['upload_data'] as $ud){
                        echo $ud . "<br>";
                    }
                }

                $this -> post_model -> create_post($post_image);
                redirect('posts');
            }
        }

        public function delete($postID){
            $this -> post_model -> delete_post($postID);
            redirect('posts');
        }

        public function edit($postID){
            $data['post'] = $this -> post_model -> get_posts($postID);

            $this -> form_validation -> set_rules('title', 'Title', 'required');
            $this -> form_validation -> set_rules('content', 'Cpntent', 'required');

            if($this -> form_validation -> run() === FALSE){
                $this -> load -> view('templates/header');
                $this -> load -> view('posts/edit', $data);
                $this -> load -> view('templates/footer');
            } else {
                $hash_name = bin2hex(random_bytes(16)) . $_FILES['userfile']['name'];

                $config['upload_path'] = './static/img';
                $config['file_name'] = $hash_name;
                $config['allowed_types'] = 'gif|jpg|png';
                $config['max_size'] = '2048';
                $config['max_width'] = '500';
                $config['max_height'] = '500';

                $this -> load -> library('upload', $config);

                if(!$this -> upload -> do_upload()){
                    $errors = array('error' => $this -> upload -> display_errors());
                    $post_image = $data['post']['image'];
                    echo $errors['error'];
                } else {
                    $data = array('upload_data' => $this -> upload ->data());
                    $post_image = $hash_name;

                    foreach($data['upload_data'] as $ud){
                        echo $ud . "<br>";
                    }
                }

                $ID_img = array('postID' => $postID, 'image' => $post_image);
                $this -> post_model -> edit_post($ID_img);
                
                redirect('posts/'.$postID);
            }
        }
    }