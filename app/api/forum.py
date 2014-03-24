from flask import Flask, request, jsonify, Blueprint
from app.db import db
from app.api.user import id_by_email, user_details

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


def forum_details(forum):
    details = {}
    res = db.query("SELECT * from forums f INNER JOIN users on id=founder_id where fname=%s",forum)
    details['id'] = res[0]['fid']
    details['short_name'] = res[0]['shortname']
    details['name'] = res[0]['fname']
    details['user'] = res[0]['email']
    return details



@mod.route("/details/",methods=["GET"])
def details():
    json = request.json
    check_required(json, ['forum'])
    det  = forum_details(json['forum'])
    if 'related' in json:
        if 'user' in json['related']:
            det['user'] = user_details(det['user'],'email')
        
    return send_resp(det)


@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass

@mod.route("/listThreads/",methods=["GET"])
def listThreads():
    pass

@mod.route("/listUsers/",methods=["GET"])
def listUsers():
    pass

