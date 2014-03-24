from flask import Flask, request, jsonify, Blueprint
from app.db import db
from app.api.user import id_by_email, user_details
from app.utils.common_utils import *




mod=Blueprint('thread',__name__, url_prefix='/thread')


@mod.route("/close/",methods=["POST"])
def close():
    json = request.json
    resp = {u'code': 0, u'response': json}
    return jsonify(resp)


def count_posts(thread):
    thr = db.query("SELECT COUNT(*) as cnt from posts WHERE thread_id=%s AND spam=0 AND deleted=0 AND approved=1", (thread))
    return thr[0]['cnt']



def thread_details(thread,related=None):
    thr = db.query("SELECT * from threads  INNER JOIN users ON threads.user_id = users.id WHERE tid=%s", (thread))
    resp = {}
    if thr.__len__() !=0:
        resp['date'] = thr[0]['date']
        resp['title'] = thr[0]['title']
        resp['message'] = thr[0]['message']
        resp['user'] = thr[0]['email']
        resp['dislikes'] = thr[0]['dislikes']
        resp['likes'] = thr[0]['likes']
        resp['points'] = thr[0]['points']
        resp['forum'] = sname_by_id(thr[0]['forum_id'])
        resp['slug'] = thr[0]['slug']
        resp['id'] = thr[0]['tid']
        resp['isClosed'] = bool(thr[0]['closed'])
        resp['isDeleted'] = bool(thr[0]['deleted'])
        resp['posts'] = count_posts(thr[0]['tid'])
        if related is not None: # place for optimization
            if 'user' in related:
                resp['user'] = user_details(thr[0]['email'],'email')
            if 'forum' in related:
                resp['forum'] = forum_details(resp['forum'])
    return resp



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
    json = request.json
    check_required(json, ['thread'])
    if 'related' in json:
        thr = thread_details(json['thread'],json['related'])
    else:
        thr = thread_details(json['thread'])

    return send_resp(thr,"No such thread found")


@mod.route("/list/",methods=["GET"])
def list():
    pass

@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass


@mod.route("/open/",methods=["POST"])
def open():
    json = request.json
 # thread_id = json["thread"]
    resp = {u'code': 0, u'response': json}
    return jsonify(resp)

@mod.route("/remove/",methods=["POST"])
def remove():
    json = request.json
    thread_id = json["thread"]
    resp = {u'code': 0, u'response': json}
    return jsonify(resp)

@mod.route("/restore/",methods=["POST"])
def restore():
    json = request.json
    thread_id = json["thread"]
    resp = {u'code': 0, u'response': json}
    return jsonify(resp)

@mod.route("/subscribe/",methods=["POST"])
def subscribe():
    pass

@mod.route("/unsubscribe/",methods=["POST"])
def unsubscribe():
    pass

@mod.route("/update/",methods=["POST"])
def update():
    pass

@mod.route("/vote/",methods=["POST"])
def vote():
    pass

