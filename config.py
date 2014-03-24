from flask import Flask, request, jsonify
from flaskext.mysql import MySQL

mysql = MySQL()

app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'qazxsw12'
app.config['MYSQL_DATABASE_DB'] = 'gameserver'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
