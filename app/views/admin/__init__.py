from app.views.admin.index import blue_admin_index
from app.views.admin.user import blue_admin_user
from app.views.admin.manage import blue_admin_manage
from app.views.admin.setting import blue_admin_setting
from app.views.admin.content import blue_admin_content
from app.views.admin.middleware import check_login, before_response
from app.views.admin.exception import blue_admin_exception


def init_admin_blue(App):
    check_login(App)
    App.register_blueprint(blueprint=blue_admin_index)
    App.register_blueprint(blueprint=blue_admin_user)
    App.register_blueprint(blueprint=blue_admin_manage)
    App.register_blueprint(blueprint=blue_admin_content)
    App.register_blueprint(blueprint=blue_admin_setting)
    App.register_blueprint(blueprint=blue_admin_exception)
    before_response(App)
