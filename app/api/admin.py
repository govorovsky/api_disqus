from flask import Blueprint
from flask import jsonify

from app.utils.common_utils import prefix
from app.config import *

import MySQLdb

mod = Blueprint('admin', __name__, url_prefix=prefix + '/')


@mod.route("clear/", methods=['GET', 'POST'])
@mod.route("clear", methods=['GET', 'POST'])
def truncate():
    conn = MySQLdb.connect(host, user, password, forum_db)
    db = conn.cursor()
    tables = ['users', 'posts', 'threads', 'forums', 'subscriptions', 'followers']
    db.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        db.execute("TRUNCATE TABLE %s" % table)
    db.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    db.close()
    conn.close()
    return jsonify({'message': 'tables dropped'})


