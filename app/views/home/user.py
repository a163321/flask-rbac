from flask import Blueprint

blue_home_user = Blueprint("blue_home_user", __name__, url_prefix='/home/user')


@blue_home_user.route('/')
def index():
    return 'home/user/index'
