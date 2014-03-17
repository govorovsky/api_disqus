from flask import Flask, request, jsonify, Blueprint


mod=Blueprint('forum',__name__, url_prefix='/forum')

resp = {}
resp["code"] = 0;
resp["response"] = []


@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    return jsonify(json)


@mod.route("/details/",methods=["GET"])
def details():
    pass

@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass

@mod.route("/listThreads/",methods=["GET"])
def listThreads():
    pass

@mod.route("/listUsers/",methods=["GET"])
def listUsers():
    pass

