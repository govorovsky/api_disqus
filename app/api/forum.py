from flask import Blueprint

from app.utils.common_utils import *


mod = Blueprint('forum', __name__, url_prefix=prefix + '/forum')


@mod.route("/create/", methods=["POST"])
def create():
    json = request.json
    check_required(json, ['name', 'short_name', 'user'])
    if is_exist('forum', json['short_name']):
        return send_resp({}, 'Such forum already exists')
    uid = id_by_email(json['user'])
    if uid < 0:
        return send_resp(json)
    db.insert("INSERT INTO forums (fname,shortname,founder_id) values (%s,%s,%s)",
              (json['name'], json['short_name'], uid))
    #fid = db.query("SELECT LAST_INSERT_ID() as id")
    fid = db.query("SELECT fid from forumds where shortname=%s", json['short_name'])
    json['id'] = fid[0]['fid']
    return send_resp(json)


@mod.route("/details/", methods=["GET"])
def details():
    json = getJson(request)
    check_required(json, ['forum'])
    det = forum_details(json['forum'], 'shortname')
    if det.__len__() != 0:
        if 'related' in json:
            if 'user' in json['related']:
                det['user'] = user_details(det['user'], 'email')
    return send_resp(det, "No such forum found")


@mod.route("/listPosts/", methods=["GET"])
def listPosts():
    json = getJson(request)
    check_required(json, ['forum'])
    return send_resp(listing(json, 'post'))


@mod.route("/listThreads/", methods=["GET"])
def listThreads():
    json = getJson(request)
    check_required(json, ['forum'])
    return send_resp(listing(json, 'thread'))  # no error if no threads found


@mod.route("/listUsers/", methods=["GET"])
def listUsers():
    json = getJson(request)
    check_required(json, ['forum'])
    return send_resp(listing(json, 'user'))

