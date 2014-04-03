from flask import Blueprint

from app.utils.common_utils import *


mod = Blueprint('post', __name__, url_prefix='/gov/post')


@mod.route("/create/", methods=["POST"])
def create():
    json = getJson(request)
    check_required(json, ['date', 'thread', 'message', 'user', 'forum'])
    uid = id_by_email(json['user'])
    fid = id_by_sname(json['forum'])
    if 'parent' in json:
        parent = json['parent']
    else:
        parent = None
        json['parent'] = None
    if 'isApproved' in json:
        approved = json['isApproved']
    else:
        approved = 0
        json['isApproved'] = 0
    if 'isHighlighted' in json:
        highlighted = json['isHighlighted']
    else:
        highlighted = 0
        json['isHighlighted'] = 0
    if 'isEdited' in json:
        edited = json['isEdited']
    else:
        edited = 0
        json['isEdited'] = 0
    if 'isSpam' in json:
        spam = json['isSpam']
    else:
        spam = 0
        json['isSpam'] = 0
    if 'isDeleted' in json:
        deleted = json['isDeleted']
    else:
        deleted = 0
        json['isDeleted'] = 0
    db.insert("""INSERT INTO posts (date,thread_id,message,user_id,forum_id,parent,approved,highlighted,edited,spam,deleted) 
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (
    json['date'], json['thread'], json['message'], uid, fid, parent, approved, highlighted, edited, spam, deleted))

    pid = db.query("SELECT LAST_INSERT_ID() as id")[0]['id']
    json['id'] = pid
    return send_resp(json)


@mod.route("/details/", methods=["GET"])
def details():
    json = getJson(request)
    check_required(json, ['post'])
    related = []
    if 'related' in json:
        related = json['related']
    return send_resp(post_details(json['post'], related), "No such post")


@mod.route("/list/", methods=["GET"])
def list():
    return send_resp(listing(getJson(request), 'post'))


@mod.route("/remove/", methods=["POST"])
def remove():
    json = request.json
    check_required(json, ['post'])
    moderate(json, 'post', 'remove')
    return send_resp(json)


@mod.route("/restore/", methods=["POST"])
def restore():
    json = request.json
    check_required(json, ['post'])
    moderate(json, 'post', 'restore')
    return send_resp(json)


@mod.route("/update/", methods=["POST"])
def update():
    json = request.json
    check_required(json, ['post', 'message'])
    db.insert("UPDATE posts SET message=%s, date=date where pid=%s", (json['message'], json['post']))
    return send_resp(post_details(json['post']), "No such post found")


@mod.route("/vote/", methods=["POST"])
def vote():
    return voter(getJson(request), 'post')
