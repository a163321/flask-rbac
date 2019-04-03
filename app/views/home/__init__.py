from app.views.home.index import blue_home_index
from app.views.home.user import blue_home_user


def init_home_blue(App):
    App.register_blueprint(blueprint=blue_home_index)
    App.register_blueprint(blueprint=blue_home_user)
