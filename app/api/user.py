from flask import Blueprint

from app.utils.common_utils import *


mod = Blueprint('user', __name__, url_prefix=prefix + '/user')


@mod.route("/create/", methods=["POST"])
def create():
    json = request.json
    resp = {}
    resp["name"] = json["name"]
    resp["email"] = json["email"]
    uniq = id_by_email(json['email'])
    if uniq != -1:
        return send_resp(user_details(uniq, 'id'))  # return existing data
    if "isAnonymous" in json:
        resp["isAnonymous"] = json["isAnonymous"]
    else:
        resp["isAnonymous"] = False

    if resp["isAnonymous"] is True:
        db.insert("INSERT INTO users(email,anonymous) values (%s,%s) ", (resp["email"], resp["isAnonymous"]))
        id = db.query("SELECT LAST_INSERT_ID() as id")
        resp["id"] = id[0]["id"]
        resp['name'] = None
        resp = {u'code': 0, u'response': resp}
        return jsonify(resp)

    resp["username"] = json["username"]
    resp["about"] = json["about"]
    db.insert("INSERT INTO users(username,email,about,name) values (%s,%s,%s,%s) ",
              (resp["username"], resp["email"], resp["about"], resp["name"]))
    id = db.query("SELECT LAST_INSERT_ID() as id")
    resp["id"] = id[0]["id"]
    resp = {u'code': 0, u'response': resp}
    return jsonify(resp)


@mod.route("/details/", methods=["GET"])
def details():
    json = getJson(request)
    check_required(json, ['user'])
    return send_resp(user_details(json["user"], 'email'), "No such user found")


@mod.route("/follow/", methods=["POST"])
def follow():
    json = request.json
    follower = json["follower"]
    followee = json["followee"]
    follower_id = user_by_email(follower)
    followee_id = user_by_email(followee)
    db.insert("INSERT INTO followers (follower,followee) values (%s, %s) ON DUPLICATE KEY UPDATE active=1",
              (follower_id, followee_id))
    return send_resp(user_details(follower_id, 'id'), "No such user found")


def listFollow(json, who):
    vals = ['follower', 'followee']
    t = 0 if who == 'follower' else 1
    params = ()
    id = user_by_email(json['user'])
    if id < 0:
        return send_resp({}, "No such user found")
    params += (id,)
    query = """SELECT %s from followers inner join users u on %s=u.id where %s=%%s AND active=1""" % (
        vals[t], vals[t], vals[(t + 1) % 2])
    if 'since_id' in json:
        query += ' AND %s >= %%s' % (vals[t] )
        params += (json['since_id'],)
    if 'order' in json:
        order = json['order']
    else:
        order = 'desc'
    query += ' ORDER BY u.name %s ' % (order)
    if 'limit' in json:
        query += ' LIMIT %s' % (json['limit'])
    followers = db.query(query, params)
    result = []
    for flw in followers:
        result.append(user_details(flw[vals[t]], 'id'))
    return send_resp(result)


@mod.route("/listFollowers/", methods=["GET"])
def listFollowers():  # !maybe slow
    return listFollow(getJson(request), 'follower')


@mod.route("/listFollowing/", methods=["GET"])
def listFollowing():
    return listFollow(getJson(request), 'followee')


@mod.route("/listPosts/", methods=["GET"])
def listPosts():
    return send_resp(listing(getJson(request), 'post'))


@mod.route("/unfollow/", methods=["POST"])
def unfollow():
    json = request.json
    follower = json["follower"]
    followee = json["followee"]
    follower_id = user_by_email(follower)
    followee_id = user_by_email(followee)
    if followee_id < 0 or follower_id < 0:
        return send_resp({}, "No such user found")
    db.insert("UPDATE followers SET active=0 where follower=%s AND followee=%s", (follower_id, followee_id))
    return send_resp(user_details(follower_id, 'id'), "No such user found")


@mod.route("/updateProfile/", methods=["POST"])
def updateprofile():
    json = request.json
    check_required(json, ['about', 'user', 'name'])
    if id_by_email(json['user']) == -1:
        return send_resp({}, "No such user found")
    db.insert("UPDATE users SET about=%s, name=%s where email=%s", (json['about'], json['name'], json['user']))
    return send_resp(user_details(json['user'], 'email'), "No such user found")
