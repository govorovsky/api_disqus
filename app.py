#!flask/bin/python
from flask import Flask, request, jsonify
from api.user import mod as user_api
from api.forum import mod as forum_api
from api.thread import mod as thread_api
from api.post import mod as post_api

app = Flask(__name__)

app.register_blueprint(user_api)
app.register_blueprint(forum_api)
app.register_blueprint(thread_api)
app.register_blueprint(post_api)

if __name__ == '__main__':
    app.run(debug = True)
