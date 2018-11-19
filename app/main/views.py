from flask import render_template, url_for, redirect, session, make_response, request
from flask_login import login_required
import json, os

from . import main
from .. import db
from ..models import UserForm, User, user_to_json_getInfo

@main.route('/index')
def index():
    resp = make_response()
    resp.status_code = 200
    resp.headers['content-type'] = 'text/html'
    resp.response = render_template('index.html')
    return resp

@main.route('/api/user/<username>')
def getUserInfo(username):
    resp = make_response()
    resp.headers['content-type'] = 'application/json'
    user = User.query.filter_by(username=username).first()

    if user is None:
        resp.status_code = 404
        resp.response = json.dumps({
            'error_code': 4001,
            'message': 'cant find user'
        })
    resp.status_code = 200
    resp.response = json.dumps(user, default=user_to_json_getInfo)
    return resp

@main.route('/upload')
def upload_page():
    resp = make_response()
    resp.status_code = 200
    resp.headers['content-type'] = 'text/html'
    resp.response = render_template('upload.html')
    return resp

@main.route('/api/upload', methods=['POST'])
def upload():
    data = request.files.get('file')
    print(data,type(data))
    if data:
        data.save(os.path.join(os.getcwd(), 'app', 'uploads', data.filename))

    resp = make_response()
    resp.status_code = 200
    resp.headers['content-type'] = 'application/json'
    resp.response = json.dumps({
        'code': 200,
        'message': 'successs'
    })
    return resp