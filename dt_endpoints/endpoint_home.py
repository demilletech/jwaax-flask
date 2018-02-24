from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import redirect


from dt_auth import auth_jwaax_provider

import dtutil

home_page = Blueprint('home_page', __name__, template_folder='templates')


@home_page.route('/')
def index():
    jt = dtutil.get_in_request('jt')
    print(jt)
    if not jt or not auth_jwaax_provider.verify_token(jt):
        return redirect("/signin/")
    return "Index"


@home_page.route('/signin/', methods=['GET'])
def signin():
    newjt = auth_jwaax_provider.generate_token(
        '0', '127.0.0.1:5000/signin_jwaax/')
    return redirect('https://secure.demilletech.net/api/external/signin/?request_token=' + newjt)


@home_page.route('/signin_jwaax/', methods=['GET'])
def signin_jwaax():
    newjt = dtutil.get_in_request('jt')
    resp = make_response(redirect('/'))
    resp.set_cookie('jt', newjt)
    return resp
