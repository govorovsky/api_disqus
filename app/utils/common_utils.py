from flask import request, jsonify
from app.db import db
import urlparse

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def id_by_email(email):
    res = db.query("SELECT id FROM users where email=%s",(email))
    if res.__len__() > 0:
        return res[0]['id']
    return -1

def email_by_id(id):
    res = db.query("SELECT email FROM users where id=%s",(id))
    return res[0]['email']

def user_by_email(email):
    res = db.query("SELECT * FROM users where email=%s",(email))
    return res[0]

def getBool(val):
    return (val.lower() == "true")

def send_resp(data, msg=None):
    if (data.__len__() == 0) and ( msg is not None):
        return jsonify({u'code':1, u'message':msg})
    return jsonify({u'code':0, u'response' : data})

def getJson(request):
    if request.method == 'GET':
        return dict( (k, v if len(v)>1 else v[0] ) 
        for k, v in urlparse.parse_qs(request.query_string).iteritems() )
    else:
        return request.json


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
    res = db.query("SELECT * from forums where shortname=%s",forum)
    details['id'] = res[0]['fid']
    details['short_name'] = res[0]['shortname']
    details['name'] = res[0]['fname']
    details['user'] = email_by_id(res[0]['founder_id'])
    return details

def listThr(json):
    from app.api.thread import thread_details
    if 'forum' in json:
        how = 'forum_id'
        id = id_by_sname(json['forum'])
    else:
        how = 'user_id'
        id = id_by_email(json['user'])
    if 'related' in json:
        related = json['related']
    else:
        related = []
    query = "SELECT tid FROM threads where %s=%%s" % (how)
    params = ()
    params += (id,)
    if 'since' in json:
        query += " AND date >= %s"
        params += (json['since'],)
    if 'order' in json:
        order = json['order']
    else:
        order = 'desc'
    query += " ORDER BY date %s" % (order)
    if 'limit' in json:
        query+=" LIMIT %s" % (json['limit'])
    print query
    lst = db.query(query, (params))
    result = []
    if lst.__len__() > 0:
        for thread in lst: # for every id get thread info
            thr = thread_details(thread['tid'],related)
            result.append(thr)
    return result
    
    

    
