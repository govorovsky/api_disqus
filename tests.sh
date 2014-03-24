#!/bin/bash

function check() {

if [ "$1" == "$2" ] 
then
    echo -e "\033[37;1;42m TEST $3 passed \033[0m"
    echo
    
else
    echo -e "\033[37;1;41m TEST $3 failed \033[0m"
    echo -e "GIVEN:"
    echo -e "$1"
    echo -e "Excpected:"
    echo -e "$2"
    exit 1
fi

}

# prepare DB
mysql -u root -p'qazxsw12'  -e  "source schema.sql" 


test_create_user=`curl -X POST -H "Content-Type: application/json" -d  '{"username": "user1", "about": "hello im user1",  "email": "example@mail.ru", "name" : "User1Name"}' localhost:5000/user/create/ 2>/dev/null`

test_create_anon_user=`curl -X POST -H "Content-Type: application/json" -d  '{"isAnonymous": "True" ,"email": "example1@mail.ru", "name" : ""}' localhost:5000/user/create/ 2>/dev/null`

test_update_user=`curl -X POST -H "Content-Type: application/json" -d  '{ "user" : "example@mail.ru", "about" : "sweetnes", "name" : "WOWOWO"}'  localhost:5000/user/updateProfile/ 2>/dev/null` 

test_forum_create=`curl -X POST -H "Content-Type: application/json" -d  '{ "user" : "example@mail.ru", "name" : "first_forum", "short_name" : "fst_frm"}'  localhost:5000/forum/create/ 2>/dev/null`

test_forum_details=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "first_forum", "related":["user"]}'  localhost:5000/forum/details/ 2>/dev/null`


test_forum_details_norelated=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "first_forum", "related":[]}'  localhost:5000/forum/details/ 2>/dev/null`


read -d '' success_create_user << "EOF"
{
  "code": 0, 
  "response": {
    "about": "hello im user1", 
    "email": "example@mail.ru", 
    "id": 1, 
    "isAnonymous": false, 
    "name": "User1Name", 
    "username": "user1"
  }
}
EOF


read -d '' success_update_user << "EOF"
{
  "code": 0, 
  "response": {
    "about": "sweetnes", 
    "email": "example@mail.ru", 
    "followers": [], 
    "following": [], 
    "id": 1, 
    "isAnonymous": false, 
    "name": "WOWOWO", 
    "subscriptions": [], 
    "username": "user1"
  }
}
EOF




read -d '' success_forum_create << "EOF"
{
  "code": 0, 
  "response": {
    "id": 1, 
    "name": "first_forum", 
    "short_name": "fst_frm", 
    "user": "example@mail.ru"
  }
}
EOF



read -d '' success_forum_details_norelated << "EOF"
{
  "code": 0, 
  "response": {
    "id": 1, 
    "name": "first_forum", 
    "short_name": "fst_frm", 
    "user": "example@mail.ru"
  }
}
EOF
read -d '' success_forum_details << "EOF"
{
  "code": 0, 
  "response": {
    "id": 1, 
    "name": "first_forum", 
    "short_name": "fst_frm", 
    "user": {
      "about": "sweetnes", 
      "email": "example@mail.ru", 
      "followers": [], 
      "following": [], 
      "id": 1, 
      "isAnonymous": false, 
      "name": "WOWOWO", 
      "subscriptions": [], 
      "username": "user1"
    }
  }
}
EOF


read -d '' success_create_anon_user << "EOF"
{
  "code": 0, 
  "response": {
    "email": "example1@mail.ru", 
    "id": 2, 
    "isAnonymous": true, 
    "name": null
  }
}
EOF




check "$test_create_user" "$success_create_user" "user creation"

check "$test_create_anon_user" "$success_create_anon_user" "anon user creation"

check "$test_update_user" "$success_update_user" "user update"

check "$test_forum_create" "$success_forum_create" "forum create"

check "$test_forum_details" "$success_forum_details" "forum details"

check "$test_forum_details_norelated" "$success_forum_details_norelated" "forum details no related user"



exit 0
