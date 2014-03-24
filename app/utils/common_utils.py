from flask import request, jsonify

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def getBool(val):
    return (val.lower() == "true")

def send_resp(data):
    if data.__len__() == 0 :
        return jsonify({u'code':1})
    return jsonify({u'code':0, u'response' : data})

def check_required(json, vars):
    for var in vars:
        if var not in json:
            raise Exception("Missed required variable")

