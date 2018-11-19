from flask import Blueprint

follow = Blueprint('follow', __name__)

from . import views