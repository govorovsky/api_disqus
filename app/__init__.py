from flask import Flask, request, jsonify
import sys

app = Flask(__name__)
print 'init'



from api.user import mod as user_api
from api.forum import mod as forum_api
from api.thread import mod as thread_api
from api.post import mod as post_api

app.register_blueprint(user_api)
app.register_blueprint(forum_api)
app.register_blueprint(thread_api)
app.register_blueprint(post_api)
