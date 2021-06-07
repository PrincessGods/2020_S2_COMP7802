<?php
    class Sql_model extends CI_Model{
        public function __construct(){
            $this -> load -> database();
        }

        public function get_mysqli(){
            $db = (array)get_instance()->db;
            $mysqli = mysqli_connect('localhost', $db['username'], $db['password'], $db['database']);
            return $mysqli;
        }
    }