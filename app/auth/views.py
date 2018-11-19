from flask import render_template, url_for, redirect, request, make_response, session
from flask_login import login_user, login_required, current_user
import json

from . import auth
from ..models import User, Permission, user_to_json_getInfo
from ..email import send_msg
from .. import db
from ..decorators import permission_required, admin_required

@auth.route('/')
def login_page():
    return render_template('login.html')

@auth.route('/login', methods=['GET','POST'])
def login():
    resp = make_response()
    resp.headers['content-type'] = 'application/json'
    data = json.loads(request.data)
    user = User.query.filter_by(username=data['username']).first()
    if user is not None and user.verify_password(data['password']):
        session['name'] = data['username']
        login_user(user)
        resp.status_code = 200
        resp.response = json.dumps({
            'message': 'success',
            'code': 200,
            'data': user
        }, default=user_to_json_getInfo)
    else:
        resp.status_code = 404
        resp.response = json.dumps({
            'message': 'user not exist',
            'error_code': 4001
        })
    return resp

@auth.route('/register', methods=['POST'])
def register():
    data = json.loads(request.data)
    user = User(username=data['username'], password=data['password'], email=data['email'])
    db.session.add(user)
    db.session.commit()

    token = user.generate_confirm_token()
    send_msg(user.email, 'Confirm your Account', 'auth/email', user=user, token=token)
    return redirect(url_for('main.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return "You have confirmed your account, thanks"

    if current_user.confirm(token):
        return "You have confirmed your account, thanks"
    else:
        return "The confirmation link is invalid or has expired."

@auth.route('/admin')
@admin_required
def only_for_admin():
    return 'only for admin'

@auth.route('/moderator')
@permission_required(Permission.MODERATE_COMMENTS)
def only_for_moderators():
    return 'only for moderators'




