from flask import Blueprint, render_template, request, url_for

blue_admin_setting = Blueprint("blue_admin_setting",
                               __name__,
                               url_prefix='/admin',
                               template_folder='../../../templates',
                               static_folder='../../../static'
                               )


@blue_admin_setting.route('/setting')
def content_index():
    return 'setting/index'
