from . import follow
from flask import make_response, request
from ..models import Follow, User, user_to_json_getInfo
import json

@follow.route('/<userid>')
def getFollow(userid):
    resp = make_response()
    resp.status_code = 200
    resp.headers['content-type'] = 'application/json'

    user = User.query.filter_by(id=userid).first()
    follower_ids = list(map(lambda f:f.follower_id,user.follower.all()))
    followed_ids = list(map(lambda f:f.followed_id, user.followed.all()))

    followers = User.query.filter(User.id.in_(follower_ids)).all()
    followeds = User.query.filter(User.id.in_(followed_ids)).all()

    resp.response = json.dumps({
        'followers': followers,
        'followeds': followeds,
    },default=user_to_json_getInfo)
    return resp


