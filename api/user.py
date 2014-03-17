from flask import Flask, request, jsonify, Blueprint


mod=Blueprint('user',__name__, url_prefix='/user')

@mod.route("/create/",methods=["POST"])
def create():
    json = request.json
    return jsonify(json)

@mod.route("/details/",methods=["GET"])
def details():
    pass

@mod.route("/follow/",methods=["POST"])
def follow():
    pass

@mod.route("/listFollowers/",methods=["GET"])
def listFollowers():
    pass

@mod.route("/listFollowing",methods=["GET"])
def listFollowing():
    pass

@mod.route("/listPosts/",methods=["GET"])
def listPosts():
    pass

@mod.route("/unfollow/",methods=["POST"])
def unfollow():
    pass

@mod.route("/updateProfile",methods=["POST"])
def updateprofile():
    pass
