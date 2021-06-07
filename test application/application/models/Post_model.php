<?php
    class Post_model extends CI_Model{
        public function __construct(){
            $this -> load -> database();
        }

        public function get_posts($postID = FALSE){
            if($postID === FALSE){
                $this -> db -> order_by('postID', 'ASCE');//降序：DESC
                $query = $this -> db -> get('posttest');
                return $query -> result_array();
            }
            $query = $this -> db -> get_where('posttest', array('postID' => $postID));
            return $query -> row_array();
        }

        public function create_post($image){
            $slug = url_title($this -> input -> post('title'));

            $type = $this -> input -> post('type');
            if($type == "Choose..."){
                $type = "find";
            }

            $data = array(
                'title' => $this -> input -> post('title'),
                'address' => $this -> input -> post('address'),
                'contents' => $this -> input -> post('content'),
                'type' => $type,
                'owner' => $this-> session ->userdata('u_name'),
                'image' => $image
            );

            $this -> db -> insert('posttest', $data);
        }

        public function delete_post($postID){
            $this -> db -> where('postID', $postID);
            $this -> db -> delete('posttest');
        }

        public function edit_post($ID_img){
            $data = array(
                'title' => $this -> input -> post('title'),
                'address' => $this -> input -> post('address'),
                'contents' => $this -> input -> post('content'),
                'type' => $this -> input -> post('type'),
                'owner' => $this-> session ->userdata('u_name'),
                'image' => $ID_img['image']
            );
                $this -> db -> where('postID', $ID_img['postID']);
                $this -> db -> update('posttest', $data);
        }

        public function search_post($keyword){
            if($keyword != ''){
                $this -> db -> select('*');
                $this -> db -> from('posttest');
                $this -> db -> like('contents', $keyword);
                $this -> db -> or_like('Owner', $keyword);
                $this -> db -> or_like('title', $keyword);
                $this -> db -> order_by('postID', 'DESC');
                return $this -> db -> get() -> result_array();
            }

            return "error";
        }

    }