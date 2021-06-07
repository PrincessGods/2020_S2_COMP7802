<?php
    class Pages extends CI_Controller{
        public function view($page = 'index'){
            if(!file_exists(APPPATH.'views/pages/'.$page.'.php')){
                show_404();
            }
            
            $this->load->model('sql_model');

            $data['title'] = ucfirst($page);
            $data['posts'] = $this -> post_model -> get_posts();
            $data['mysqli'] = $this -> sql_model -> get_mysqli();
            
            $this -> load -> view('templates/header');
            $this -> load -> view('pages/'.$page, $data);
            $this -> load -> view('templates/footer');
        }

        public function search(){
            $result = "Data Not Found";
            
            if($keyword = $this -> input -> get('owner')){
                $result = $this -> post_model -> search_post($keyword);
            }
            // echo json_encode($this -> input -> post('search'));
            echo json_encode($result);
        }

        public function login(){
            if($this->session->userdata('u_id') != null){
                redirect(base_url());
            }

            $this -> form_validation -> set_rules('username', 'User name', 'required');
            $this -> form_validation -> set_rules('password', 'Password', 'required');

            if($this -> form_validation -> run() === FALSE){
                $this -> load -> view('templates/header');
                $this -> load -> view('pages/login');
                $this -> load -> view('templates/footer');
            } else {
                echo $this -> user_model -> login();
                redirect(base_url());
            }
        }

        public function logout(){
            if($this->session->userdata('u_id') == null){
                redirect(base_url());
            }

            $this -> user_model -> logout();
            redirect(base_url());
        }
    }