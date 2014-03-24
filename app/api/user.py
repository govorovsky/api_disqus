from flask import Flask, request, jsonify, Blueprint
from app.db import db
from app.utils.common_utils import *


mod=Blueprint('user',__name__, url_prefix='/user')

def id_by_email(email):
    res = db.query("SELECT id FROM users where email=%s",(email))
    if res.__len__() > 0:
        return res[0]['id']
    return -1

def user_by_email(email):
    res = db.query("SELECT * FROM users where email=%s",(email))
    return res[0]

def get_following(id):
    res = db.query("SELECT email FROM followers INNER JOIN users on followee=id where follower=%s and active=1",(id))
    result = []
    for followee in res:
        result.append(followee['email'])
    return result

def get_followers(id):
    res = db.query("SELECT email FROM followers INNER JOIN users on follower=id where followee=%s and active=1",(id))
    result = []
    for followee in res:
        result.append( followee['email'])
    return result

def get_subscriptions(id):
    res = db.query("SELECT * FROM subscriptions where users_id=%s",(id))
    result = []
    for subs in res:
        result.append( subs['threads_id'])
    return result




def user_details(ident, method):
    query = "SELECT * FROM users where %s=%%s" % (method)
    res = db.query(query,(ident))
    user = {}
    if res.__len__() != 0:
        uid = res[0]["id"] 
        user["followers"] = get_followers(uid)
        user["following"] = get_following(uid)
        user["id"] = uid
        user["subscriptions"] = get_subscriptions(uid)
        user["isAnonymous"] = bool(res[0]["anonymous"])
        user["email"] = res[0]["email"]
        if(user["isAnonymous"] == True):
            user["name"] = None
        else: # Anon cant have about info and name?
            user["username"] = res[0]["username"]
            user["about"] = res[0]["about"]
            user["name"] = res[0]["name"]
    return user


@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    resp ={}
    resp["name"] = json["name"]
    resp["email"] = json["email"]
    if id_by_email(json['email']) != -1:
        return send_resp({}, "User already exists")
    if "isAnonymous" in json:
        resp["isAnonymous"] = getBool(json["isAnonymous"])
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
    db.insert("INSERT INTO users(username,email,about,name) values (%s,%s,%s,%s) ", (resp["username"],resp["email"], resp["about"],resp["name"]))
    id = db.query("SELECT LAST_INSERT_ID() as id")
    resp["id"] = id[0]["id"]
    resp = {u'code': 0, u'response': resp}
    return jsonify(resp)

@mod.route("/details/",methods=["GET"])
def details():
    json = request.json
    return send_resp(user_details(json["user"], 'email'), "No such user found")

@mod.route("/follow/",methods=["POST"])
def follow():
    json = request.json
    follower = json["follower"]
    followee = json["followee"]
    follower_id = user_by_email(follower)['id']
    followee_id = user_by_email(followee)['id']
    db.insert("INSERT INTO followers (follower,followee) values (%s, %s) ON DUPLICATE KEY UPDATE active=(!active)", (follower_id, followee_id))
    resp = {u'code': 0, u'response': user_details(follower_id,'id')}
    return jsonify(resp)


def listFollow(json,who):
    vals = ['follower', 'followee']
    t = 0 if who == 'follower' else 1
    id = user_by_email(json['user'])['id']
    query = """SELECT %s from followers where %s=%%s and active=1""" % (vals[t], vals[(t+1)%2])
    followers = db.query(query,id);
    result = []
    for flw in followers:
       result.append(user_details(flw[vals[t]],'id'))
    return jsonify({u'code': 0, u'response': result})



@mod.route("/listFollowers/",methods=["GET"])
def listFollowers(): # !maybe slow
    return listFollow(request.json, 'follower')

@mod.route("/listFollowing/",methods=["GET"])
def listFollowing():
    return listFollow(request.json, 'followee')


@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    
    pass

@mod.route("/unfollow/",methods=["POST"])
def unfollow():
    json = request.json
    follower = json["follower"]
    followee = json["followee"]
    follower_id = user_by_email(follower)['id']
    followee_id = user_by_email(followee)['id']
    db.insert("UPDATE followers SET active=0 where follower=%s AND followee=%s",(follower_id, followee_id))
    resp = {u'code': 0, u'response': user_details(follower_id,'id')}
    return jsonify(resp)


@mod.route("/updateProfile/",methods=["POST"])
def updateprofile():
    json = request.json
    check_required(json, ['about', 'user', 'name'])
    if id_by_email(json['user']) == -1:
        return send_resp({}, "No such user found")
    db.insert("UPDATE users SET about=%s, name=%s where email=%s", (json['about'], json['name'], json['user']))
    return send_resp(user_details(json['user'], 'email'))
