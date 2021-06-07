<?php
    class User_model extends CI_Model{
        public function signup(){
            if($postID === FALSE){
                $this -> db -> order_by('postID', 'ASCE');//降序：DESC
                $query = $this -> db -> get('posttest');
                return $query -> result_array();
            }
            $query = $this -> db -> get_where('posttest', array('postID' => $postID));
            return $query -> row_array();
        }

        public function login(){
            $username = $this -> input -> post('username');
            $password = $this -> input -> post('password');
            $reme = $this -> input -> post('reme');

            $query = $this -> db -> get_where('usertest', array('Username' => $username));
            $query = $query -> row_array();

            $hashedPwdCheck = password_verify($password, $query['Password']);
            if($hashedPwdCheck == FALSE){
                return "Incorrect Password";

            } elseif ($hashedPwdCheck == TRUE && $reme == FALSE){
                $userdata = array(
                    'u_id'  => $query['ID'],
                    'u_email' => $query['Email'],
                    'u_name' => $query['Username'],
                    'u_phone' => $query['Phone'],
                    'u_address' => $query['Address'],
                    'u_gender' => $query['Gender'],
                    'u_country' => $query['Country']
                );
                $this-> session -> set_userdata($userdata);
                return "Session";

            } elseif ($hashedPwdCheck == TRUE && $reme == TRUE){
                $input_name = array(
                    'name'  => 'input_name',
                    'value' => $username,
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $input_pwd = array(
                    'name'  => 'input_pwd',
                    'value' => $password,
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_id = array(
                    'name'  => 'u_id',
                    'value' => $query['ID'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_id = array(
                    'name'  => 'u_id',
                    'value' => $query['ID'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_email = array(
                    'name'  => 'u_email',
                    'value' => $query['Email'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_name = array(
                    'name'  => 'u_name',
                    'value' => $query['Username'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_phone = array(
                    'name'  => 'u_phone',
                    'value' => $query['Phone'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_address = array(
                    'name'  => 'u_address',
                    'value' => $query['Address'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_gender = array(
                    'name'  => 'u_gender',
                    'value' => $query['Gender'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                $u_country = array(
                    'name'  => 'u_country',
                    'value' => $query['Country'],
                    'expire' => 3600 * 24 * 14,
                    'path' => '/'
                );

                set_cookie($input_name);
                set_cookie($input_pwd);
                set_cookie($u_id);
                set_cookie($u_email);
                set_cookie($u_name);
                set_cookie($u_phone);
                set_cookie($u_address);
                set_cookie($u_gender);
                set_cookie($u_country);

                $userdata = array(
                    'u_id'  => $query['ID'],
                    'u_email' => $query['Email'],
                    'u_name' => $query['Username'],
                    'u_phone' => $query['Phone'],
                    'u_address' => $query['Address'],
                    'u_gender' => $query['Gender'],
                    'u_country' => $query['Country']
                );
                $this-> session -> set_userdata($userdata);

                return "Cookie";
            }
        }

        public function logout(){
            if(get_cookie('u_id') != null){
                delete_cookie("input_name", "", "/", "");
                delete_cookie("input_pwd", "", "/", "");
                delete_cookie("u_id", "", "/", "");
                delete_cookie("u_email", "", "/", "");
                delete_cookie("u_name", "", "/", "");
                delete_cookie("u_phone", "", "/", "");
                delete_cookie("u_address", "", "/", "");
                delete_cookie("u_gender", "", "/", "");
                delete_cookie("u_country", "", "/", "");
            }

            $userdata = array(
                'u_id',
                'u_email',
                'u_name',
                'u_phone',
                'u_address',
                'u_gender',
                'u_country'
            );
            $this-> session -> unset_userdata($userdata);
        }

    }