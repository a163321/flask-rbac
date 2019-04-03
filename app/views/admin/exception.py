from flask import Blueprint, render_template
from app.common import Tool

blue_admin_exception = Blueprint("blue_admin_exception",
                                 __name__,
                                 url_prefix='/admin',
                                 template_folder='../../../templates',
                                 static_folder='../../../static'
                                 )


@blue_admin_exception.app_errorhandler(404)
def error_not_found(e):
    return render_template('admin/exception/404.html')


@blue_admin_exception.app_errorhandler(403)
def error_not_auth(e):
    return render_template('admin/exception/403.html')


@blue_admin_exception.app_errorhandler(415)
def error_request_method(e):
    return Tool.admin_json_response('请求方式错误', code=0)
