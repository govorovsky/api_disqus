from flask import Flask, request, jsonify, Blueprint
from app.db import db
from app.api.user import id_by_email, user_details
from app.api.thread import thread_details

from app.utils.common_utils import *


mod=Blueprint('forum',__name__, url_prefix='/forum')





@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    check_required(json, ['name', 'short_name', 'user'])
    uid = id_by_email(json['user'])
    db.insert("INSERT INTO forums (fname,shortname,founder_id) values (%s,%s,%s)", (json['name'], json['short_name'], uid))
    fid = db.query("SELECT LAST_INSERT_ID() as id")
    json['id'] = fid[0]['id']
    return send_resp(json)


@mod.route("/details/",methods=["GET"])
def details():
    json = request.json
    check_required(json, ['forum'])
    det  = forum_details(json['forum'])
    if det.__len__() !=0:
        if 'related' in json:
            if 'user' in json['related']:
                det['user'] = user_details(det['user'],'email') 
    return send_resp(det,"No such forum found")


@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass

@mod.route("/listThreads/",methods=["GET"])
def listThreads():
    json = request.json
    check_required(json, ['forum'])
    if 'related' in json:
        related = json['related']
    else:
        related = []
    fid = id_by_sname(json['forum'])
    query = "SELECT tid FROM threads where forum_id=%s"
    params = ()
    params += (fid,)
    if 'since' in json:
        query += " AND date >= %s"
        params += (json['since'],)
    if 'order' in json:
        order = json['order']
    else:
        order = 'desc'
    query += " ORDER BY date %s" % (order)
    if 'limit' in json:
        query+=" LIMIT %s" % (json['limit'])
    print query
    lst = db.query(query, (params))
    result = []
    if lst.__len__() > 0:
        for thread in lst: # for every id get thread info
            thr = thread_details(thread['tid'],related)
            result.append(thr)
    return send_resp(result) # no error if no threads found

@mod.route("/listUsers/",methods=["GET"])
def listUsers():
    pass

