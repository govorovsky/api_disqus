from flask import request, jsonify
from app.db import db

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getBool(val):
    return (val.lower() == "true")

def send_resp(data, msg=None):
    if (data.__len__() == 0) and ( msg is not None):
        return jsonify({u'code':1, u'message':msg})
    return jsonify({u'code':0, u'response' : data})

def check_required(json, vars):
    for var in vars:
        if var not in json:
            raise Exception("Missed required variable")

def id_by_sname(name):
    id = db.query("SELECT fid from forums where shortname=%s", (name))
    return id[0]['fid']

def sname_by_id(id):
    name = db.query("SELECT shortname from forums where fid=%s", (id))
    return name[0]['shortname']

def forum_details(forum):
    details = {}
    res = db.query("SELECT * from forums f INNER JOIN users on id=founder_id where shortname=%s",forum)
    details['id'] = res[0]['fid']
    details['short_name'] = res[0]['shortname']
    details['name'] = res[0]['fname']
    details['user'] = res[0]['email']
    return details
