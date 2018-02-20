from flask import request

def get_in_request(key):
    jsonv = request.get_json()
    if jsonv is not None and key in jsonv:
        return jsonv[key]
    if key in request.form:
        return request.form[key]
    if key in request.args:
        return request.args[key]
    if key in request.cookies:
        return request.cookies[key]
    return None

def isdict(item):
    return isinstance(item, dict)