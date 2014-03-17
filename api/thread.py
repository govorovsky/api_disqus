from flask import Flask, request, jsonify, Blueprint



mod=Blueprint('thread',__name__, url_prefix='/thread')


@mod.route("/close/",methods=["POST"])
def close():
    json = request.json
    resp = {u'code': 0, u'response': json}
    return jsonify(resp)


@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    return jsonify(json)

@mod.route("/details/",methods=["GET"])
def details():
    pass

@mod.route("/list/",methods=["GET"])
def list():
    pass

@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass


@mod.route("/open/",methods=["POST"])
def open(action):
    json = request.json
    thread_id = json["thread"]
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

