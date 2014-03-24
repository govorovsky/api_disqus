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


test_create_user1=`curl -X POST -H "Content-Type: application/json" -d  '{"username": "user1", "about": "hello im user1",  "email": "example@mail.ru", "name" : "User1Name"}' localhost:5000/user/create/ 2>/dev/null`
test_create_user2=`curl -X POST -H "Content-Type: application/json" -d  '{"username": "user2", "about": "hello im user2",  "email": "example2@mail.ru", "name" : "User1Name", "isAnonymous" : "True"}' localhost:5000/user/create/ 2>/dev/null`

test_create_anon_user=`curl -X POST -H "Content-Type: application/json" -d  '{"isAnonymous": "True" ,"email": "example1@mail.ru", "name" : ""}' localhost:5000/user/create/ 2>/dev/null`

test_update_user=`curl -X POST -H "Content-Type: application/json" -d  '{ "user" : "example@mail.ru", "about" : "sweetnes", "name" : "WOWOWO"}'  localhost:5000/user/updateProfile/ 2>/dev/null` 

test_update_user404=`curl -X POST -H "Content-Type: application/json" -d  '{ "user" : "example3222@mail.ru", "about" : "sweetnes", "name" : "WOWOWO"}'  localhost:5000/user/updateProfile/ 2>/dev/null` 

test_forum_create=`curl -X POST -H "Content-Type: application/json" -d  '{ "user" : "example@mail.ru", "name" : "first_forum", "short_name" : "fst_frm"}'  localhost:5000/forum/create/ 2>/dev/null`

test_forum_details=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm", "related":["user"]}'  localhost:5000/forum/details/ 2>/dev/null`

test_forum_details_norelated=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm", "related":[]}'  localhost:5000/forum/details/ 2>/dev/null`

test_thread_create1=`curl  -X POST -H "Content-Type: application/json" -d  '{"forum": "fst_frm", "title": "Thread With Sufficiently Large Title", "isClosed": "True", "user": "example@mail.ru", "date": "2014-01-01 00:00:01", "message": "hey hey hey hey!", "slug": "Threadwithsufficientlylargetitle", "isDeleted": "True"}' localhost:5000/thread/create/ 2>/dev/null`

test_thread_create2=`curl  -X POST -H "Content-Type: application/json" -d  '{"forum": "fst_frm", "title": "Second thread here", "isClosed": "True", "user": "example2@mail.ru", "date": "2014-02-01 02:00:01", "message": "ho ho heck", "slug": "Scondthread", "isDeleted": "False"}' localhost:5000/thread/create/ 2>/dev/null`

test_thread2_details=`curl -X GET -H "Content-Type: application/json" -d  '{"thread" : "1", "related":["user", "forum"]}'  localhost:5000/thread/details/ 2>/dev/null`
test_thread2_details=`curl -X GET -H "Content-Type: application/json" -d  '{"thread" : "2", "related":["user", "forum"]}'  localhost:5000/thread/details/ 2>/dev/null`


test_forum_listthreads1=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm",  "since":"2013-02-01 00:00:00","related":["user", "forum"], "limit":"1"}'  localhost:5000/forum/listThreads/ 2>/dev/null`

test_forum_listthreads2=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm",  "since":"2014-02-01 02:00:01","related":["user", "forum"], "limit":"2"}'  localhost:5000/forum/listThreads/ 2>/dev/null`

test_forum_listthreads3=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm",  "since":"2013-02-01 02:00:01","related":["user", "forum"], "limit":"5"}'  localhost:5000/forum/listThreads/ 2>/dev/null`

test_forum_listthreads4=`curl -X GET -H "Content-Type: application/json" -d  '{"forum" : "fst_frm",  "since":"2013-02-01 02:00:01","related":["user", "forum"], "limit":"5", "order" : "asc"}'  localhost:5000/forum/listThreads/ 2>/dev/null`

read -d '' success_create_user1 << "EOF"
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

read -d '' success_create_user2 << "EOF"
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


read -d '' success_update_user404 << "EOF"
{
  "code": 1, 
  "message": "No such user found"
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
    "id": 3, 
    "isAnonymous": true, 
    "name": null
  }
}
EOF


read -d '' success_thread_create1 << "EOF"
{
  "code": 0, 
  "response": {
    "date": "2014-01-01 00:00:01", 
    "forum": "fst_frm", 
    "id": 1, 
    "isClosed": true, 
    "isDeleted": true, 
    "message": "hey hey hey hey!", 
    "slug": "Threadwithsufficientlylargetitle", 
    "title": "Thread With Sufficiently Large Title", 
    "user": "example@mail.ru"
  }
}
EOF

read -d '' success_thread_create2 << "EOF"
{
  "code": 0, 
  "response": {
    "date": "2014-02-01 02:00:01", 
    "forum": "fst_frm", 
    "id": 2, 
    "isClosed": true, 
    "isDeleted": false, 
    "message": "ho ho heck", 
    "slug": "Scondthread", 
    "title": "Second thread here", 
    "user": "example2@mail.ru"
  }
}
EOF

read -d '' success_thread_create3 << "EOF"
{
  "code": 0, 
  "response": {
    "date": "2014-01-01 00:00:01", 
    "forum": "fst_frm", 
    "id": 1, 
    "isClosed": true, 
    "isDeleted": true, 
    "message": "hey hey hey hey!", 
    "slug": "Threadwithsufficientlylargetitle", 
    "title": "Thread With Sufficiently Large Title", 
    "user": "example@mail.ru"
  }
}
EOF



read -d '' success_thread2_details << "EOF"
{
  "code": 0, 
  "response": {
    "date": "Wed, 01 Jan 2014 00:00:01 GMT", 
    "dislikes": 0, 
    "forum": {
      "id": 1, 
      "name": "first_forum", 
      "short_name": "fst_frm", 
      "user": "example@mail.ru"
    }, 
    "id": 1, 
    "isClosed": true, 
    "isDeleted": true, 
    "likes": 0, 
    "message": "hey hey hey hey!", 
    "points": 0, 
    "posts": 0, 
    "slug": "Threadwithsufficientlylargetitle", 
    "title": "Thread With Sufficiently Large Title", 
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


read -d '' success_thread2_details << "EOF"
{
  "code": 0, 
  "response": {
    "date": "Sat, 01 Feb 2014 02:00:01 GMT", 
    "dislikes": 0, 
    "forum": {
      "id": 1, 
      "name": "first_forum", 
      "short_name": "fst_frm", 
      "user": "example@mail.ru"
    }, 
    "id": 2, 
    "isClosed": true, 
    "isDeleted": false, 
    "likes": 0, 
    "message": "ho ho heck", 
    "points": 0, 
    "posts": 0, 
    "slug": "Scondthread", 
    "title": "Second thread here", 
    "user": {
      "email": "example2@mail.ru", 
      "followers": [], 
      "following": [], 
      "id": 2, 
      "isAnonymous": true, 
      "name": null, 
      "subscriptions": []
    }
  }
}
EOF



read -d '' success_forum_listthreads1 << "EOF"
{
  "code": 0, 
  "response": [
    {
      "date": "Sat, 01 Feb 2014 02:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 2, 
      "isClosed": true, 
      "isDeleted": false, 
      "likes": 0, 
      "message": "ho ho heck", 
      "points": 0, 
      "posts": 0, 
      "slug": "Scondthread", 
      "title": "Second thread here", 
      "user": {
        "email": "example2@mail.ru", 
        "followers": [], 
        "following": [], 
        "id": 2, 
        "isAnonymous": true, 
        "name": null, 
        "subscriptions": []
      }
    }
  ]
}
EOF


read -d '' success_forum_listthreads2 << "EOF"
{
  "code": 0, 
  "response": [
    {
      "date": "Sat, 01 Feb 2014 02:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 2, 
      "isClosed": true, 
      "isDeleted": false, 
      "likes": 0, 
      "message": "ho ho heck", 
      "points": 0, 
      "posts": 0, 
      "slug": "Scondthread", 
      "title": "Second thread here", 
      "user": {
        "email": "example2@mail.ru", 
        "followers": [], 
        "following": [], 
        "id": 2, 
        "isAnonymous": true, 
        "name": null, 
        "subscriptions": []
      }
    }
  ]
}
EOF



read -d '' success_forum_listthreads3 << "EOF"
{
  "code": 0, 
  "response": [
    {
      "date": "Sat, 01 Feb 2014 02:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 2, 
      "isClosed": true, 
      "isDeleted": false, 
      "likes": 0, 
      "message": "ho ho heck", 
      "points": 0, 
      "posts": 0, 
      "slug": "Scondthread", 
      "title": "Second thread here", 
      "user": {
        "email": "example2@mail.ru", 
        "followers": [], 
        "following": [], 
        "id": 2, 
        "isAnonymous": true, 
        "name": null, 
        "subscriptions": []
      }
    }, 
    {
      "date": "Wed, 01 Jan 2014 00:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 1, 
      "isClosed": true, 
      "isDeleted": true, 
      "likes": 0, 
      "message": "hey hey hey hey!", 
      "points": 0, 
      "posts": 0, 
      "slug": "Threadwithsufficientlylargetitle", 
      "title": "Thread With Sufficiently Large Title", 
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
  ]
}
EOF

read -d '' success_forum_listthreads4 << "EOF"
{
  "code": 0, 
  "response": [
    {
      "date": "Wed, 01 Jan 2014 00:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 1, 
      "isClosed": true, 
      "isDeleted": true, 
      "likes": 0, 
      "message": "hey hey hey hey!", 
      "points": 0, 
      "posts": 0, 
      "slug": "Threadwithsufficientlylargetitle", 
      "title": "Thread With Sufficiently Large Title", 
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
    }, 
    {
      "date": "Sat, 01 Feb 2014 02:00:01 GMT", 
      "dislikes": 0, 
      "forum": {
        "id": 1, 
        "name": "first_forum", 
        "short_name": "fst_frm", 
        "user": "example@mail.ru"
      }, 
      "id": 2, 
      "isClosed": true, 
      "isDeleted": false, 
      "likes": 0, 
      "message": "ho ho heck", 
      "points": 0, 
      "posts": 0, 
      "slug": "Scondthread", 
      "title": "Second thread here", 
      "user": {
        "email": "example2@mail.ru", 
        "followers": [], 
        "following": [], 
        "id": 2, 
        "isAnonymous": true, 
        "name": null, 
        "subscriptions": []
      }
    }
  ]
}
EOF




check "$test_create_user1" "$success_create_user1" "user creation"

check "$test_create_anon_user" "$success_create_anon_user" "anon user creation"

check "$test_update_user" "$success_update_user" "user update"

check "$test_update_user404" "$success_update_user404" "user 404 update"

check "$test_forum_create" "$success_forum_create" "forum create"

check "$test_forum_details" "$success_forum_details" "forum details"

check "$test_forum_details_norelated" "$success_forum_details_norelated" "forum details no related user"

check "$test_thread_create1" "$success_thread_create1" "thread create 1"
check "$test_thread_create2" "$success_thread_create2" "thread create 2"
#check "$test_thread_create3" "$success_thread_create1" "thread create 3"

check "$test_thread1_details" "$success_thread1_details" "thread 1 details "
check "$test_thread2_details" "$success_thread2_details" "thread 2 details "


check "$test_forum_listthreads1" "$success_forum_listthreads1" "forum listthreads limit 1 order desc  "
check "$test_forum_listthreads2" "$success_forum_listthreads2" "forum listthreads limit 2 order desc   "
check "$test_forum_listthreads3" "$success_forum_listthreads3" "forum listthreads limit 5 order desc   "
check "$test_forum_listthreads4" "$success_forum_listthreads4" "forum listthreads limit 5 order asc  "





exit 0
