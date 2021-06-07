<?php

    class Includes extends CI_Controller{
        public function include($page){
            if(!file_exists(APPPATH.'views/includes/'.$page.'.php')){
                show_404();
            }

            $this->load->model('sql_model');

            $data['mysqli'] = $this -> sql_model -> get_mysqli();

            $this -> load -> view('includes/' .$page, $data);
        }
    }