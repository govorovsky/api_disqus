import urlparse

from flask import jsonify, request

from app.db import db

prefix = '/db/api'

tables = {
    'thread': ['tid', 'threads', 'all'],
    'post': ['pid', 'posts', 'all'],
    'user': ['user_id', 'posts', 'distinct'],
    'forum': ['shortname', 'forums']
}


def is_exist(what, id):
    thr = db.query("SELECT %s from %s WHERE %s=%%s" % (tables[what][0], tables[what][1], tables[what][0]), id)
    return 1 if (thr.__len__() > 0) else 0


def moderate(json, what, action):
    if what == 'thread':
        id = json['thread']
    else:
        id = json['post']
    act = 1 if (action == 'close' or action == 'remove') else 0
    target = 'closed' if ( action == 'close' or action == 'open') else 'deleted'
    if is_exist(what, id):
        db.insert(
            "UPDATE %s SET date=date, %s=%s " % (tables[what][1], target, act) + " where %s=%%s" % (tables[what][0]),
            id)
        return send_resp(json)
    else:
        return send_resp({}, "No such %s found" % what)


def get_following(id):
    res = db.query("SELECT email FROM followers INNER JOIN users on followee=id where follower=%s and active=1", id)
    result = []
    for followee in res:
        result.append(followee['email'])
    return result


def get_followers(id):
    res = db.query("SELECT email FROM followers INNER JOIN users on follower=id where followee=%s and active=1", id)
    result = []
    for followee in res:
        result.append(followee['email'])
    return result


def get_subscriptions(id):
    res = db.query("SELECT threads_id FROM subscriptions where users_id=%s AND active=1 order by threads_id desc", id)
    result = []
    for subs in res:
        result.append(subs['threads_id'])
    return result


def user_details(ident, method, src=None):
    query = "SELECT * FROM users where %s=%%s" % method
    if src is not None:
        res = src
    else:
        res = db.query(query, ident)
    user = {}
    if res.__len__() != 0:
        user['id'] = uid = res[0]["id"]
        user["followers"] = get_followers(uid)
        user["following"] = get_following(uid)
        user["subscriptions"] = get_subscriptions(uid)
        user["isAnonymous"] = bool(res[0]["anonymous"])
        user["email"] = res[0]["email"]
        user["username"] = res[0]["username"]
        user["about"] = res[0]["about"]
        user["name"] = res[0]["name"]
    return user


def post_details(pid, related=None):
    p = db.query("SELECT * FROM posts p join forums as f on f.fid = p.forum_id join users u on u.id = p.user_id where p.pid = %s" , (pid))
    if p.__len__() > 0:
        post = {
            'parent': p[0]['parent'],
            'isApproved': bool(p[0]['approved']),
            'isHighlighted': bool(p[0]['highlighted']),
            'isEdited': bool(p[0]['edited']),
            'isSpam': bool(p[0]['spam']),
            'isDeleted': bool(p[0]['deleted']),
            'date': str(p[0]['date']),
            'thread': p[0]['thread_id'],
            'message': p[0]['message'],
            'id': p[0]['pid'],
            'likes': p[0]['likes'],
            'dislikes': p[0]['dislikes'],
            'points': p[0]['likes'] - p[0]['dislikes']
        }
        if related is not None:
            if 'user' in related:
                post['user'] = user_details(p[0]['user_id'], 'id', p)
            if 'thread' in related:
                post['thread'] = thread_details(post['thread'])
            if 'forum' in related:
                post['forum'] = forum_details(p[0]['forum_id'], 'fid', p)

        if 'user' not in post:
            post['user'] = p[0]['email']
        if 'forum' not in post:
            post['forum'] = p[0]['shortname']
        return post
    return {}


def thread_details(thread, related=None, src=None):
    query = "SELECT * from threads "
    query += " JOIN users u ON user_id=u.id"
    query += " JOIN forums f ON forum_id=f.fid"
    query += " WHERE tid=%s"
    thr = db.query(query, thread) if src is None else src
    resp = {}
    if thr.__len__() != 0:
        if related is not None:
            if 'user' in related:
                resp['user'] = user_details(thr[0]['user_id'], 'id', thr)
            if 'forum' in related:
                resp['forum'] = forum_details(thr[0]['forum_id'], 'fid', thr)
        if 'user' not in resp:
            resp['user'] = thr[0]['email']
        if 'forum' not in resp:
            resp['forum'] = thr[0]['shortname']
        resp['date'] = str(thr[0]['date'])
        resp['title'] = thr[0]['title']
        resp['message'] = thr[0]['message']
        resp['dislikes'] = thr[0]['dislikes']
        resp['likes'] = thr[0]['likes']
        resp['points'] = thr[0]['likes'] - thr[0]['dislikes']
        resp['slug'] = thr[0]['slug']
        resp['id'] = thr[0]['tid']
        resp['isClosed'] = bool(thr[0]['closed'])
        resp['isDeleted'] = bool(thr[0]['deleted'])
        resp['posts'] = count_posts(thr[0]['tid'])
    return resp


def count_posts(thread):
    thr = db.query("SELECT COUNT(*) as cnt from posts WHERE thread_id=%s", thread)
    return thr[0]['cnt']


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def id_by_email(email):
    res = db.query("SELECT id FROM users where email=%s", email)
    if res.__len__() > 0:
        return res[0]['id']
    return -1


def email_by_id(id):
    res = db.query("SELECT email FROM users where id=%s", id)
    return res[0]['email']


def user_by_email(email):
    res = db.query("SELECT id FROM users where email=%s", email)
    if res.__len__() > 0:
        return res[0]['id']
    return -1


def send_resp(data, msg=None):
    if (data.__len__() == 0) and (msg is not None):
        return jsonify({u'code': 1, u'message': msg})
    return jsonify({u'code': 0, u'response': data})


def getJson(request):
    if request.method == 'GET':
        return dict((k, v if len(v) > 1 else v[0] )
                    for k, v in urlparse.parse_qs(request.query_string).iteritems())
    else:
        return request.json


def check_required(json, vars):
    for var in vars:
        if var not in json:
            raise Exception("Missed required variable")


def id_by_sname(name):
    id = db.query("SELECT fid from forums where shortname=%s", name)
    if id.__len__() > 0:
        return id[0]['fid']
    else:
        return -1


def sname_by_id(id):
    name = db.query("SELECT shortname from forums where fid=%s", id)
    return name[0]['shortname']


def forum_details(forum, how, src=None):
    details = {}
    res = db.query("SELECT * from forums where %s=%%s" % how, forum) if(src is None) else src
    if res.__len__() > 0:
        details['id'] = res[0]['fid']
        details['short_name'] = res[0]['shortname']
        details['name'] = res[0]['fname']
        details['user'] = email_by_id(res[0]['founder_id'])
    return details


def listing(json, what):
    how = ''
    id = -1
    if 'thread' in json and what in ['post']:
        how = 'thread_id'
        id = json['thread']
    if 'forum' in json and what in ['post', 'thread', 'user']:
        how = 'forum_id'
        id = id_by_sname(json['forum'])
    if 'user' in json and what in ['post', 'thread']:
        how = 'user_id'
        id = id_by_email(json['user'])
    if 'related' in json:
        related = json['related']
    else:
        related = []

    if id < 0 or how == '':
        return []

    query = "SELECT %s %s FROM %s where %s=%%s" % (tables[what][2], tables[what][0], tables[what][1], how)
    params = ()
    params += (id,)
    if 'since' in json:
        query += " AND date >= %s"
        params += (json['since'],)
    if 'since_id' in json:
        query += " AND user_id >= %s"
        params += (json['since_id'],)
    if 'order' in json:
        order = json['order']
    else:
        order = 'desc'
    type_order = 'date' if what is not 'user' else 'user_id'
    query += " ORDER BY %s %s" % (type_order, order)
    if 'limit' in json:
        query += " LIMIT %s" % (json['limit'])
    lst = db.query(query, params)
    result = []
    if lst.__len__() > 0:
        if what == 'user':
            for ids in lst:  # TODO FIX THIS
                thr = entity_handlers[what](ids[tables[what][0]], 'id')
                result.append(thr)
        else:
            for ids in lst:  # for every id get entity info, may be slow...
                thr = entity_handlers[what](ids[tables[what][0]], related)
                result.append(thr)
    return result


def voter(json, entity):
    check_required(json, ['vote', entity])
    vt = int(json['vote'])
    if entity == 'thread':
        table = 'threads'
    if entity == 'post':
        table = 'posts'
    type = 'likes' if (vt > 0) else 'dislikes'
    query = "UPDATE %s SET %s = %s + 1, date=date where %sid=%%s" % (
        table, type, type, entity[0])  #TIMESTAMP auto-update needed?
    db.insert(query, json[entity])
    return send_resp(entity_handlers[entity](json[entity]), "No such %s found" % entity)


entity_handlers = {
    'thread': thread_details,
    'post': post_details,
    'forum': forum_details,
    'user': user_details
}
