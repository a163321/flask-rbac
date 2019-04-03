from flask import Blueprint
blue_home_index = Blueprint("blue_home_index", __name__, url_prefix='/home')

@blue_home_index.route('/')
def index():
    return 'home/index'
