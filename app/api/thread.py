from flask import Flask, request, jsonify, Blueprint
from app.db import db
from app.api.user import id_by_email, user_details
from app.utils.common_utils import *




mod=Blueprint('thread',__name__, url_prefix='/thread')

def Moderate(json,action):
    json = getJson(request)
    thread_id = json['thread']
    act = 1 if (action == 'close' or action == 'remove' ) else 0
    target = 'closed' if ( action == 'close' or action == 'open') else 'deleted'
    if(isExist(json['thread'])):
        db.insert("UPDATE threads SET %s=%s " % (target,act) +" where tid=%s", thread_id)
        return send_resp(json)
    else:
        return send_resp({}, "No such thread found")


@mod.route("/close/",methods=["POST"])
def close():
    return OpenClose(getJson(request),'close')

def count_posts(thread):
    thr = db.query("SELECT COUNT(*) as cnt from posts WHERE thread_id=%s AND spam=0 AND deleted=0 AND approved=1", (thread))
    return thr[0]['cnt']



def thread_details(thread,related=None):
    thr = db.query("SELECT * from threads WHERE tid=%s", (thread))
    resp = {}
    if thr.__len__() !=0:
        if related is not None: # place for optimization
            if 'user' in related:
                resp['user'] = user_details(thr[0]['user_id'],'id')
            if 'forum' in related:
                resp['forum'] = forum_details(sname_by_id(thr[0]['forum_id']))
        if 'user' not in resp:
            resp['user'] = email_by_id(thr[0]['user_id'])
        if 'forum' not in resp:
            resp['forum'] = sname_by_id(thr[0]['forum_id'])
        resp['date'] = thr[0]['date']
        resp['title'] = thr[0]['title']
        resp['message'] = thr[0]['message']
        resp['dislikes'] = thr[0]['dislikes']
        resp['likes'] = thr[0]['likes']
        resp['points'] = thr[0]['likes'] - thr[0]['dislikes']
        resp['slug'] = thr[0]['slug']
        resp['id'] = thr[0]['tid']
        resp['isClosed'] = bool(thr[0]['closed'])
        resp['isDeleted'] = bool(thr[0]['deleted'])
        resp['posts'] = count_posts(thr[0]['tid'])
    return resp

def isExist(thread_id):
    thr = db.query("SELECT * from threads WHERE tid=%s", (thread_id))
    return (1 if (thr.__len__() > 0 ) else 0)

@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    check_required(json, ['title', 'slug', 'forum', 'isClosed', 'user','date','message'])
    if "isDeleted" in json:
        deleted = getBool(json['isDeleted'])
        json['isDeleted'] = deleted
    else:
        deleted = 0
        json['isDeleted'] = False

    closed = getBool(json['isClosed'])
    json['isClosed'] = closed

    uid = id_by_email(json["user"])
    fid = id_by_sname(json["forum"])

    db.insert("""INSERT INTO threads (title, slug, forum_id, closed, deleted, user_id, date, message) 
                 values (%s,%s,%s,%s,%s,%s,%s,%s) """, (json["title"], json["slug"], fid, closed, deleted, uid, json['date'], json['message']))
 
    tid = db.query("SELECT LAST_INSERT_ID() as id")
    json['id'] = tid[0]['id']
  
    return send_resp(json)



@mod.route("/details/",methods=["GET"])
def details():
    json = getJson(request)
    check_required(json, ['thread'])
    if 'related' in json:
        thr = thread_details(json['thread'],json['related'])
    else:
        thr = thread_details(json['thread'])
    return send_resp(thr,"No such thread found")


@mod.route("/list/",methods=["GET"])
def list():
    json = getJson(request)
    return send_resp(listThr(json))

@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass




@mod.route("/open/",methods=["POST"])
def open():
    return Moderate(getJson(request),'open')

@mod.route("/remove/",methods=["POST"])
def remove():
    return Moderate(getJson(request),'remove')

@mod.route("/restore/",methods=["POST"])
def restore():
    return Moderate(getJson(request),'restore')

def subscribe_action(json,type):
    check_required(json,['user','thread'])
    uemail = id_by_email(json['user'])
    act = 1 if (type == 'sub') else 0
    query = "INSERT INTO subscriptions(users_id, threads_id,active) VALUES (%%s,%%s,%%s) ON DUPLICATE KEY UPDATE active=%s" % (act)
    db.insert(query,(uemail, json['thread'],act))

@mod.route("/subscribe/",methods=["POST"])
def subscribe():
    json = getJson(request)
    subscribe_action(json,'sub')
    return send_resp(json)

@mod.route("/unsubscribe/",methods=["POST"])
def unsubscribe():
    json = getJson(request)
    subscribe_action(json,'unsub')
    return send_resp(json)

@mod.route("/update/",methods=["POST"])
def update():
    json = request.json
    check_required(json, ['thread', 'slug', 'message'])
    db.insert("UPDATE threads SET slug=%s, message=%s where tid=%s", (json['slug'], json['message'] , json['thread']))
    return send_resp(thread_details(json['thread']),"No such thread found")

@mod.route("/vote/",methods=["POST"])
def vote():
    json = getJson(request)
    check_required(json,['vote','thread'])
    vt = int(json['vote'])
    type = 'likes' if (vt > 0) else 'dislikes'
    query = "UPDATE threads SET %s = %s + 1 where tid=%%s" % (type,type)
    db.insert(query, json['thread'])
    return send_resp(thread_details(json['thread']),"No such thread found")


