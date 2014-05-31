from flask import Blueprint

from app.utils.common_utils import *


mod = Blueprint('thread', __name__, url_prefix=prefix + '/thread')


@mod.route("/close/", methods=["POST"])
def close():
    return moderate(getJson(request), 'thread', 'close')


@mod.route("/create/", methods=["POST"])
def create():
    json = request.json
    check_required(json, ['title', 'slug', 'forum', 'isClosed', 'user', 'date', 'message'])
    if "isDeleted" in json:
        deleted = json['isDeleted']
        json['isDeleted'] = deleted
    else:
        deleted = 0
        json['isDeleted'] = False

    closed = json['isClosed']
    json['isClosed'] = closed

    uid = id_by_email(json["user"])
    fid = id_by_sname(json["forum"])

    db.insert("""INSERT INTO threads (title, slug, forum_id, closed, deleted, user_id, date, message) 
                 values (%s,%s,%s,%s,%s,%s,%s,%s) """,
              (json["title"], json["slug"], fid, closed, deleted, uid, json['date'], json['message']))

    tid = db.query("SELECT LAST_INSERT_ID() as id")
    json['id'] = tid[0]['id']

    return send_resp(json)


@mod.route("/details/", methods=["GET"])
def details():
    json = getJson(request)
    check_required(json, ['thread'])
    if 'related' in json:
        thr = thread_details(json['thread'], json['related'])
    else:
        thr = thread_details(json['thread'])
    return send_resp(thr, "No such thread found")


@mod.route("/list/", methods=["GET"])
def list():
    json = getJson(request)
    return send_resp(listing(json, 'thread'),"No entries")


@mod.route("/listPosts/", methods=["GET"])
def listPosts():
    json = getJson(request)
    check_required(json, ['thread'])
    return send_resp(listing(json, 'post'))


@mod.route("/open/", methods=["POST"])
def open():
    return moderate(getJson(request), 'thread', 'open')


@mod.route("/remove/", methods=["POST"])
def remove():
    return moderate(getJson(request), 'thread', 'remove')


@mod.route("/restore/", methods=["POST"])
def restore():
    return moderate(getJson(request), 'thread', 'restore')


def subscribe_action(json, type):
    check_required(json, ['user', 'thread'])
    uemail = id_by_email(json['user'])
    act = 1 if (type == 'sub') else 0
    query = "INSERT INTO subscriptions(users_id, threads_id,active) VALUES (%%s,%%s,%%s) ON DUPLICATE KEY UPDATE active=%s" % (
        act)
    db.insert(query, (uemail, json['thread'], act))


@mod.route("/subscribe/", methods=["POST"])
def subscribe():
    json = getJson(request)
    subscribe_action(json, 'sub')
    return send_resp(json)


@mod.route("/unsubscribe/", methods=["POST"])
def unsubscribe():
    json = getJson(request)
    subscribe_action(json, 'unsub')
    return send_resp(json)


@mod.route("/update/", methods=["POST"])
def update():
    json = request.json
    check_required(json, ['thread', 'slug', 'message'])
    db.insert("UPDATE threads SET slug=%s, message=%s, date=date where tid=%s",
              (json['slug'], json['message'], json['thread']))
    return send_resp(thread_details(json['thread']), "No such thread found")


@mod.route("/vote/", methods=["POST"])
def vote():
    return (voter(getJson(request), 'thread'))

